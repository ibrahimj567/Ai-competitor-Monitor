import json

from openai import OpenAI

from app.core.config import settings


class AIService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def summarize_changes(self, diff_text: str):

        if not diff_text.strip():

            return {
                "summary": "No meaningful changes detected.",
                "severity": "None",
                "confidence": 1.0,
                "changes": []
            }

        prompt = f"""
You are an expert website monitoring assistant.

Analyze the website changes below.

Ignore:
- whitespace
- formatting
- cookie notices
- analytics code
- timestamps
- session IDs

Return ONLY valid JSON.

Format:

{{
  "summary":"...",
  "severity":"Low",
  "confidence":0.95,
  "changes":[
      "...",
      "...",
      "..."
  ]
}}

Website Changes:

{diff_text}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except Exception:

            return {
                "summary": content,
                "severity": "Unknown",
                "confidence": 0.5,
                "changes": []
            }