"""Shared Groq gateway for Restructura One."""

import os

from dotenv import load_dotenv
from groq import Groq


class GroqGateway:
    def __init__(self, model: str | None = None):
        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is missing. Add it to your local .env file."
            )

        self.model = model or os.getenv(
            "GROQ_MODEL", "openai/gpt-oss-120b"
        )
        self.client = Groq(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Groq returned an empty response.")

        return content.strip()
