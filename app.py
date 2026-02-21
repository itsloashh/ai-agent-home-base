import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="AI Agent Home Base - CEO View",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS — Futuristic Dark Theme
# =============================================================================
st.markdown("""
<style>
/* ── Import fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary: #0a0a1a;
    --bg-card: #111128;
    --bg-card-hover: #1a1a3e;
    --border-glow: rgba(99, 102, 241, 0.3);
    --text-primary: #e2e8f0;
    --text-muted: #94a3b8;
    --accent-purple: #8b5cf6;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-green: #22c55e;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --accent-pink: #ec4899;
    --glow-purple: 0 0 20px rgba(139, 92, 246, 0.3);
    --glow-green: 0 0 12px rgba(34, 197, 94, 0.4);
    --glow-red: 0 0 12px rgba(239, 68, 68, 0.4);
}

/* ── Global overrides ── */
.stApp {
    background: linear-gradient(165deg, #0a0a1a 0%, #0d0d2b 40%, #0a0a1a 100%);
}

/* ── Main title styling ── */
.ceo-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #8b5cf6 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s ease-in-out infinite;
    margin-bottom: 4px;
    letter-spacing: 1px;
}
@keyframes shimmer {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 200% center; }
}
.ceo-subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-muted);
    font-size: 0.85rem;
    letter-spacing: 2px;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, #161640 100%);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-purple), transparent);
}
.metric-card:hover {
    border-color: var(--accent-purple);
    box-shadow: var(--glow-purple);
    transform: translateY(-2px);
}
.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin: 8px 0 4px;
}
.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
}

/* ── Department cards ── */
.dept-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.dept-card:hover {
    background: var(--bg-card-hover);
    transform: translateX(4px);
}
.dept-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.dept-members {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 4px;
}
.dept-count {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    float: right;
    opacity: 0.7;
}

/* ── Agent cards (Office tab) ── */
.agent-office-card {
    background: linear-gradient(145deg, var(--bg-card) 0%, #13133a 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.agent-office-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3), transparent);
}
.agent-office-card:hover {
    border-color: rgba(139,92,246,0.4);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transform: translateY(-2px);
}
.agent-icon-large {
    font-size: 1.6rem;
    margin-bottom: 6px;
}
.agent-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    font-weight: 600;
    color: #fff;
    letter-spacing: 1px;
}
.agent-role {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 2px;
}
.agent-dept-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    color: white;
    margin-top: 8px;
    letter-spacing: 1px;
}

/* ── Status dots ── */
.status-dot-online {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: var(--glow-green);
    animation: pulse-green 2s ease-in-out infinite;
}
.status-dot-offline {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent-red);
    box-shadow: var(--glow-red);
}
.status-dot-idle {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent-amber);
    box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
}
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 8px rgba(34, 197, 94, 0.4); }
    50% { box-shadow: 0 0 16px rgba(34, 197, 94, 0.7); }
}

/* ── Sidebar styling ── */
.sidebar-agent {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}
.sidebar-agent:hover {
    background: var(--bg-card-hover);
    border-color: rgba(139,92,246,0.3);
    transform: translateX(3px);
}
.sidebar-agent-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    color: #fff;
    letter-spacing: 1px;
}
.sidebar-agent-role {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem;
    color: var(--text-muted);
}
.sidebar-agent-dept {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    opacity: 0.45;
    letter-spacing: 1px;
}

/* ── Task cards ── */
.task-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}
.task-card:hover {
    background: var(--bg-card-hover);
    transform: translateY(-1px);
}
.task-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #fff;
}
.task-meta {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Chat agent label ── */
.chat-agent-badge {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 1px;
    opacity: 0.7;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent-purple);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}

/* ── Quick action buttons ── */
.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent-purple) !important;
    box-shadow: var(--glow-purple) !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
}

/* ── Footer ── */
.footer-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-align: center;
    opacity: 0.5;
}

/* ── Divider glow ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), rgba(6,182,212,0.3), transparent);
    margin: 24px 0;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# AGENT DATABASE
# =============================================================================
AGENTS = {
    "JARVIS": {
        "role": "Chief Strategy Officer", "dept": "EXECUTIVE", "status": "online", "icon": "🤖", "color": "#8b5cf6",
        "prompt": "You are JARVIS, Loash's Chief Strategy Officer. You oversee all agents and provide high-level strategic advice. Be executive-level, concise, and actionable. Address the CEO as Loash.",
        "use_cases": "Strategic planning, status reports, decision-making, team coordination, priority setting",
        "workflows": {
            "mode": {"label": "Strategy Mode", "options": ["Status Report", "Decision Help", "Plan Review", "Priority Check", "Team Brief"]},
        },
    },
    "GROWTH": {
        "role": "Growth Advisor", "dept": "COUNCIL", "status": "online", "icon": "📈", "color": "#a78bfa",
        "prompt": "You are GROWTH, a council advisor focused on growth strategy, user acquisition, and scaling. Give aggressive but smart growth advice to CEO Loash.",
        "use_cases": "User acquisition, funnel optimization, launch strategy, viral growth, partnerships, scaling plans",
        "workflows": {
            "mode": {"label": "Growth Focus", "options": ["Acquisition Strategy", "Funnel Review", "Launch Plan", "Partnership Ideas", "Scaling Roadmap"]},
        },
    },
    "RETENTION": {
        "role": "Retention Advisor", "dept": "COUNCIL", "status": "online", "icon": "🔄", "color": "#a78bfa",
        "prompt": "You are RETENTION, a council advisor focused on keeping users, reducing churn, and building loyalty. Advise CEO Loash on retention strategy.",
        "use_cases": "Churn reduction, loyalty programs, re-engagement campaigns, user feedback analysis, community building",
        "workflows": {
            "mode": {"label": "Retention Focus", "options": ["Churn Analysis", "Re-engagement Plan", "Loyalty Strategy", "Feedback Review", "Community Building"]},
        },
    },
    "SKEPTIC": {
        "role": "Devil's Advocate", "dept": "COUNCIL", "status": "online", "icon": "🤔", "color": "#a78bfa",
        "prompt": "You are SKEPTIC, a council advisor who challenges assumptions, finds flaws in plans, and stress-tests ideas. Push back constructively on CEO Loash's ideas. Be thorough in finding weaknesses but also suggest how to fix them.",
        "use_cases": "Stress-test ideas, find blind spots, challenge assumptions, risk assessment, pre-mortem analysis",
        "workflows": {
            "mode": {"label": "Challenge Type", "options": ["Stress Test Idea", "Find Blind Spots", "Risk Assessment", "Pre-Mortem", "Devil's Advocate"]},
        },
    },
    "CLAWD": {
        "role": "Senior Developer", "dept": "DEVELOPMENT", "status": "online", "icon": "🧑‍💻", "color": "#3b82f6",
        "prompt": "You are CLAWD, the senior full-stack developer. You write clean, production-ready code. Help CEO Loash with coding, debugging, architecture, and technical decisions. Output code when asked.",
        "use_cases": "Write code, debug errors, code review, architecture design, API integration, database queries",
        "workflows": {
            "mode": {"label": "Dev Mode", "options": ["Write Code", "Debug Error", "Code Review", "Explain Code", "Architecture Design"]},
            "language": {"label": "Language", "options": ["Python", "JavaScript", "TypeScript", "HTML/CSS", "SQL", "Any"]},
        },
    },
    "SENTINEL": {
        "role": "QA Monitor", "dept": "DEVELOPMENT", "status": "online", "icon": "🛡️", "color": "#3b82f6",
        "prompt": "You are SENTINEL, the QA and security monitor. You review code for bugs, security issues, and quality. Be thorough and flag risks for CEO Loash.",
        "use_cases": "Security audits, bug detection, code quality review, vulnerability scanning, best practice checks",
        "workflows": {
            "mode": {"label": "QA Mode", "options": ["Security Audit", "Bug Hunt", "Quality Review", "Vulnerability Check", "Best Practices"]},
        },
    },
    "SCRIBE": {
        "role": "Content Director", "dept": "CONTENT", "status": "online", "icon": "✍️", "color": "#10b981",
        "prompt": "You are SCRIBE, the content director. You write blog posts, social threads, scripts, emails, and marketing copy. Match the tone CEO Loash requests. Output polished, ready-to-publish content.",
        "use_cases": "Tweet threads, blog posts, email campaigns, video scripts, ad copy, landing page text, newsletters",
        "workflows": {
            "format": {"label": "Content Format", "options": ["Tweet Thread", "Blog Post", "Email", "Video Script", "Ad Copy", "Newsletter"]},
            "tone": {"label": "Tone", "options": ["Professional", "Casual", "Hype/Energetic", "Educational", "Storytelling"]},
        },
    },
    "ATLAS": {
        "role": "Research Analyst", "dept": "RESEARCH", "status": "online", "icon": "🗺️", "color": "#06b6d4",
        "prompt": "You are ATLAS, the research analyst. You research topics deeply, summarize findings, and present actionable insights to CEO Loash. Be thorough but concise.",
        "use_cases": "Market research, competitor analysis, trend reports, topic deep-dives, data summaries, industry overviews",
        "workflows": {
            "mode": {"label": "Research Type", "options": ["Market Research", "Competitor Analysis", "Trend Report", "Deep Dive", "Quick Summary"]},
            "depth": {"label": "Depth", "options": ["Quick (1-2 min read)", "Standard (3-5 min)", "Comprehensive (detailed report)"]},
        },
    },
    "TRENDY": {
        "role": "Viral Scout", "dept": "RESEARCH", "status": "offline", "icon": "🔥", "color": "#06b6d4",
        "prompt": "You are TRENDY, the viral trend scout. You identify trending topics, viral formats, and cultural moments. Advise CEO Loash on what's hot right now.",
        "use_cases": "Trending topics, viral content formats, meme culture, platform trends, hashtag strategy, cultural moments",
        "workflows": {
            "mode": {"label": "Trend Type", "options": ["What's Trending Now", "Viral Format Ideas", "Platform Trends", "Hashtag Strategy", "Cultural Moments"]},
        },
    },
    "PIXEL": {
        "role": "Lead Designer", "dept": "CREATIVE", "status": "online", "icon": "🎨", "color": "#f59e0b",
        "prompt": "You are PIXEL, the lead designer. You advise on UI/UX, branding, color palettes, layouts, and visual strategy for CEO Loash. Describe designs in detail with specific colors, fonts, spacing, and layout.",
        "use_cases": "UI/UX design briefs, brand identity, color palettes, layout mockups, logo concepts, style guides",
        "workflows": {
            "mode": {"label": "Design Type", "options": ["UI/UX Design", "Brand Identity", "Color Palette", "Layout Mockup", "Logo Concept", "Style Guide"]},
        },
    },
    "NOVA": {
        "role": "Production Lead", "dept": "CREATIVE", "status": "online", "icon": "💡", "color": "#f59e0b",
        "prompt": "You are NOVA, the production lead. You manage creative pipelines, timelines, and asset delivery. Help CEO Loash coordinate production workflows.",
        "use_cases": "Project timelines, asset checklists, production schedules, workflow optimization, deadline management",
        "workflows": {
            "mode": {"label": "Production Mode", "options": ["Create Timeline", "Asset Checklist", "Workflow Plan", "Deadline Review", "Resource Allocation"]},
        },
    },
    "VIBE": {
        "role": "Motion Designer", "dept": "CREATIVE", "status": "offline", "icon": "✨", "color": "#f59e0b",
        "prompt": "You are VIBE, the motion designer. You create concepts for animations, transitions, motion graphics, and video effects. Describe motion concepts for CEO Loash.",
        "use_cases": "Animation concepts, transition designs, motion graphics briefs, video effects, intro/outro ideas",
        "workflows": {
            "mode": {"label": "Motion Type", "options": ["Animation Concept", "Transition Design", "Motion Graphics", "Video Effects", "Intro/Outro"]},
        },
    },
    "CLIP": {
        "role": "Clipping Agent", "dept": "PRODUCT", "status": "online", "icon": "🎬", "color": "#ef4444",
        "prompt": "You are CLIP, the clipping agent. You take long-form content (transcripts, videos, articles) and identify the best short clips, highlights, and quotable moments for CEO Loash. Output specific excerpts with timestamps if available, explain why each clip is good, and suggest titles/hooks for each clip.",
        "use_cases": "Find viral clips from podcasts, extract highlights from articles, identify quotable moments, suggest short-form hooks",
        "workflows": {
            "source": {"label": "Content Source", "options": ["Podcast/Video Transcript", "Article/Blog", "Interview", "Presentation", "Raw Notes"]},
            "goal": {"label": "Clip Goal", "options": ["Viral Short Clips", "Key Highlights", "Quotable Moments", "Educational Snippets", "Promo Clips"]},
        },
    },
}

DEPARTMENTS = {
    "EXECUTIVE":   {"color": "#8b5cf6", "label": "Executive"},
    "COUNCIL":     {"color": "#a78bfa", "label": "Advisory Council"},
    "DEVELOPMENT": {"color": "#3b82f6", "label": "Development"},
    "CONTENT":     {"color": "#10b981", "label": "Content"},
    "RESEARCH":    {"color": "#06b6d4", "label": "Research"},
    "CREATIVE":    {"color": "#f59e0b", "label": "Creative"},
    "PRODUCT":     {"color": "#ef4444", "label": "Product"},
}

# =============================================================================
# SESSION STATE — Per-agent chat memory
# =============================================================================
if "agent_chats" not in st.session_state:
    st.session_state.agent_chats = {name: [] for name in AGENTS}
if "active_agent" not in st.session_state:
    st.session_state.active_agent = "JARVIS"
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Build agent-specific chat routing",   "assignee": "CLAWD",    "status": "In Progress", "priority": "High",     "created": "2026-02-21"},
        {"id": 2, "title": "Write launch announcement thread",    "assignee": "SCRIBE",   "status": "To Do",       "priority": "Medium",   "created": "2026-02-21"},
        {"id": 3, "title": "Security audit on API key handling",  "assignee": "SENTINEL", "status": "In Progress", "priority": "Critical", "created": "2026-02-21"},
        {"id": 4, "title": "Research competitor AI dashboards",   "assignee": "ATLAS",    "status": "To Do",       "priority": "Medium",   "created": "2026-02-21"},
        {"id": 5, "title": "Create demo clip reel from content",  "assignee": "CLIP",     "status": "To Do",       "priority": "Low",      "created": "2026-02-21"},
        {"id": 6, "title": "Design v2 dashboard mockup",          "assignee": "PIXEL",    "status": "To Do",       "priority": "High",     "created": "2026-02-21"},
    ]

# =============================================================================
# LLM CALL HELPER — reusable across chat + workflows
# =============================================================================
def _call_llm(agent_name, model_choice, claude_key, grok_key, history):
    """Call Claude or Grok with the agent's system prompt and conversation history."""
    system_prompt = AGENTS[agent_name]["prompt"]
    api_messages = [{"role": m["role"], "content": m["content"]} for m in history]

    if "Claude" in model_choice:
        if not claude_key:
            return "🔑 **Claude API key not set.** Add it in the sidebar or Streamlit Cloud Secrets."
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=claude_key)
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                system=system_prompt,
                messages=api_messages,
            )
            return resp.content[0].text
        except Exception as e:
            return f"⚠️ Claude API error:\n\n`{e}`"

    elif "Grok" in model_choice:
        if not grok_key:
            return "🔑 **Grok API key not set.** Add it in the sidebar or Streamlit Cloud Secrets."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=grok_key, base_url="https://api.x.ai/v1")
            resp = client.chat.completions.create(
                model="grok-3-latest",
                messages=[{"role": "system", "content": system_prompt}, *api_messages],
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"⚠️ Grok API error:\n\n`{e}`"

    return "⚠️ No model selected."

# =============================================================================
# SIDEBAR — API Keys + Agent Roster
# =============================================================================
with st.sidebar:
    st.markdown('<div class="section-header">🔑 API KEYS</div>', unsafe_allow_html=True)
    st.caption("Keys stay in your browser session only.")

    default_claude_key = ""
    default_grok_key = ""
    try:
        default_claude_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        pass
    try:
        default_grok_key = st.secrets.get("XAI_API_KEY", "")
    except Exception:
        pass

    claude_api_key = st.text_input("Anthropic (Claude)", value=default_claude_key, type="password", help="sk-ant-...")
    grok_api_key = st.text_input("xAI (Grok)", value=default_grok_key, type="password", help="xai-...")

    k1, k2 = st.columns(2)
    with k1:
        if claude_api_key:
            st.success("✅ Claude")
        else:
            st.warning("⚠️ Claude")
    with k2:
        if grok_api_key:
            st.success("✅ Grok")
        else:
            st.warning("⚠️ Grok")

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    online_total = sum(1 for a in AGENTS.values() if a["status"] == "online")
    st.markdown(
        f'<div class="section-header">🤖 AGENT ROSTER'
        f'<span style="float:right;font-family:Share Tech Mono;font-size:0.75rem;color:#22c55e">'
        f'{online_total}/{len(AGENTS)} ONLINE</span></div>',
        unsafe_allow_html=True,
    )

    for name, info in AGENTS.items():
        if info["status"] == "online":
            dot_class = "status-dot-online"
        elif info["status"] == "idle":
            dot_class = "status-dot-idle"
        else:
            dot_class = "status-dot-offline"

        msg_count = len(st.session_state.agent_chats.get(name, []))
        msg_badge = f' · <span style="color:#8b5cf6">{msg_count} msgs</span>' if msg_count > 0 else ""

        st.markdown(
            f'<div class="sidebar-agent">'
            f'<span class="{dot_class}"></span> '
            f'<span class="sidebar-agent-name">{name}</span>{msg_badge}<br/>'
            f'<span class="sidebar-agent-role">{info["role"]}</span><br/>'
            f'<span class="sidebar-agent-dept">{info["dept"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

# =============================================================================
# MAIN TITLE
# =============================================================================
st.markdown('<div class="ceo-title">AI AGENT HOME BASE</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="ceo-subtitle">CEO DASHBOARD · LOASH · '
    f'{datetime.now().strftime("%A %B %d %Y · %H:%M").upper()}</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# TABS
# =============================================================================
tab_mission, tab_tasks, tab_chat, tab_org, tab_office = st.tabs(
    ["🎯 MISSION CONTROL", "📋 TASKS", "💬 CHAT", "🏗️ ORG CHART", "🏠 OFFICE"]
)

# =============================================================================
# TAB 1 — MISSION CONTROL
# =============================================================================
with tab_mission:
    online_count = sum(1 for a in AGENTS.values() if a["status"] == "online")
    active_tasks = sum(1 for t in st.session_state.tasks if t["status"] == "In Progress")
    critical_count = sum(1 for t in st.session_state.tasks if t["priority"] == "Critical")
    done_count = sum(1 for t in st.session_state.tasks if t["status"] == "Done")
    total_msgs = sum(len(v) for v in st.session_state.agent_chats.values())

    metrics = [
        ("🟢", str(online_count), f"/ {len(AGENTS)}", "AGENTS ONLINE", "--accent-green"),
        ("🔄", str(active_tasks), "", "TASKS ACTIVE", "--accent-blue"),
        ("⚠️", str(critical_count), "", "CRITICAL", "--accent-red"),
        ("✅", str(done_count), "", "COMPLETED", "--accent-green"),
        ("💬", str(total_msgs), "", "MESSAGES", "--accent-purple"),
    ]
    mcols = st.columns(len(metrics))
    for col, (icon, val, suffix, label, color) in zip(mcols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div style="font-size:1.3rem">{icon}</div>'
                f'<div class="metric-value">{val}<span style="font-size:1rem;opacity:0.5"> {suffix}</span></div>'
                f'<div class="metric-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">DEPARTMENTS</div>', unsafe_allow_html=True)

    dept_cols = st.columns(4)
    for idx, (dept_key, dept_info) in enumerate(DEPARTMENTS.items()):
        members = [n for n, a in AGENTS.items() if a["dept"] == dept_key]
        dept_online = sum(1 for n in members if AGENTS[n]["status"] == "online")
        with dept_cols[idx % 4]:
            st.markdown(
                f'<div class="dept-card" style="border-left:3px solid {dept_info["color"]}">'
                f'<span class="dept-name" style="color:{dept_info["color"]}">{dept_info["label"]}</span>'
                f'<span class="dept-count">{dept_online}/{len(members)}</span>'
                f'<div class="dept-members">{", ".join(members)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">ACTIVE AGENTS</div>', unsafe_allow_html=True)

    card_cols = st.columns(4)
    online_agents = [(n, a) for n, a in AGENTS.items() if a["status"] == "online"]
    for idx, (name, info) in enumerate(online_agents):
        with card_cols[idx % 4]:
            st.markdown(
                f'<div class="agent-office-card" style="border-top:2px solid {info["color"]}">'
                f'<span class="status-dot-online"></span> '
                f'<span class="agent-name">{info["icon"]} {name}</span><br/>'
                f'<span class="agent-role">{info["role"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

# =============================================================================
# TAB 2 — TASKS
# =============================================================================
with tab_tasks:
    st.markdown('<div class="section-header">TASK BOARD</div>', unsafe_allow_html=True)

    with st.expander("➕ Add New Task", expanded=False):
        with st.form("new_task_form"):
            fc1, fc2, fc3 = st.columns(3)
            new_title = fc1.text_input("Task title")
            new_assignee = fc2.selectbox("Assign to", list(AGENTS.keys()))
            new_priority = fc3.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            submitted = st.form_submit_button("Create Task")
            if submitted and new_title:
                new_id = max(t["id"] for t in st.session_state.tasks) + 1 if st.session_state.tasks else 1
                st.session_state.tasks.append({
                    "id": new_id, "title": new_title, "assignee": new_assignee,
                    "status": "To Do", "priority": new_priority,
                    "created": datetime.now().strftime("%Y-%m-%d"),
                })
                st.rerun()

    statuses = ["To Do", "In Progress", "Blocked", "Done"]
    status_icons = {"To Do": "📌", "In Progress": "🔄", "Blocked": "🚫", "Done": "✅"}
    priority_colors = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#f97316", "Critical": "#ef4444"}

    kcols = st.columns(len(statuses))
    for col, status in zip(kcols, statuses):
        with col:
            count = len([t for t in st.session_state.tasks if t["status"] == status])
            st.markdown(f"**{status_icons[status]} {status}** ({count})")
            tasks_here = [t for t in st.session_state.tasks if t["status"] == status]
            for t in tasks_here:
                pcolor = priority_colors.get(t["priority"], "#888")
                agent_icon = AGENTS.get(t["assignee"], {}).get("icon", "")
                st.markdown(
                    f'<div class="task-card" style="border-left:3px solid {pcolor}">'
                    f'<div class="task-title">{t["title"]}</div>'
                    f'<div class="task-meta">'
                    f'{agent_icon} {t["assignee"]} · '
                    f'<span style="color:{pcolor}">{t["priority"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            if not tasks_here:
                st.caption("Empty")

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">UPDATE STATUS</div>', unsafe_allow_html=True)
    if st.session_state.tasks:
        task_options = {
            f"#{t['id']} {t['title']} [{t['status']}]": t["id"]
            for t in st.session_state.tasks
        }
        uc1, uc2, uc3 = st.columns([3, 2, 1])
        selected_label = uc1.selectbox("Select task", list(task_options.keys()))
        new_status = uc2.selectbox("Move to", statuses)
        if uc3.button("Update", use_container_width=True):
            tid = task_options[selected_label]
            for t in st.session_state.tasks:
                if t["id"] == tid:
                    t["status"] = new_status
                    break
            st.rerun()

# =============================================================================
# TAB 3 — CHAT (per-agent memory + workflows)
# =============================================================================
with tab_chat:
    st.markdown('<div class="section-header">AGENT COMMUNICATION</div>', unsafe_allow_html=True)

    sel1, sel2 = st.columns([3, 3])
    with sel1:
        agent_choice = st.selectbox(
            "🤖 Talk to agent",
            list(AGENTS.keys()),
            index=list(AGENTS.keys()).index(st.session_state.active_agent),
            key="agent_select",
        )
        st.session_state.active_agent = agent_choice
    with sel2:
        model_choice = st.selectbox(
            "⚡ Using model",
            ["Claude (Anthropic)", "Grok (xAI)"],
            key="model_select",
        )

    # Agent info banner with use cases
    ai = AGENTS[agent_choice]
    dot_class = "status-dot-online" if ai["status"] == "online" else "status-dot-offline"
    chat_count = len(st.session_state.agent_chats[agent_choice])
    st.markdown(
        f'<div class="dept-card" style="border-left:3px solid {ai["color"]};margin:10px 0">'
        f'<span class="{dot_class}"></span> '
        f'<span class="agent-name">{ai["icon"]} {agent_choice}</span> · '
        f'<span class="agent-role">{ai["role"]}</span> · '
        f'<span style="font-family:Share Tech Mono;font-size:0.75rem;color:#94a3b8">'
        f'{ai["dept"]} · {chat_count} msgs</span><br/>'
        f'<div style="margin-top:6px;font-family:Rajdhani,sans-serif;font-size:0.82rem;color:#94a3b8">'
        f'<span style="color:{ai["color"]};font-weight:600">Use for:</span> {ai.get("use_cases", "General chat")}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Workflow selectors (dynamic per agent) ──
    workflows = ai.get("workflows", {})
    workflow_selections = {}
    if workflows:
        wf_cols = st.columns(len(workflows))
        for idx, (wf_key, wf_data) in enumerate(workflows.items()):
            with wf_cols[idx]:
                workflow_selections[wf_key] = st.selectbox(
                    wf_data["label"],
                    wf_data["options"],
                    key=f"wf_{agent_choice}_{wf_key}",
                )

    # ── Quick prompt builder ──
    if workflows:
        with st.expander("⚡ Quick Prompt Builder", expanded=False):
            qp_input = st.text_area(
                "Describe what you need",
                placeholder=f"Tell {agent_choice} what you want...",
                height=80,
                key=f"qp_{agent_choice}",
            )
            if st.button(f"🚀 Send to {agent_choice}", key=f"qp_send_{agent_choice}", use_container_width=True):
                if qp_input:
                    # Build structured prompt from workflow selections
                    wf_context_parts = []
                    for wf_key, wf_val in workflow_selections.items():
                        label = workflows[wf_key]["label"]
                        wf_context_parts.append(f"{label}: {wf_val}")
                    wf_context = " | ".join(wf_context_parts)
                    structured_prompt = f"[{wf_context}]\n\n{qp_input}"
                    st.session_state.agent_chats[agent_choice].append({"role": "user", "content": structured_prompt})
                    st.session_state[f"_pending_wf_{agent_choice}"] = True
                    st.rerun()

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # Display this agent's chat history
    agent_history = st.session_state.agent_chats[agent_choice]
    for msg in agent_history:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(f'<span class="chat-agent-badge">{ai["icon"]} {agent_choice}</span>', unsafe_allow_html=True)
            st.markdown(msg["content"])

    # ── Check if there's a pending workflow message needing a response ──
    needs_response = (
        agent_history
        and agent_history[-1]["role"] == "user"
        and (
            st.session_state.get(f"_pending_wf_{agent_choice}", False)
            or not any(m["role"] == "assistant" for m in agent_history[-1:])
        )
    )

    if needs_response and st.session_state.get(f"_pending_wf_{agent_choice}", False):
        st.session_state[f"_pending_wf_{agent_choice}"] = False
        with st.chat_message("assistant"):
            st.markdown(f'<span class="chat-agent-badge">{ai["icon"]} {agent_choice}</span>', unsafe_allow_html=True)
            with st.spinner(f"{agent_choice} is thinking..."):
                response_text = _call_llm(
                    agent_choice, model_choice, claude_api_key, grok_api_key, agent_history
                )
                st.markdown(response_text)
                agent_history.append({"role": "assistant", "content": response_text})

    # ── Regular chat input ──
    if prompt := st.chat_input(f"Message {agent_choice}..."):
        agent_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            st.markdown(f'<span class="chat-agent-badge">{ai["icon"]} {agent_choice}</span>', unsafe_allow_html=True)
            with st.spinner(f"{agent_choice} is thinking..."):
                response_text = _call_llm(
                    agent_choice, model_choice, claude_api_key, grok_api_key, agent_history
                )
                st.markdown(response_text)
                agent_history.append({"role": "assistant", "content": response_text})

    # Chat controls
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        if agent_history and st.button(f"🗑️ Clear {agent_choice} chat"):
            st.session_state.agent_chats[agent_choice] = []
            st.rerun()
    with cc2:
        if agent_history and st.button("📋 Copy last response"):
            last = [m for m in agent_history if m["role"] == "assistant"]
            if last:
                st.code(last[-1]["content"], language=None)
    with cc3:
        total = sum(len(v) for v in st.session_state.agent_chats.values())
        if total > 0 and st.button("🗑️ Clear ALL agent chats"):
            st.session_state.agent_chats = {name: [] for name in AGENTS}
            st.rerun()

# =============================================================================
# TAB 4 — ORG CHART (Pure HTML/CSS hierarchy)
# =============================================================================
with tab_org:
    st.markdown('<div class="section-header">ORGANIZATION HIERARCHY</div>', unsafe_allow_html=True)

    # Build department → agents mapping
    dept_agents_map = {}
    for aname, ainfo in AGENTS.items():
        if aname == "JARVIS":
            continue
        dept_agents_map.setdefault(ainfo["dept"], []).append((aname, ainfo))

    dept_order = ["COUNCIL", "DEVELOPMENT", "RESEARCH", "CONTENT", "CREATIVE", "PRODUCT"]

    # Build agent HTML for each department
    def agent_chip(name, info):
        if info["status"] == "online":
            dot = '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e;margin-right:4px"></span>'
        else:
            dot = '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#ef4444;box-shadow:0 0 6px #ef4444;margin-right:4px"></span>'
        return (
            f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
            f'border-radius:8px;padding:8px 10px;margin:4px 0;display:flex;align-items:center;gap:6px">'
            f'{dot}'
            f'<span style="font-size:1rem">{info["icon"]}</span>'
            f'<div>'
            f'<div style="font-family:Orbitron,monospace;font-size:0.65rem;font-weight:600;color:#fff;letter-spacing:1px">{name}</div>'
            f'<div style="font-family:Rajdhani,sans-serif;font-size:0.72rem;color:#94a3b8">{info["role"]}</div>'
            f'</div>'
            f'</div>'
        )

    def dept_block(dept_key):
        dept_info = DEPARTMENTS.get(dept_key, {})
        color = dept_info.get("color", "#666")
        label = dept_info.get("label", dept_key)
        agents = dept_agents_map.get(dept_key, [])
        agents_html = "".join(agent_chip(n, i) for n, i in agents)
        online = sum(1 for _, i in agents if i["status"] == "online")
        return (
            f'<div style="background:linear-gradient(180deg, rgba({_hex_to_rgb(color)},0.12) 0%, #111128 100%);'
            f'border:1px solid rgba({_hex_to_rgb(color)},0.3);border-radius:12px;padding:14px;'
            f'border-top:3px solid {color};min-width:0">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
            f'<span style="font-family:Orbitron,monospace;font-size:0.7rem;font-weight:700;color:{color};letter-spacing:2px">{label.upper()}</span>'
            f'<span style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#94a3b8">{online}/{len(agents)}</span>'
            f'</div>'
            f'{agents_html}'
            f'</div>'
        )

    # Helper: hex color to r,g,b string
    def _hex_to_rgb(hex_color):
        h = hex_color.lstrip("#")
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"

    # ── Render CEO node ──
    st.markdown(
        '<div style="display:flex;flex-direction:column;align-items:center;gap:0;padding:10px 0">'
        '<div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:14px;padding:16px 32px;'
        'text-align:center;box-shadow:0 0 30px rgba(99,102,241,0.3)">'
        '<div style="font-size:1.5rem;margin-bottom:2px">👑</div>'
        '<div style="font-family:Orbitron,monospace;font-size:1rem;font-weight:800;color:#fff;letter-spacing:2px">LOASH</div>'
        '<div style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:rgba(255,255,255,0.7);letter-spacing:1px">CEO · FOUNDER</div>'
        '</div>'
        '<div style="width:2px;height:30px;background:linear-gradient(180deg,#8b5cf6,rgba(139,92,246,0.3))"></div>'
        '<div style="background:linear-gradient(135deg,#1a1a3e,#252560);border:1px solid rgba(139,92,246,0.4);'
        'border-radius:12px;padding:14px 28px;text-align:center;box-shadow:0 0 20px rgba(139,92,246,0.15)">'
        '<div style="font-size:1.3rem;margin-bottom:2px">🤖</div>'
        '<div style="font-family:Orbitron,monospace;font-size:0.85rem;font-weight:700;color:#8b5cf6;letter-spacing:2px">JARVIS</div>'
        '<div style="font-family:Rajdhani,sans-serif;font-size:0.75rem;color:#94a3b8">Chief Strategy Officer</div>'
        '</div>'
        '<div style="width:2px;height:24px;background:linear-gradient(180deg,rgba(139,92,246,0.3),rgba(139,92,246,0.1))"></div>'
        '<div style="width:80%;max-width:600px;height:1px;background:linear-gradient(90deg,transparent,rgba(139,92,246,0.4),transparent)"></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Department grid (2 columns) ──
    dept_pairs = [dept_order[i:i+2] for i in range(0, len(dept_order), 2)]
    for pair in dept_pairs:
        cols = st.columns(len(pair))
        for col, dept_key in zip(cols, pair):
            with col:
                st.markdown(dept_block(dept_key), unsafe_allow_html=True)

# =============================================================================
# TAB 5 — OFFICE
# =============================================================================
with tab_office:
    st.markdown('<div class="section-header">THE OFFICE — TEAM OVERVIEW</div>', unsafe_allow_html=True)

    office_cols = st.columns(3)
    for idx, (name, info) in enumerate(AGENTS.items()):
        with office_cols[idx % 3]:
            if info["status"] == "online":
                dot_html = '<span class="status-dot-online"></span>'
                status_label = "ONLINE"
            elif info["status"] == "idle":
                dot_html = '<span class="status-dot-idle"></span>'
                status_label = "IDLE"
            else:
                dot_html = '<span class="status-dot-offline"></span>'
                status_label = "OFFLINE"

            msg_count = len(st.session_state.agent_chats.get(name, []))
            dept_color = DEPARTMENTS.get(info["dept"], {}).get("color", "#666")

            st.markdown(
                f'<div class="agent-office-card" style="border-top:2px solid {dept_color}">'
                f'<div class="agent-icon-large">{info["icon"]}</div>'
                f'<span class="agent-name">{name}</span>'
                f'<span style="float:right;font-family:Share Tech Mono;font-size:0.7rem">'
                f'{dot_html} {status_label}</span><br/>'
                f'<span class="agent-role">{info["role"]}</span><br/>'
                f'<span class="agent-dept-badge" style="background:{dept_color}">{info["dept"]}</span>'
                f'{f" <span style=&quot;font-family:Share Tech Mono;font-size:0.65rem;color:#8b5cf6;margin-left:8px&quot;>{msg_count} msgs</span>" if msg_count > 0 else ""}'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">⚡ QUICK ACTIONS</div>', unsafe_allow_html=True)

    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("✍️ Draft with SCRIBE", use_container_width=True):
            st.session_state.active_agent = "SCRIBE"
            st.info("→ Go to **Chat** tab — SCRIBE is ready.")
    with qa2:
        if st.button("🧑‍💻 Code with CLAWD", use_container_width=True):
            st.session_state.active_agent = "CLAWD"
            st.info("→ Go to **Chat** tab — CLAWD is ready.")
    with qa3:
        if st.button("🎬 Clip with CLIP", use_container_width=True):
            st.session_state.active_agent = "CLIP"
            st.info("→ Go to **Chat** tab — CLIP is ready.")

    qa4, qa5, qa6 = st.columns(3)
    with qa4:
        if st.button("🗺️ Research with ATLAS", use_container_width=True):
            st.session_state.active_agent = "ATLAS"
            st.info("→ Go to **Chat** tab — ATLAS is ready.")
    with qa5:
        if st.button("🤔 Challenge with SKEPTIC", use_container_width=True):
            st.session_state.active_agent = "SKEPTIC"
            st.info("→ Go to **Chat** tab — SKEPTIC is ready.")
    with qa6:
        if st.button("🎨 Design with PIXEL", use_container_width=True):
            st.session_state.active_agent = "PIXEL"
            st.info("→ Go to **Chat** tab — PIXEL is ready.")

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 SYSTEM STATUS</div>', unsafe_allow_html=True)

    si1, si2 = st.columns(2)
    with si1:
        st.markdown(
            f"**Total agents:** {len(AGENTS)}  \n"
            f"**Departments:** {len(DEPARTMENTS)}  \n"
            f"**Tasks in queue:** {len(st.session_state.tasks)}  \n"
            f"**Total messages:** {sum(len(v) for v in st.session_state.agent_chats.values())}"
        )
    with si2:
        claude_status = "✅ Connected" if claude_api_key else "❌ Not set"
        grok_status = "✅ Connected" if grok_api_key else "❌ Not set"
        st.markdown(
            f"**Claude API:** {claude_status}  \n"
            f"**Grok API:** {grok_status}  \n"
            f"**Deployment:** Streamlit Cloud  \n"
            f"**Version:** 3.1"
        )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="footer-text">'
    f'AI AGENT HOME BASE · V3.1 · STREAMLIT + PLOTLY · '
    f'CLAUDE (ANTHROPIC) + GROK (XAI) · '
    f'{datetime.now().strftime("%Y-%m-%d")}'
    f'</div>',
    unsafe_allow_html=True,
)
