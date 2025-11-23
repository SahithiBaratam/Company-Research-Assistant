import os
import requests
from typing import List, Dict

from dotenv import load_dotenv
from prompts import CHAT_SYSTEM_PROMPT, PLAN_SYSTEM_PROMPT
from web_researcher import ddg_company_research

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"



     


def groq_chat(prompt: str) -> str:
    """
    Call the Groq API Chat Completion endpoint.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 800
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return f"[GROQ ERROR] {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]


class CompanyResearchAgent:

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY missing in .env!")

        self.chat_history: List[Dict[str, str]] = [
            {"role": "system", "content": CHAT_SYSTEM_PROMPT}
        ]

        self.account_plan_markdown = ""
        self.last_research_context = ""

    def _build_prompt(self):
        text = ""
        for msg in self.chat_history:
            if msg["role"] == "system":
                text += f"[SYSTEM]\n{msg['content']}\n\n"
            elif msg["role"] == "user":
                text += f"[USER]\n{msg['content']}\n\n"
            elif msg["role"] == "assistant":
                text += f"[ASSISTANT]\n{msg['content']}\n\n"

        text += "[ASSISTANT]\n"
        return text

    def chat(self, user_message: str) -> str:
        self.chat_history.append({"role": "user", "content": user_message})
        prompt = self._build_prompt()
        reply = groq_chat(prompt)
        self.chat_history.append({"role": "assistant", "content": reply})
        return reply

    def research_company_with_ddg(self, company_name: str, keywords: str = "") -> str:
        raw = ddg_company_research(company_name, keywords)
        self.last_research_context = raw

        summary_prompt = f"""
[SYSTEM] Summarize online research for account planning.

[USER]
Summarize these DuckDuckGo results about {company_name}:

{raw}

Focus on:
- Company background
- Products & services
- Regions
- News / updates
- Useful insights
[ASSISTANT]
"""

        summary = groq_chat(summary_prompt)

        self.chat_history.append({
            "role": "user",
            "content": f"(Web Research Summary):\n{summary}"
        })

        return summary

    def generate_account_plan(self) -> str:
        summary = self._summarize_conversation()

        prompt = f"""
[SYSTEM]
{PLAN_SYSTEM_PROMPT}

[USER]
Create a complete Markdown Account Plan using this summary:

{summary}

[ASSISTANT]
"""

        plan = groq_chat(prompt)
        self.account_plan_markdown = plan
        return plan

    def update_account_plan(self, section_name: str, user_instruction: str) -> str:
        prompt = f"""
[SYSTEM] {PLAN_SYSTEM_PROMPT}

[USER]
Here is the current account plan:

{self.account_plan_markdown}

Update ONLY this section: {section_name}

Apply these changes:
{user_instruction}

Return FULL updated Markdown plan.

[ASSISTANT]
"""

        updated = groq_chat(prompt)
        self.account_plan_markdown = updated
        return updated

    def _summarize_conversation(self) -> str:
        text = ""
        for msg in self.chat_history:
            if msg["role"] == "user":
                text += f"User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                text += f"Assistant: {msg['content']}\n"

        prompt = f"""
[SYSTEM] Summarize this conversation for account planning.

[USER]
{text}

[ASSISTANT]
"""

        return groq_chat(prompt)
