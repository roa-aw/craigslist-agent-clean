"""
agent/agent.py
LLM-powered sales agent using OpenAI function calling.
Manages conversation history and the tool-call loop.
"""

from __future__ import annotations
import json
import os
from typing import Optional
from openai import OpenAI
from tools import TOOL_DEFINITIONS, TOOL_MAP

SYSTEM_PROMPT = """You are a friendly and knowledgeable used-car sales assistant.
You have access to a real vehicle inventory sourced from Craigslist listings across the US.

Your job:
1. Understand what the customer is looking for (make, model, budget, condition, location, etc.)
2. Call the appropriate inventory tool to fetch real data — never make up listings.
3. Present results clearly: list each vehicle with its year, make, model, price, condition,
   mileage (if available), and region. Format prices with commas, e.g. $12,500.
4. If no results are found, use get_similar() to find alternatives and tell the user
   you're showing nearby options.
5. If the user's request is too vague (e.g. "show me cars"), ask ONE clarifying question
   before calling a tool.
6. Keep responses conversational and concise — bullet points for listings, prose for advice.
7. If the user asks about pricing trends or "how much does X cost", use get_price_range().
8. Always end with a helpful follow-up offer, e.g. "Want me to filter by location or condition?"

Never invent vehicle data. Only report what the tools return."""


class SalesAgent:
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model  = model
        self.history: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # ── public interface ──────────────────────────────────────────────────

    def chat(self, user_message: str) -> str:
        """Send a user message; return the agent's final text response."""
        self.history.append({"role": "user", "content": user_message})
        return self._run_loop()

    def reset(self) -> None:
        """Clear conversation history (keep system prompt)."""
        self.history = [self.history[0]]

    # ── internal ──────────────────────────────────────────────────────────

    def _run_loop(self) -> str:
        """
        Call the LLM, execute any requested tools, then loop until the
        model produces a plain text response (no more tool calls).
        """
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            # No tool call → final answer
            if not msg.tool_calls:
                text = msg.content or ""
                self.history.append({"role": "assistant", "content": text})
                return text

            # Append the assistant's tool-call request to history
            self.history.append(msg)

            # Execute every requested tool and append results
            for tc in msg.tool_calls:
                result = self._call_tool(tc.function.name, tc.function.arguments)
                self.history.append({
                    "role":         "tool",
                    "tool_call_id": tc.id,
                    "content":      json.dumps(result),
                })
            # Loop: let the model see the tool results and respond

    def _call_tool(self, name: str, args_json: str) -> dict:
        """Deserialise arguments, call the tool, return the result dict."""
        func = TOOL_MAP.get(name)
        if func is None:
            return {"error": f"Unknown tool: {name}"}
        try:
            args = json.loads(args_json) if args_json else {}
            return func(**args)
        except Exception as exc:
            return {"error": str(exc)}
