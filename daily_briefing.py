"""
Daily Briefing Script — Runs via GitHub Actions at 10pm daily.
Calls Claude API to generate a briefing, sends it to Telegram.
Completely independent from app.py.
"""
import os
import requests
import anthropic
from datetime import datetime

# ── Config from GitHub Secrets ──
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ── Agent roster (mirrors app.py) ──
AGENTS = {
    "JARVIS": "Chief Strategy Officer (EXECUTIVE)",
    "GROWTH": "Growth Advisor (COUNCIL)",
    "RETENTION": "Retention Advisor (COUNCIL)",
    "SKEPTIC": "Devil's Advocate (COUNCIL)",
    "CLAWD": "Senior Developer (DEVELOPMENT)",
    "SENTINEL": "QA Monitor (DEVELOPMENT)",
    "SCRIBE": "Content Director (CONTENT)",
    "ATLAS": "Research Analyst (RESEARCH)",
    "TRENDY": "Viral Scout (RESEARCH) — OFFLINE",
    "PIXEL": "Lead Designer (CREATIVE)",
    "NOVA": "Production Lead (CREATIVE)",
    "VIBE": "Motion Designer (CREATIVE) — OFFLINE",
    "CLIP": "Clipping Agent (PRODUCT)",
}


def generate_briefing():
    """Generate daily briefing via Claude."""
    now = datetime.now()
    prompt = (
        f"You are JARVIS, Chief Strategy Officer for CEO Loash's AI Agent Home Base.\n\n"
        f"Generate a daily executive briefing for {now.strftime('%A, %B %d %Y')}.\n\n"
        f"TEAM STATUS:\n"
        f"- 11/13 agents online (TRENDY and VIBE are offline)\n"
        f"- Departments: Executive, Advisory Council, Development, Content, Research, Creative, Product\n"
        f"- Full roster: {', '.join(AGENTS.keys())}\n\n"
        f"Generate a concise daily briefing with:\n"
        f"1. 🟢 STATUS — Quick team snapshot\n"
        f"2. 🎯 PRIORITIES — What CEO should focus on today\n"
        f"3. 💡 RECOMMENDATIONS — Strategic suggestions\n"
        f"4. ⚠️ WATCH LIST — Risks or items needing attention\n\n"
        f"Keep it concise and actionable. Use emoji for readability. "
        f"Address the CEO as Loash. This will be sent via Telegram so keep formatting clean."
    )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are JARVIS, the Chief Strategy Officer. Generate executive briefings.",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def send_telegram(message):
    """Send message to Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # Telegram has a 4096 char limit per message
    header = f"🏢 *AI AGENT HOME BASE*\n📋 *Daily Briefing — {datetime.now().strftime('%B %d, %Y')}*\n{'─' * 30}\n\n"
    full_message = header + message

    # Split if too long
    chunks = []
    while len(full_message) > 4000:
        split_at = full_message.rfind("\n", 0, 4000)
        if split_at == -1:
            split_at = 4000
        chunks.append(full_message[:split_at])
        full_message = full_message[split_at:]
    chunks.append(full_message)

    for chunk in chunks:
        resp = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
        })
        if not resp.ok:
            # Retry without markdown if parsing fails
            requests.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": chunk,
            })


if __name__ == "__main__":
    print("Generating daily briefing...")
    briefing = generate_briefing()
    print("Sending to Telegram...")
    send_telegram(briefing)
    print("Done!")
