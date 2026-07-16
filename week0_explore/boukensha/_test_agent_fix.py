"""Schnell-Tests für den Agent-Bug-Fix:
- Keine doppelten user-Rollen im Nachrichtenverlauf
- Kein Tool-Loop wenn MUD nicht verbunden
- Korrekte Endantwort nach Tool-Use
"""
from pathlib import Path
from unittest.mock import MagicMock

from boukensha.agent import Agent
from boukensha.config import Config
from boukensha.mud import MudManager

_CFG = Config(home=Path("/tmp/boukensha-test"))


def make_resp(stop_reason, text="Antwort!"):
    resp = MagicMock()
    resp.stop_reason = stop_reason
    resp.content = [MagicMock(type="text", text=text)]
    resp.usage = None
    return resp


def test_no_mud_direkte_antwort():
    """Ohne MUD: keine Tools → Modell liefert direkt end_turn, kein Loop."""
    backend = MagicMock()
    backend.complete.return_value = make_resp("end_turn", "Ich bin Boukensha!")

    agent = Agent(config=_CFG, mud=MudManager(), backend=backend)
    result = agent.step("Wer bist du?")

    assert result == "Ich bin Boukensha!", f"Unerwartetes Ergebnis: {result!r}"
    assert backend.complete.call_count == 1, f"Zu viele Calls: {backend.complete.call_count}"
    call_kwargs = backend.complete.call_args[1]
    assert call_kwargs["tools"] == [], f"Tools sollten leer sein: {call_kwargs['tools']}"
    msgs = call_kwargs["messages"]
    for i in range(len(msgs) - 1):
        assert not (msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "user"), \
            f"Doppelte user-Rollen an Position {i}: {msgs}"
    print("PASS: test_no_mud_direkte_antwort")


def test_no_mud_kein_tool_loop():
    """Ohne MUD darf kein Tool-Loop entstehen (früher: max_steps-Abbruchfehler)."""
    backend = MagicMock()
    backend.complete.return_value = make_resp("end_turn", "Ende!")

    agent = Agent(config=_CFG, mud=MudManager(), backend=backend, max_steps=3)
    result = agent.step("Mach etwas!")
    assert "Abbruch" not in result, f"Unerwarteter Abbruch: {result}"
    assert backend.complete.call_count == 1
    print("PASS: test_no_mud_kein_tool_loop")


def test_tool_use_dann_end_turn():
    """Mit MUD: 1 Tool-Call, dann end_turn – keine doppelten user-Rollen."""
    mud = MagicMock()
    mud.is_open = True
    mud.read.return_value = ""

    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.name = "look"
    tool_block.id = "tool-1"
    tool_block.input = {}

    resp1 = MagicMock()
    resp1.stop_reason = "tool_use"
    resp1.content = [tool_block]
    resp1.usage = None

    resp2 = make_resp("end_turn", "Der Raum sieht gut aus.")

    backend = MagicMock()
    backend.complete.side_effect = [resp1, resp2]

    agent = Agent(config=_CFG, mud=mud, backend=backend)
    look_tool = MagicMock()
    look_tool.name = "look"
    look_tool.run.return_value = "Du siehst einen Raum."
    agent.registry.register(look_tool)

    result = agent.step("Schau dich um!")
    assert result == "Der Raum sieht gut aus.", f"Unerwartetes Ergebnis: {result!r}"
    assert backend.complete.call_count == 2

    for call_num, call in enumerate(backend.complete.call_args_list):
        msgs = call[1]["messages"]
        for i in range(len(msgs) - 1):
            assert not (msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "user"), \
                f"Doppelte user-Rollen in Call {call_num} an Position {i}"
    print("PASS: test_tool_use_dann_end_turn")


if __name__ == "__main__":
    test_no_mud_direkte_antwort()
    test_no_mud_kein_tool_loop()
    test_tool_use_dann_end_turn()
    print("\n✓ Alle Tests bestanden!")
