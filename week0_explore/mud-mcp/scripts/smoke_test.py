"""End-to-end smoke test: drive the MCP server over stdio against the live MUD."""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    params = StdioServerParameters(command="python", args=["-m", "mud_mcp.server"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("TOOLS:", [t.name for t in tools.tools])

            r = await session.call_tool("mud_status", {})
            print("\nstatus (before):", r.content[0].text)

            r = await session.call_tool("mud_connect", {})
            print("\nconnect banner (tail):\n", r.content[0].text[-300:])

            r = await session.call_tool("mud_status", {})
            print("\nstatus (after):", r.content[0].text)

            r = await session.call_tool("mud_disconnect", {})
            print("\ndisconnect:", r.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
