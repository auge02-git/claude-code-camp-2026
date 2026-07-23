from __future__ import annotations

import http.client
import json
import socket
import ssl
import time
from urllib.parse import urlparse

from .errors import ApiError


class Client:
    RETRYABLE_STATUS_CODES = frozenset({408, 409, 429, 500, 502, 503, 504})
    TRANSIENT_ERRORS = (
        ConnectionResetError,
        ConnectionRefusedError,
        TimeoutError,
        ssl.SSLError,
        socket.gaierror,
        http.client.RemoteDisconnected,
        http.client.HTTPException,
    )
    MAX_RETRIES = 3
    BASE_RETRY_DELAY = 0.5

    def __init__(self, builder) -> None:
        self._builder = builder

    def call(self, *, max_output_tokens: int = 1024) -> dict:
        payload = self._builder.to_api_payload(max_output_tokens=max_output_tokens)
        body = json.dumps(payload)
        last_status = None
        last_body = None

        for attempt in range(1, self.MAX_RETRIES + 2):
            try:
                last_status, last_body = self._post(body)
            except self.TRANSIENT_ERRORS as exc:
                if attempt > self.MAX_RETRIES:
                    raise ApiError(
                        f"API request failed after {attempt} attempts: {exc.__class__.__name__}: {exc}"
                    ) from exc
                time.sleep(self._retry_delay(attempt))
                continue

            if self._is_retryable_status(last_status) and attempt <= self.MAX_RETRIES:
                time.sleep(self._retry_delay(attempt))
                continue

            break

        if last_status is None or last_body is None:
            raise ApiError("API request failed before receiving a response")

        if not (200 <= last_status < 300):
            suffix = "" if attempt == 1 else "s"
            raise ApiError(
                f"API request failed after {attempt} attempt{suffix} ({last_status}): {last_body}"
            )

        return json.loads(last_body)

    def _post(self, body: str) -> tuple[int, str]:
        parsed = urlparse(self._builder.url())
        if parsed.scheme not in {"http", "https"}:
            raise ApiError(f"Unsupported URL scheme: {parsed.scheme}")

        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"

        if parsed.scheme == "https":
            conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443)
        else:
            conn = http.client.HTTPConnection(parsed.hostname, parsed.port or 80)

        try:
            conn.request("POST", path, body=body, headers=self._builder.headers())
            response = conn.getresponse()
            response_body = response.read().decode("utf-8")
            return response.status, response_body
        finally:
            conn.close()

    def _is_retryable_status(self, status_code: int) -> bool:
        return status_code in self.RETRYABLE_STATUS_CODES

    def _retry_delay(self, attempt: int) -> float:
        return self.BASE_RETRY_DELAY * (2 ** (attempt - 1))

