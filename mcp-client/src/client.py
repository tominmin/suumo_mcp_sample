import json
from contextlib import AsyncExitStack
from typing import Optional

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import OpenAI

SERVER_URL = "http://localhost:8000/mcp"

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI()

    async def connect_to_server(self, server_url: str = SERVER_URL):
        """Connect to an MCP server over HTTP

        Args:
            server_url: URL of the running MCP server
        """
        http_transport = await self.exit_stack.enter_async_context(sse_client(server_url))
        self.session = await self.exit_stack.enter_async_context(ClientSession(*http_transport))
        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()

        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            } for tool in response.tools
        ]

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=available_tools,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id
            # Execute tool call
            tool_args = json.loads(tool_call.function.arguments)

            tool_result = await self.session.call_tool(tool_name, tool_args)
            tool_result_contents = [content.model_dump() for content in tool_result.content]

            messages.append(
                {
                    "tool_call_id": tool_call_id,
                    "role": "tool",
                    "name": tool_name,
                    "content": tool_result_contents,
                }
            )

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return response.choices[0].message.content

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()