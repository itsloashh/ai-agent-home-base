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
# PASSWORD GATE — protects the entire app
# =============================================================================
def check_password():
    """Returns True if the user has entered the correct password."""
    correct_pw = ""
    try:
        correct_pw = st.secrets.get("APP_PASSWORD", "")
    except Exception:
        pass

    if not correct_pw:
        # No password set in secrets — skip gate
        return True

    if st.session_state.get("authenticated", False):
        return True

    st.markdown(
        '<div style="display:flex;flex-direction:column;align-items:center;'
        'justify-content:center;min-height:60vh;text-align:center">'
        '<div style="font-size:3rem;margin-bottom:10px">🏢</div>'
        '<div style="font-family:Orbitron,monospace;font-size:1.5rem;font-weight:800;'
        'background:linear-gradient(135deg,#8b5cf6,#06b6d4);-webkit-background-clip:text;'
        '-webkit-text-fill-color:transparent;margin-bottom:4px">AI AGENT HOME BASE</div>'
        '<div style="font-family:Share Tech Mono,monospace;font-size:0.8rem;color:#94a3b8;'
        'letter-spacing:2px;margin-bottom:30px">CEO ACCESS REQUIRED</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    password = st.text_input("Enter password", type="password", key="pw_input")
    if st.button("🔓 Unlock", use_container_width=True):
        if password == correct_pw:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect password.")
    return False

if not check_password():
    st.stop()

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
    "EXECUTIVE": {
        "color": "#8b5cf6", "label": "Executive",
        "mission": "High-level strategy, team coordination, and decision-making for the entire organization.",
        "examples": "Weekly strategy reviews, OKR planning, cross-team coordination, investor updates, priority decisions",
    },
    "COUNCIL": {
        "color": "#a78bfa", "label": "Advisory Council",
        "mission": "Provide diverse strategic perspectives — growth, retention, and critical analysis to stress-test every decision.",
        "examples": "Pitch deck review, go-to-market critique, growth experiments, churn analysis, idea validation",
    },
    "DEVELOPMENT": {
        "color": "#3b82f6", "label": "Development",
        "mission": "Build, ship, and secure all technical products. Code quality, architecture, and security.",
        "examples": "Feature development, bug fixes, API integrations, security audits, code reviews, database optimization",
    },
    "CONTENT": {
        "color": "#10b981", "label": "Content",
        "mission": "Create all written content — social, blog, email, scripts — that drives engagement and brand voice.",
        "examples": "Twitter threads, blog series, email sequences, YouTube scripts, ad copy, press releases, newsletters",
    },
    "RESEARCH": {
        "color": "#06b6d4", "label": "Research",
        "mission": "Deep research, trend analysis, and competitive intelligence to inform strategy.",
        "examples": "Competitor teardowns, market sizing, trend reports, user research summaries, industry analysis",
    },
    "CREATIVE": {
        "color": "#f59e0b", "label": "Creative",
        "mission": "Design, visual identity, motion, and production pipeline for all creative assets.",
        "examples": "UI mockups, brand guidelines, logo concepts, animation briefs, video storyboards, asset production timelines",
    },
    "PRODUCT": {
        "color": "#ef4444", "label": "Product",
        "mission": "Content repurposing, clip extraction, and maximizing the value of every piece of content produced.",
        "examples": "Podcast clip extraction, highlight reels, quote cards, short-form video hooks, content atomization",
    },
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
        {"id": 1, "title": "Build agent-specific chat routing",   "assignee": "CLAWD",    "status": "In Progress", "priority": "High",     "created": "2026-02-21", "description": "Implement per-agent chat memory and routing so each agent has its own conversation thread.", "result": ""},
        {"id": 2, "title": "Write launch announcement thread",    "assignee": "SCRIBE",   "status": "To Do",       "priority": "Medium",   "created": "2026-02-21", "description": "Create a Twitter/X thread announcing the AI Agent Home Base dashboard launch.", "result": ""},
        {"id": 3, "title": "Security audit on API key handling",  "assignee": "SENTINEL", "status": "In Progress", "priority": "Critical", "created": "2026-02-21", "description": "Review how API keys are stored, transmitted, and used. Flag any vulnerabilities.", "result": ""},
        {"id": 4, "title": "Research competitor AI dashboards",   "assignee": "ATLAS",    "status": "To Do",       "priority": "Medium",   "created": "2026-02-21", "description": "Find and analyze 5-10 competitor AI agent dashboard products. Summarize features, pricing, and gaps.", "result": ""},
        {"id": 5, "title": "Create demo clip reel from content",  "assignee": "CLIP",     "status": "To Do",       "priority": "Low",      "created": "2026-02-21", "description": "Take our existing content and identify the best 5-10 short clips for social media promotion.", "result": ""},
        {"id": 6, "title": "Design v2 dashboard mockup",          "assignee": "PIXEL",    "status": "To Do",       "priority": "High",     "created": "2026-02-21", "description": "Design a polished v2 mockup for the CEO dashboard with improved layout and visual hierarchy.", "result": ""},
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
# AUTO-ROUTE — Analyze message and pick the best agent
# =============================================================================
ROUTING_KEYWORDS = {
    "JARVIS": ["strategy", "prioritize", "plan", "team", "overview", "coordinate", "decision", "direction", "roadmap", "delegate", "status", "okr", "kpi"],
    "GROWTH": ["grow", "acquire", "users", "scale", "launch", "funnel", "viral", "marketing", "audience", "traffic", "conversion", "signup"],
    "RETENTION": ["retain", "churn", "loyalty", "engagement", "community", "feedback", "onboarding", "activation", "nps"],
    "SKEPTIC": ["risk", "flaw", "problem", "challenge", "wrong", "fail", "weakness", "concern", "doubt", "critique", "bad idea", "devil"],
    "CLAWD": ["code", "build", "develop", "api", "bug", "debug", "program", "script", "database", "deploy", "function", "backend", "frontend", "python", "javascript", "app"],
    "SENTINEL": ["security", "audit", "vulnerability", "hack", "protect", "review code", "test", "qa", "quality"],
    "SCRIBE": ["write", "blog", "tweet", "thread", "email", "copy", "content", "article", "script", "newsletter", "announcement", "post", "caption"],
    "ATLAS": ["research", "analyze", "competitor", "market", "data", "report", "industry", "trend", "compare", "study", "deep dive"],
    "TRENDY": ["trending", "viral", "meme", "tiktok", "culture", "hashtag", "what's hot", "popular"],
    "PIXEL": ["design", "ui", "ux", "layout", "color", "brand", "logo", "mockup", "visual", "style", "font", "aesthetic"],
    "NOVA": ["timeline", "schedule", "deadline", "production", "asset", "pipeline", "workflow", "project manage"],
    "VIBE": ["animation", "motion", "video", "transition", "intro", "outro", "effect"],
    "CLIP": ["clip", "highlight", "excerpt", "cut", "short-form", "repurpose", "podcast", "transcript", "quote"],
}

def _auto_route(message):
    """Analyze a message and return the best agent + reasoning."""
    msg_lower = message.lower()
    scores = {}
    for agent_name, keywords in ROUTING_KEYWORDS.items():
        score = 0
        matched = []
        for kw in keywords:
            if kw in msg_lower:
                score += 1
                matched.append(kw)
        if score > 0:
            scores[agent_name] = {"score": score, "matched": matched}

    if not scores:
        # Default to JARVIS for general/unclear messages
        return "JARVIS", "No specific domain detected — routing to JARVIS as your Chief Strategy Officer for general guidance."

    # Get the top match
    best = max(scores.items(), key=lambda x: x["score"])
    agent_name = best[0]
    matched_kws = best[1]["matched"]
    agent_info = AGENTS[agent_name]

    # Check for ties or close seconds — mention them
    sorted_scores = sorted(scores.items(), key=lambda x: x["score"], reverse=True)
    reasoning = (
        f"Detected keywords: **{', '.join(matched_kws)}** → "
        f"Best match is **{agent_name}** ({agent_info['role']})"
    )
    if len(sorted_scores) > 1 and sorted_scores[1][1]["score"] == sorted_scores[0][1]["score"]:
        alt = sorted_scores[1][0]
        reasoning += f" (also considered **{alt}**)"

    return agent_name, reasoning

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
tab_jarvis, tab_mission, tab_tasks, tab_chat, tab_org, tab_office = st.tabs(
    ["🎙️ JARVIS", "🎯 MISSION CONTROL", "📋 TASKS", "💬 CHAT", "🏗️ ORG CHART", "🏠 OFFICE"]
)

# =============================================================================
# TAB 0 — JARVIS (CEO Command Center)
# =============================================================================
with tab_jarvis:
    if "jarvis_chat" not in st.session_state:
        st.session_state.jarvis_chat = []
    if "jarvis_voice_enabled" not in st.session_state:
        st.session_state.jarvis_voice_enabled = True

    # ── Arc Reactor visual ──
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    .jr-wrap{display:flex;flex-direction:column;align-items:center;padding:10px 0}
    .jr-reactor{position:relative;width:150px;height:150px;display:flex;align-items:center;justify-content:center}
    .jr-glow{position:absolute;width:160px;height:160px;border-radius:50%;
        background:radial-gradient(circle,rgba(6,182,212,0.08) 0%,transparent 70%);
        animation:jrPulse 3s ease-in-out infinite}
    .jr-r1{position:absolute;width:150px;height:150px;border-radius:50%;
        border:2px solid rgba(6,182,212,0.3);animation:jrSpin 8s linear infinite}
    .jr-r1::before{content:'';position:absolute;top:-2px;left:50%;width:7px;height:7px;
        background:#06b6d4;border-radius:50%;transform:translateX(-50%);box-shadow:0 0 10px #06b6d4}
    .jr-r2{position:absolute;width:115px;height:115px;border-radius:50%;
        border:1.5px solid rgba(139,92,246,0.4);animation:jrSpin 5s linear infinite reverse}
    .jr-r2::before{content:'';position:absolute;bottom:-2px;left:50%;width:5px;height:5px;
        background:#8b5cf6;border-radius:50%;transform:translateX(-50%);box-shadow:0 0 8px #8b5cf6}
    .jr-r3{position:absolute;width:80px;height:80px;border-radius:50%;
        border:1px solid rgba(6,182,212,0.25);animation:jrSpin 3s linear infinite}
    .jr-core{width:50px;height:50px;border-radius:50%;z-index:2;
        background:radial-gradient(circle,rgba(6,182,212,0.25) 0%,transparent 70%);
        display:flex;align-items:center;justify-content:center;
        animation:jrCorePulse 2.5s ease-in-out infinite}
    .jr-core-dot{width:20px;height:20px;border-radius:50%;
        background:radial-gradient(circle,rgba(6,182,212,0.6),rgba(139,92,246,0.2));
        box-shadow:0 0 12px rgba(6,182,212,0.3)}
    .jr-title{font-family:'Orbitron',monospace;font-size:1.2rem;font-weight:900;
        background:linear-gradient(135deg,#06b6d4,#8b5cf6);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        letter-spacing:4px;margin-top:12px}
    .jr-sub{font-family:'Share Tech Mono',monospace;font-size:0.65rem;
        color:#64748b;letter-spacing:2px;margin-top:2px}
    @keyframes jrSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
    @keyframes jrPulse{0%,100%{transform:scale(1);opacity:.5}50%{transform:scale(1.08);opacity:.8}}
    @keyframes jrCorePulse{0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(1.12);opacity:1}}
    </style>
    <div class="jr-wrap">
        <div class="jr-reactor">
            <div class="jr-glow"></div><div class="jr-r1"></div>
            <div class="jr-r2"></div><div class="jr-r3"></div>
            <div class="jr-core"><div class="jr-core-dot"></div></div>
        </div>
        <div class="jr-title">J.A.R.V.I.S.</div>
        <div class="jr-sub">CHIEF STRATEGY OFFICER · VOICE ENABLED</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls ──
    jv1, jv2, jv3 = st.columns([2, 2, 2])
    with jv1:
        st.session_state.jarvis_voice_enabled = st.toggle(
            "🔊 Voice Output", value=st.session_state.jarvis_voice_enabled, key="voice_toggle"
        )
    with jv2:
        jarvis_model = st.selectbox("Model", ["Claude (Anthropic)", "Grok (xAI)"], key="jarvis_model")
    with jv3:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.jarvis_chat = []
            st.rerun()

    # ── Mic Button (PC + Mobile) ──
    from streamlit_mic_recorder import speech_to_text
    mic1, mic2, mic3 = st.columns([1, 2, 1])
    with mic2:
        voice_text = speech_to_text(
            language="en",
            start_prompt="🎙️  TAP TO TALK",
            stop_prompt="⏹️  SEND TO JARVIS",
            just_once=True,
            use_container_width=True,
            key="jarvis_stt",
        )
    if voice_text:
        st.session_state.jarvis_chat.append({"role": "user", "content": voice_text})
        st.rerun()

    # ── JARVIS System Prompt ──
    jarvis_system = (
        "You are J.A.R.V.I.S., the Chief Strategy Officer and personal AI assistant for CEO Loash. "
        "You are voice-enabled, so keep responses conversational and concise — like you're speaking to Loash directly. "
        "You have 12 agents under your command across 7 departments: "
        "GROWTH, RETENTION, SKEPTIC (Advisory Council), CLAWD, SENTINEL (Development), "
        "SCRIBE (Content), ATLAS, TRENDY (Research), PIXEL, NOVA, VIBE (Creative), CLIP (Product).\n\n"
        "CAPABILITIES:\n"
        "1. Strategic advice and decision-making\n"
        "2. Delegate tasks — tell Loash which agent to use and why\n"
        "3. App & tool recommendations — recommend BEST FREE options: Canva (design), Figma (UI/UX), "
        "CapCut (video), DaVinci Resolve (pro video), OBS (streaming), Notion (PM), "
        "VS Code (coding), GitHub (code), Streamlit (dashboards), Buffer (social), "
        "Mailchimp (email), ChatGPT/Claude/Grok (AI), Descript (podcast), "
        "Audacity (audio), GIMP (images), Blender (3D), Loom (recording), "
        "Zapier/Make (automation), Supabase/Firebase (backend), Cloudflare (CDN).\n"
        "4. Priority management\n5. Quick answers — be direct\n\n"
        "Keep responses SHORT for voice (2-4 sentences for simple, longer for complex). "
        "Always address Loash by name. Be confident and decisive."
    )

    # ── Display conversation ──
    for msg in st.session_state.jarvis_chat:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown('<span class="chat-agent-badge">🤖 J.A.R.V.I.S.</span>', unsafe_allow_html=True)
            st.markdown(msg["content"])

    # ── Process pending message ──
    if st.session_state.jarvis_chat and st.session_state.jarvis_chat[-1]["role"] == "user":
        with st.chat_message("assistant"):
            st.markdown('<span class="chat-agent-badge">🤖 J.A.R.V.I.S.</span>', unsafe_allow_html=True)
            with st.spinner("JARVIS is thinking..."):
                j_hist = [{"role": m["role"], "content": m["content"]} for m in st.session_state.jarvis_chat]
                j_resp = None
                if "Claude" in jarvis_model:
                    if not claude_api_key:
                        j_resp = "🔑 Claude API key not set."
                    else:
                        try:
                            import anthropic
                            client = anthropic.Anthropic(api_key=claude_api_key)
                            resp = client.messages.create(
                                model="claude-sonnet-4-20250514", max_tokens=1024,
                                system=jarvis_system, messages=j_hist,
                            )
                            j_resp = resp.content[0].text
                        except Exception as e:
                            j_resp = f"⚠️ Error: {e}"
                elif "Grok" in jarvis_model:
                    if not grok_api_key:
                        j_resp = "🔑 Grok API key not set."
                    else:
                        try:
                            from openai import OpenAI
                            client = OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1")
                            resp = client.chat.completions.create(
                                model="grok-3-latest",
                                messages=[{"role": "system", "content": jarvis_system}, *j_hist],
                            )
                            j_resp = resp.choices[0].message.content
                        except Exception as e:
                            j_resp = f"⚠️ Error: {e}"

                st.markdown(j_resp)
                st.session_state.jarvis_chat.append({"role": "assistant", "content": j_resp})

                # Voice output — Microsoft Edge TTS (free, unlimited, high quality)
                if st.session_state.jarvis_voice_enabled and j_resp:
                    clean = j_resp.replace("**","").replace("*","").replace("#","").replace("`","")
                    clean = clean.replace("\n"," ").replace("\\","").strip()
                    if len(clean) > 800:
                        clean = clean[:800] + "... see full response on screen."

                    try:
                        import edge_tts
                        import asyncio
                        import base64
                        import tempfile
                        import os

                        async def _gen_speech(text, voice, outfile):
                            comm = edge_tts.Communicate(text, voice)
                            await comm.save(outfile)

                        # Voice options — pick one:
                        # en-US-GuyNeural (deep American male)
                        # en-GB-RyanNeural (British male — recommended for JARVIS)
                        # en-US-ChristopherNeural (authoritative American)
                        # en-US-JennyNeural (female)
                        jarvis_voice = "en-GB-RyanNeural"

                        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                            tmp_path = tmp.name

                        asyncio.run(_gen_speech(clean, jarvis_voice, tmp_path))

                        with open(tmp_path, "rb") as f:
                            audio_bytes = f.read()
                        os.unlink(tmp_path)

                        if audio_bytes:
                            audio_b64 = base64.b64encode(audio_bytes).decode()
                            st.components.v1.html(
                                f'<audio autoplay><source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg"></audio>',
                                height=0,
                            )
                    except Exception as e:
                        # Silent fallback to browser TTS
                        clean_js = clean.replace("'", "\\'").replace('"', '\\"')
                        st.components.v1.html(f"""<script>
                        (function(){{const s=window.speechSynthesis;s.cancel();
                        const u=new SpeechSynthesisUtterance('{clean_js}');
                        u.rate=1.0;u.pitch=0.85;s.speak(u)}})();
                        </script>""", height=0)

    # ── Text input — use your phone/browser dictation (mic icon on keyboard) ──
    if jarvis_typed := st.chat_input("Talk to JARVIS — use 🎙️ on your keyboard for voice..."):
        st.session_state.jarvis_chat.append({"role": "user", "content": jarvis_typed})
        st.rerun()

    # ── Quick commands ──
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:Share Tech Mono,monospace;font-size:0.72rem;color:#94a3b8;'
        'letter-spacing:1px;margin-bottom:8px">QUICK COMMANDS</div>',
        unsafe_allow_html=True,
    )
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        if st.button("📋 Daily Brief", key="jv_brief", use_container_width=True):
            st.session_state.jarvis_chat.append({"role": "user", "content": "Give me a quick daily briefing. What should I focus on today?"})
            st.rerun()
    with qc2:
        if st.button("🧠 Who handles this?", key="jv_route", use_container_width=True):
            st.session_state.jarvis_chat.append({"role": "user", "content": "I have a task I need help with. Ask me what it is and then tell me which agent should handle it."})
            st.rerun()
    with qc3:
        if st.button("📱 Best free app?", key="jv_app", use_container_width=True):
            st.session_state.jarvis_chat.append({"role": "user", "content": "I need a tool recommendation. Ask me what I'm trying to accomplish and suggest the best free apps."})
            st.rerun()
    with qc4:
        if st.button("⚡ What's urgent?", key="jv_urgent", use_container_width=True):
            st.session_state.jarvis_chat.append({"role": "user", "content": "What are my most urgent priorities right now? What needs immediate attention?"})
            st.rerun()

    st.markdown(
        '<div style="text-align:center;font-family:Share Tech Mono,monospace;font-size:0.62rem;'
        'color:#475569;letter-spacing:1px;margin-top:8px">'
        '💡 USE THE MIC BUTTON ABOVE FOR VOICE · OR TYPE BELOW · PHONE: USE 🎙️ ON KEYBOARD'
        '</div>',
        unsafe_allow_html=True,
    )

# =============================================================================
# TAB 1 — MISSION CONTROL (interactive)
# =============================================================================
with tab_mission:
    online_count = sum(1 for a in AGENTS.values() if a["status"] == "online")
    offline_agents = [(n, a) for n, a in AGENTS.items() if a["status"] != "online"]
    online_agents_list = [(n, a) for n, a in AGENTS.items() if a["status"] == "online"]
    active_task_list = [t for t in st.session_state.tasks if t["status"] == "In Progress"]
    critical_task_list = [t for t in st.session_state.tasks if t["priority"] == "Critical"]
    done_task_list = [t for t in st.session_state.tasks if t["status"] == "Done"]
    total_msgs = sum(len(v) for v in st.session_state.agent_chats.values())

    metrics = [
        ("🟢", str(online_count), f"/ {len(AGENTS)}", "AGENTS ONLINE"),
        ("🔄", str(len(active_task_list)), "", "TASKS ACTIVE"),
        ("⚠️", str(len(critical_task_list)), "", "CRITICAL"),
        ("✅", str(len(done_task_list)), "", "COMPLETED"),
        ("💬", str(total_msgs), "", "MESSAGES"),
    ]
    mcols = st.columns(len(metrics))
    for col, (icon, val, suffix, label) in zip(mcols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div style="font-size:1.3rem">{icon}</div>'
                f'<div class="metric-value">{val}<span style="font-size:1rem;opacity:0.5"> {suffix}</span></div>'
                f'<div class="metric-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Daily Briefing ──
    if "daily_briefing" not in st.session_state:
        st.session_state.daily_briefing = ""

    db1, db2 = st.columns([3, 1])
    with db1:
        st.markdown(
            '<div style="font-family:Rajdhani,sans-serif;font-size:0.88rem;color:#94a3b8;margin:8px 0">'
            '🤖 <span style="color:#8b5cf6;font-weight:600">JARVIS</span> will analyze your team status, '
            'tasks, and priorities to generate an executive briefing.</div>',
            unsafe_allow_html=True,
        )
    with db2:
        run_briefing = st.button("📋 Daily Briefing", use_container_width=True, type="primary")

    if run_briefing:
        with st.spinner("🤖 JARVIS is preparing your daily briefing..."):
            # Build real context from dashboard state
            online_names = ", ".join(n for n, a in AGENTS.items() if a["status"] == "online")
            offline_names = ", ".join(n for n, a in AGENTS.items() if a["status"] != "online") or "None"
            tasks_todo = [t for t in st.session_state.tasks if t["status"] == "To Do"]
            tasks_progress = [t for t in st.session_state.tasks if t["status"] == "In Progress"]
            tasks_blocked = [t for t in st.session_state.tasks if t["status"] == "Blocked"]
            tasks_done = [t for t in st.session_state.tasks if t["status"] == "Done"]
            tasks_critical = [t for t in st.session_state.tasks if t["priority"] == "Critical"]

            task_summary = ""
            if tasks_critical:
                task_summary += f"CRITICAL TASKS ({len(tasks_critical)}):\n"
                for t in tasks_critical:
                    task_summary += f"  - {t['title']} (assigned: {t['assignee']}, status: {t['status']})\n"
            if tasks_progress:
                task_summary += f"IN PROGRESS ({len(tasks_progress)}):\n"
                for t in tasks_progress:
                    task_summary += f"  - {t['title']} (assigned: {t['assignee']})\n"
            if tasks_todo:
                task_summary += f"TO DO ({len(tasks_todo)}):\n"
                for t in tasks_todo:
                    task_summary += f"  - {t['title']} (assigned: {t['assignee']}, priority: {t['priority']})\n"
            if tasks_blocked:
                task_summary += f"BLOCKED ({len(tasks_blocked)}):\n"
                for t in tasks_blocked:
                    task_summary += f"  - {t['title']} (assigned: {t['assignee']})\n"
            if tasks_done:
                task_summary += f"COMPLETED ({len(tasks_done)}):\n"
                for t in tasks_done:
                    task_summary += f"  - {t['title']} (assigned: {t['assignee']})\n"

            agent_activity = ""
            for name in AGENTS:
                ct = len(st.session_state.agent_chats.get(name, []))
                if ct > 0:
                    agent_activity += f"  - {name}: {ct} messages exchanged\n"

            council_ct = len(st.session_state.get("council_decisions", []))

            briefing_prompt = (
                f"You are JARVIS, Chief Strategy Officer. Generate a daily executive briefing for CEO Loash.\n\n"
                f"CURRENT DASHBOARD STATE:\n"
                f"- Date: {datetime.now().strftime('%A, %B %d %Y, %I:%M %p')}\n"
                f"- Agents Online: {online_count}/{len(AGENTS)} ({online_names})\n"
                f"- Agents Offline: {offline_names}\n"
                f"- Total Tasks: {len(st.session_state.tasks)}\n"
                f"- Total Messages This Session: {total_msgs}\n"
                f"- Council Decisions Made: {council_ct}\n\n"
                f"TASK BREAKDOWN:\n{task_summary}\n"
                f"AGENT ACTIVITY:\n{agent_activity if agent_activity else '  No conversations this session yet.'}\n\n"
                f"Generate a structured executive briefing with:\n"
                f"1. **STATUS OVERVIEW** — Quick snapshot of where things stand\n"
                f"2. **PRIORITY ACTIONS** — What needs CEO attention right now (most urgent first)\n"
                f"3. **TEAM UTILIZATION** — Which agents are being used, which are underutilized\n"
                f"4. **RECOMMENDATIONS** — What JARVIS recommends the CEO focus on today\n"
                f"5. **BLOCKERS & RISKS** — Anything that could slow progress\n\n"
                f"Be concise, executive-level, and actionable. Address the CEO as Loash."
            )
            briefing_result = _call_llm(
                "JARVIS",
                "Claude (Anthropic)" if claude_api_key else "Grok (xAI)",
                claude_api_key, grok_api_key,
                [{"role": "user", "content": briefing_prompt}],
            )
            st.session_state.daily_briefing = briefing_result

    if st.session_state.daily_briefing:
        st.markdown(
            '<div class="dept-card" style="border-left:3px solid #8b5cf6;margin:12px 0">'
            '<span class="agent-name">🤖 JARVIS — DAILY BRIEFING</span><br/>'
            '<span style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#94a3b8">'
            f'{datetime.now().strftime("%B %d %Y")}</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.daily_briefing)
        br1, br2 = st.columns(2)
        with br1:
            if st.button("📤 Send to Telegram"):
                try:
                    import requests
                    tg_token = ""
                    tg_chat = ""
                    try:
                        tg_token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
                        tg_chat = st.secrets.get("TELEGRAM_CHAT_ID", "")
                    except Exception:
                        pass
                    if tg_token and tg_chat:
                        header = f"🏢 AI AGENT HOME BASE\n📋 Daily Briefing — {datetime.now().strftime('%B %d, %Y')}\n{'─' * 30}\n\n"
                        msg = header + st.session_state.daily_briefing
                        # Split if too long
                        chunks = []
                        while len(msg) > 4000:
                            sp = msg.rfind("\n", 0, 4000)
                            if sp == -1:
                                sp = 4000
                            chunks.append(msg[:sp])
                            msg = msg[sp:]
                        chunks.append(msg)
                        for chunk in chunks:
                            resp = requests.post(
                                f"https://api.telegram.org/bot{tg_token}/sendMessage",
                                json={"chat_id": tg_chat, "text": chunk},
                            )
                        st.success("✅ Sent to Telegram!")
                    else:
                        st.error("⚠️ Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to Streamlit Cloud Secrets.")
                except Exception as e:
                    st.error(f"⚠️ Telegram error: {e}")
        with br2:
            if st.button("🗑️ Clear briefing"):
                st.session_state.daily_briefing = ""
                st.rerun()

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ── Expandable metric details ──
    with st.expander("🟢 Agents Online — click to view details"):
        oc1, oc2 = st.columns(2)
        with oc1:
            st.markdown("**✅ Online:**")
            for name, info in online_agents_list:
                msg_ct = len(st.session_state.agent_chats.get(name, []))
                st.markdown(
                    f'<div class="sidebar-agent">'
                    f'<span class="status-dot-online"></span> '
                    f'<span class="sidebar-agent-name">{info["icon"]} {name}</span>'
                    f'<br/><span class="sidebar-agent-role">{info["role"]} · {info["dept"]}</span>'
                    f'{f" · {msg_ct} msgs" if msg_ct else ""}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        with oc2:
            st.markdown("**🔴 Offline:**")
            if offline_agents:
                for name, info in offline_agents:
                    st.markdown(
                        f'<div class="sidebar-agent">'
                        f'<span class="status-dot-offline"></span> '
                        f'<span class="sidebar-agent-name">{info["icon"]} {name}</span>'
                        f'<br/><span class="sidebar-agent-role">{info["role"]} · {info["dept"]}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("All agents online!")

    with st.expander("🔄 Active Tasks — click to view details"):
        if active_task_list:
            for t in active_task_list:
                ai_info = AGENTS.get(t["assignee"], {})
                pcolor = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#f97316", "Critical": "#ef4444"}.get(t["priority"], "#888")
                st.markdown(
                    f'<div class="task-card" style="border-left:3px solid {pcolor}">'
                    f'<div class="task-title">{t["title"]}</div>'
                    f'<div class="task-meta">{ai_info.get("icon", "")} {t["assignee"]} · '
                    f'<span style="color:{pcolor}">{t["priority"]}</span> · {t.get("created", "")}</div>'
                    f'<div style="font-family:Rajdhani,sans-serif;font-size:0.8rem;color:#94a3b8;margin-top:4px">'
                    f'{t.get("description", "")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No active tasks right now.")

    with st.expander("⚠️ Critical Issues — click to view details"):
        if critical_task_list:
            for t in critical_task_list:
                ai_info = AGENTS.get(t["assignee"], {})
                st.markdown(
                    f'<div class="task-card" style="border-left:3px solid #ef4444">'
                    f'<div class="task-title">🚨 {t["title"]}</div>'
                    f'<div class="task-meta">{ai_info.get("icon", "")} {t["assignee"]} · '
                    f'Status: {t["status"]} · {t.get("created", "")}</div>'
                    f'<div style="font-family:Rajdhani,sans-serif;font-size:0.8rem;color:#94a3b8;margin-top:4px">'
                    f'{t.get("description", "")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("No critical issues!")

    with st.expander("✅ Completed Tasks — click to view deliverables"):
        if done_task_list:
            for t in done_task_list:
                ai_info = AGENTS.get(t["assignee"], {})
                st.markdown(
                    f'<div class="task-card" style="border-left:3px solid #22c55e">'
                    f'<div class="task-title">✅ {t["title"]}</div>'
                    f'<div class="task-meta">{ai_info.get("icon", "")} {t["assignee"]} · {t.get("created", "")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if t.get("result"):
                    st.markdown(t["result"][:500] + ("..." if len(t.get("result", "")) > 500 else ""))
                    st.markdown("---")
        else:
            st.caption("No completed tasks yet. Execute tasks in the Tasks tab!")

    with st.expander("💬 Messages — per-agent breakdown"):
        for name, info in AGENTS.items():
            msg_ct = len(st.session_state.agent_chats.get(name, []))
            if msg_ct > 0:
                st.markdown(
                    f'{info["icon"]} **{name}** — {msg_ct} messages · {info["role"]}',
                )
        if total_msgs == 0:
            st.caption("No messages yet. Start chatting in the Chat tab!")

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ── DEPARTMENTS — interactive with details ──
    st.markdown('<div class="section-header">DEPARTMENTS</div>', unsafe_allow_html=True)

    for dept_key, dept_info in DEPARTMENTS.items():
        members = [(n, a) for n, a in AGENTS.items() if a["dept"] == dept_key]
        dept_online = sum(1 for _, a in members if a["status"] == "online")
        dept_tasks_done = [t for t in st.session_state.tasks if t.get("assignee") in [n for n, _ in members] and t["status"] == "Done"]
        dept_tasks_active = [t for t in st.session_state.tasks if t.get("assignee") in [n for n, _ in members] and t["status"] != "Done"]

        with st.expander(
            f'{dept_info["label"].upper()} — {dept_online}/{len(members)} online · '
            f'{len(dept_tasks_done)} completed · {len(dept_tasks_active)} in queue'
        ):
            # Department header
            st.markdown(
                f'<div class="dept-card" style="border-left:3px solid {dept_info["color"]};margin-bottom:12px">'
                f'<span class="dept-name" style="color:{dept_info["color"]}">{dept_info["label"].upper()} DEPARTMENT</span><br/>'
                f'<div style="font-family:Rajdhani,sans-serif;font-size:0.88rem;color:#e2e8f0;margin-top:6px">'
                f'{dept_info.get("mission", "")}</div>'
                f'<div style="margin-top:8px;font-family:Rajdhani,sans-serif;font-size:0.82rem;color:#94a3b8">'
                f'<span style="color:{dept_info["color"]};font-weight:600">Example use cases:</span> '
                f'{dept_info.get("examples", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Agents in this department
            st.markdown(f"**Team Members ({len(members)}):**")
            for name, info in members:
                dot_class = "status-dot-online" if info["status"] == "online" else "status-dot-offline"
                msg_ct = len(st.session_state.agent_chats.get(name, []))
                st.markdown(
                    f'<div class="agent-office-card" style="border-top:2px solid {info["color"]};margin-bottom:8px">'
                    f'<span class="{dot_class}"></span> '
                    f'<span class="agent-name">{info["icon"]} {name}</span> · '
                    f'<span class="agent-role">{info["role"]}</span>'
                    f'{f" · <span style=color:#8b5cf6>{msg_ct} msgs</span>" if msg_ct else ""}<br/>'
                    f'<div style="margin-top:4px;font-family:Rajdhani,sans-serif;font-size:0.8rem;color:#94a3b8">'
                    f'<span style="color:{info["color"]};font-weight:600">Use for:</span> '
                    f'{info.get("use_cases", "General tasks")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Completed deliverables from this department
            if dept_tasks_done:
                st.markdown(f"**Completed Deliverables ({len(dept_tasks_done)}):**")
                for t in dept_tasks_done:
                    ai_info = AGENTS.get(t["assignee"], {})
                    st.markdown(
                        f'<div class="task-card" style="border-left:3px solid #22c55e">'
                        f'<div class="task-title">✅ {t["title"]}</div>'
                        f'<div class="task-meta">{ai_info.get("icon", "")} {t["assignee"]} · {t.get("created", "")}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    if t.get("result"):
                        st.markdown(t["result"][:300] + ("..." if len(t.get("result", "")) > 300 else ""))

            # Active tasks
            if dept_tasks_active:
                st.markdown(f"**In Queue ({len(dept_tasks_active)}):**")
                for t in dept_tasks_active:
                    pcolor = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#f97316", "Critical": "#ef4444"}.get(t["priority"], "#888")
                    st.markdown(
                        f'<div class="task-card" style="border-left:3px solid {pcolor}">'
                        f'<div class="task-title">{t["title"]}</div>'
                        f'<div class="task-meta">{t["status"]} · '
                        f'<span style="color:{pcolor}">{t["priority"]}</span></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

# =============================================================================
# TAB 2 — TASKS (with AI orchestration)
# =============================================================================
with tab_tasks:
    st.markdown('<div class="section-header">TASK BOARD</div>', unsafe_allow_html=True)

    # ── Add new task ──
    with st.expander("➕ Add New Task", expanded=False):
        with st.form("new_task_form"):
            fc1, fc2 = st.columns(2)
            new_title = fc1.text_input("Task title")
            new_assignee = fc2.selectbox("Assign to", list(AGENTS.keys()))
            fc3, fc4 = st.columns(2)
            new_priority = fc3.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            new_description = fc4.text_input("Brief description (optional)")
            submitted = st.form_submit_button("Create Task")
            if submitted and new_title:
                new_id = max(t["id"] for t in st.session_state.tasks) + 1 if st.session_state.tasks else 1
                st.session_state.tasks.append({
                    "id": new_id, "title": new_title, "assignee": new_assignee,
                    "status": "To Do", "priority": new_priority,
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "description": new_description or new_title,
                    "result": "",
                })
                st.rerun()

    # ── Kanban columns ──
    statuses = ["To Do", "In Progress", "Blocked", "Done"]
    status_icons = {"To Do": "📌", "In Progress": "🔄", "Blocked": "🚫", "Done": "✅"}
    priority_colors = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#f97316", "Critical": "#ef4444"}
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

    kcols = st.columns(len(statuses))
    for col, status in zip(kcols, statuses):
        with col:
            tasks_here = [t for t in st.session_state.tasks if t["status"] == status]
            tasks_here.sort(key=lambda t: priority_order.get(t["priority"], 99))
            st.markdown(f"**{status_icons[status]} {status}** ({len(tasks_here)})")
            for t in tasks_here:
                pcolor = priority_colors.get(t["priority"], "#888")
                agent_icon = AGENTS.get(t["assignee"], {}).get("icon", "")
                has_result = "✅" if t.get("result") else ""
                st.markdown(
                    f'<div class="task-card" style="border-left:3px solid {pcolor}">'
                    f'<div class="task-title">{t["title"]} {has_result}</div>'
                    f'<div class="task-meta">'
                    f'{agent_icon} {t["assignee"]} · '
                    f'<span style="color:{pcolor}">{t["priority"]}</span> · '
                    f'{t.get("created", "")}'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            if not tasks_here:
                st.caption("Empty")

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ── Task Actions (update, execute, delete) ──
    st.markdown('<div class="section-header">TASK ACTIONS</div>', unsafe_allow_html=True)

    if st.session_state.tasks:
        task_options = {
            f"#{t['id']} {t['title']} [{t['status']}]": t["id"]
            for t in st.session_state.tasks
        }
        selected_label = st.selectbox("Select task", list(task_options.keys()), key="task_action_select")
        selected_tid = task_options[selected_label]
        selected_task = next((t for t in st.session_state.tasks if t["id"] == selected_tid), None)

        if selected_task:
            # Show task details
            agent_info = AGENTS.get(selected_task["assignee"], {})
            pcolor = priority_colors.get(selected_task["priority"], "#888")
            st.markdown(
                f'<div class="dept-card" style="border-left:3px solid {pcolor};margin:8px 0">'
                f'<span class="agent-name">{agent_info.get("icon", "")} {selected_task["assignee"]}</span> · '
                f'<span style="color:{pcolor};font-family:Orbitron,monospace;font-size:0.7rem">{selected_task["priority"]}</span> · '
                f'<span class="agent-role">{selected_task["status"]}</span><br/>'
                f'<div style="margin-top:6px;font-family:Rajdhani,sans-serif;font-size:0.85rem;color:#94a3b8">'
                f'{selected_task.get("description", selected_task["title"])}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Action buttons row
            ac1, ac2, ac3, ac4 = st.columns(4)
            with ac1:
                new_status = st.selectbox("Move to", statuses, key="task_move_status")
            with ac2:
                if st.button("📋 Update Status", use_container_width=True):
                    selected_task["status"] = new_status
                    st.rerun()
            with ac3:
                if st.button("🤖 Execute with AI", use_container_width=True, type="primary"):
                    st.session_state[f"_exec_task_{selected_tid}"] = True
                    st.rerun()
            with ac4:
                if st.button("🗑️ Delete Task", use_container_width=True):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != selected_tid]
                    st.rerun()

            # ── Execute with AI ──
            if st.session_state.get(f"_exec_task_{selected_tid}", False):
                st.session_state[f"_exec_task_{selected_tid}"] = False
                with st.spinner(f"{selected_task['assignee']} is working on this task..."):
                    exec_prompt = (
                        f"You have been assigned a task by CEO Loash.\n\n"
                        f"TASK: {selected_task['title']}\n"
                        f"DESCRIPTION: {selected_task.get('description', selected_task['title'])}\n"
                        f"PRIORITY: {selected_task['priority']}\n\n"
                        f"Complete this task thoroughly. Provide a detailed, actionable deliverable. "
                        f"Format your output clearly so the CEO can review and use it immediately."
                    )
                    exec_history = [{"role": "user", "content": exec_prompt}]
                    result = _call_llm(
                        selected_task["assignee"],
                        "Claude (Anthropic)" if claude_api_key else "Grok (xAI)",
                        claude_api_key, grok_api_key, exec_history,
                    )
                    selected_task["result"] = result
                    selected_task["status"] = "Done"
                    st.rerun()

            # ── Show result if exists ──
            if selected_task.get("result"):
                st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="section-header">'
                    f'{agent_info.get("icon", "")} {selected_task["assignee"]} DELIVERABLE</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(selected_task["result"])
                if st.button("📋 Copy result to clipboard", key=f"copy_result_{selected_tid}"):
                    st.code(selected_task["result"], language=None)

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

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # AUTO-ROUTE — Smart agent routing
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🧠 AUTO-ROUTE</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:Rajdhani,sans-serif;font-size:0.88rem;color:#94a3b8;margin-bottom:12px">'
        'Describe your idea or need — the system analyzes it, picks the best agent, '
        'explains why, and routes your message automatically.</div>',
        unsafe_allow_html=True,
    )

    # Initialize auto-route history
    if "autoroute_history" not in st.session_state:
        st.session_state.autoroute_history = []

    # Show previous auto-routes
    for ar in st.session_state.autoroute_history:
        ar_agent = AGENTS.get(ar["agent"], {})
        st.markdown(
            f'<div class="dept-card" style="border-left:3px solid {ar_agent.get("color", "#666")};margin:6px 0">'
            f'<span class="agent-name">💬 You:</span> '
            f'<span class="agent-role">{ar["message"][:100]}</span><br/>'
            f'<div style="margin-top:4px;font-family:Share Tech Mono,monospace;font-size:0.72rem;color:#8b5cf6">'
            f'🧠 Routed to {ar_agent.get("icon", "")} {ar["agent"]} — {ar["reasoning"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander(f'{ar_agent.get("icon", "")} {ar["agent"]} response', expanded=False):
            st.markdown(ar["response"])

    # Auto-route input
    with st.form("autoroute_form"):
        ar_message = st.text_area(
            "What do you need?",
            placeholder="e.g. I want to build a referral program... / Write me a launch tweet... / Is this idea worth pursuing?...",
            height=80,
            key="ar_message",
        )
        ar_model = st.selectbox("Model", ["Claude (Anthropic)", "Grok (xAI)"], key="ar_model")
        ar_submit = st.form_submit_button("🧠 Auto-Route & Execute", use_container_width=True)

    if ar_submit and ar_message:
        # Step 1: Determine best agent
        routed_agent, reasoning = _auto_route(ar_message)
        routed_info = AGENTS[routed_agent]

        st.markdown(
            f'<div class="dept-card" style="border-left:3px solid {routed_info["color"]};margin:8px 0">'
            f'<div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#8b5cf6;margin-bottom:6px">'
            f'🧠 AUTO-ROUTE DECISION</div>'
            f'<span class="agent-name">{routed_info["icon"]} {routed_agent}</span> · '
            f'<span class="agent-role">{routed_info["role"]}</span><br/>'
            f'<div style="margin-top:4px;font-family:Rajdhani,sans-serif;font-size:0.82rem;color:#94a3b8">'
            f'{reasoning}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Step 2: Send to that agent
        with st.spinner(f"{routed_info['icon']} {routed_agent} is working on this..."):
            route_prompt = (
                f"CEO Loash has a request that was auto-routed to you as the best agent.\n\n"
                f"REQUEST: {ar_message}\n\n"
                f"Provide a thorough, actionable response. If you think another agent should also be consulted, "
                f"mention that at the end of your response."
            )
            result = _call_llm(
                routed_agent, ar_model, claude_api_key, grok_api_key,
                [{"role": "user", "content": route_prompt}],
            )
            st.markdown(result)

            # Save to history
            st.session_state.autoroute_history.append({
                "message": ar_message,
                "agent": routed_agent,
                "reasoning": reasoning,
                "response": result,
            })

            # Also save to that agent's chat memory
            st.session_state.agent_chats[routed_agent].append(
                {"role": "user", "content": f"[Auto-routed] {ar_message}"}
            )
            st.session_state.agent_chats[routed_agent].append(
                {"role": "assistant", "content": result}
            )

    if st.session_state.autoroute_history:
        if st.button("🗑️ Clear auto-route history"):
            st.session_state.autoroute_history = []
            st.rerun()

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # COUNCIL MODE — Structured Decision Pipeline
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🏛️ COUNCIL — DECISION PIPELINE</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:Rajdhani,sans-serif;font-size:0.88rem;color:#94a3b8;margin-bottom:12px">'
        'Submit an idea or decision. The Council processes it through a structured pipeline: '
        '<span style="color:#22c55e;font-weight:600">GROWTH</span> analyzes the opportunity → '
        '<span style="color:#ef4444;font-weight:600">SKEPTIC</span> stress-tests it → '
        '<span style="color:#3b82f6;font-weight:600">RETENTION</span> synthesizes the final plan. '
        'One cohesive deliverable.</div>',
        unsafe_allow_html=True,
    )

    # Pipeline visualization
    st.markdown(
        '<div style="display:flex;align-items:center;justify-content:center;gap:0;margin:10px 0 16px;flex-wrap:wrap">'
        '<div style="background:#111128;border:1px solid rgba(34,197,94,0.3);border-radius:8px;padding:6px 14px;text-align:center">'
        '<div style="font-family:Orbitron,monospace;font-size:0.6rem;color:#22c55e;letter-spacing:1px">STEP 1</div>'
        '<div style="font-size:0.85rem">📈 GROWTH</div>'
        '<div style="font-family:Rajdhani,sans-serif;font-size:0.7rem;color:#94a3b8">Opportunity</div></div>'
        '<div style="color:#94a3b8;font-size:1.2rem;margin:0 6px">→</div>'
        '<div style="background:#111128;border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:6px 14px;text-align:center">'
        '<div style="font-family:Orbitron,monospace;font-size:0.6rem;color:#ef4444;letter-spacing:1px">STEP 2</div>'
        '<div style="font-size:0.85rem">🤔 SKEPTIC</div>'
        '<div style="font-family:Rajdhani,sans-serif;font-size:0.7rem;color:#94a3b8">Stress Test</div></div>'
        '<div style="color:#94a3b8;font-size:1.2rem;margin:0 6px">→</div>'
        '<div style="background:#111128;border:1px solid rgba(59,130,246,0.3);border-radius:8px;padding:6px 14px;text-align:center">'
        '<div style="font-family:Orbitron,monospace;font-size:0.6rem;color:#3b82f6;letter-spacing:1px">STEP 3</div>'
        '<div style="font-size:0.85rem">🔄 RETENTION</div>'
        '<div style="font-family:Rajdhani,sans-serif;font-size:0.7rem;color:#94a3b8">Final Plan</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Initialize council history
    if "council_decisions" not in st.session_state:
        st.session_state.council_decisions = []

    # Council input
    with st.form("council_form"):
        council_idea = st.text_area(
            "Your idea or decision",
            placeholder="e.g. Launch a free tier for our product, Pivot to B2B, Add a referral program, Raise prices by 20%...",
            height=80,
            key="council_idea",
        )
        council_context = st.text_input(
            "Additional context (optional)",
            placeholder="Any constraints, goals, timeline, or background info...",
            key="council_context",
        )
        council_model = st.selectbox("Model", ["Claude (Anthropic)", "Grok (xAI)"], key="council_model")
        council_submit = st.form_submit_button("🏛️ Run Decision Pipeline", use_container_width=True)

    if council_submit and council_idea:
        context_block = f"\nAdditional context from CEO: {council_context}" if council_context else ""

        decision = {"idea": council_idea, "context": council_context, "steps": {}}

        # ── STEP 1: GROWTH — Opportunity Analysis ──
        st.markdown(
            '<div class="dept-card" style="border-left:3px solid #22c55e;margin:8px 0">'
            '<span class="agent-name">📈 STEP 1: GROWTH — Opportunity Analysis</span></div>',
            unsafe_allow_html=True,
        )
        with st.spinner("📈 GROWTH is analyzing the opportunity..."):
            growth_prompt = (
                f"CEO Loash has submitted an idea to the Advisory Council for structured evaluation.\n\n"
                f"THE IDEA: {council_idea}{context_block}\n\n"
                f"As GROWTH (Growth Advisor), your job is STEP 1 of the decision pipeline.\n"
                f"Analyze this idea purely from a GROWTH perspective:\n"
                f"- What is the growth opportunity here? How big could this be?\n"
                f"- What are the best-case scenarios for user acquisition, revenue, or market position?\n"
                f"- What growth levers does this unlock?\n"
                f"- What data or signals support this direction?\n"
                f"- Propose an aggressive but realistic growth thesis.\n\n"
                f"Be specific, data-minded, and actionable. 3-4 paragraphs max."
            )
            growth_result = _call_llm("GROWTH", council_model, claude_api_key, grok_api_key,
                                       [{"role": "user", "content": growth_prompt}])
            decision["steps"]["GROWTH"] = growth_result
            st.markdown(growth_result)

        # ── STEP 2: SKEPTIC — Stress Test ──
        st.markdown(
            '<div class="dept-card" style="border-left:3px solid #ef4444;margin:8px 0">'
            '<span class="agent-name">🤔 STEP 2: SKEPTIC — Stress Test</span></div>',
            unsafe_allow_html=True,
        )
        with st.spinner("🤔 SKEPTIC is stress-testing GROWTH's analysis..."):
            skeptic_prompt = (
                f"CEO Loash has submitted an idea to the Advisory Council.\n\n"
                f"THE IDEA: {council_idea}{context_block}\n\n"
                f"GROWTH just completed their opportunity analysis. Here is their assessment:\n"
                f"---\n{growth_result}\n---\n\n"
                f"As SKEPTIC (Devil's Advocate), your job is STEP 2 of the decision pipeline.\n"
                f"Stress-test GROWTH's analysis ruthlessly:\n"
                f"- What are the biggest risks and failure modes?\n"
                f"- Where is GROWTH being too optimistic or ignoring red flags?\n"
                f"- What assumptions are unproven? What could go wrong?\n"
                f"- What's the worst-case scenario?\n"
                f"- What would need to be true for this to work vs. fail?\n\n"
                f"Be constructive but brutally honest. Identify the top 3-5 risks. 3-4 paragraphs max."
            )
            skeptic_result = _call_llm("SKEPTIC", council_model, claude_api_key, grok_api_key,
                                        [{"role": "user", "content": skeptic_prompt}])
            decision["steps"]["SKEPTIC"] = skeptic_result
            st.markdown(skeptic_result)

        # ── STEP 3: RETENTION — Synthesis & Final Plan ──
        st.markdown(
            '<div class="dept-card" style="border-left:3px solid #3b82f6;margin:8px 0">'
            '<span class="agent-name">🔄 STEP 3: RETENTION — Final Decision Brief</span></div>',
            unsafe_allow_html=True,
        )
        with st.spinner("🔄 RETENTION is synthesizing the final decision brief..."):
            retention_prompt = (
                f"CEO Loash has submitted an idea to the Advisory Council.\n\n"
                f"THE IDEA: {council_idea}{context_block}\n\n"
                f"The Council has completed two rounds of analysis:\n\n"
                f"GROWTH's Opportunity Analysis:\n---\n{growth_result}\n---\n\n"
                f"SKEPTIC's Stress Test:\n---\n{skeptic_result}\n---\n\n"
                f"As RETENTION (Retention Advisor), your job is STEP 3 — the FINAL step of the decision pipeline.\n"
                f"You have the full picture. Synthesize everything into ONE structured decision brief:\n\n"
                f"1. **VERDICT** — Should we proceed? (Go / No-Go / Go with modifications)\n"
                f"2. **RECOMMENDED APPROACH** — The specific strategy that balances growth opportunity against the risks identified\n"
                f"3. **KEY MITIGATIONS** — How to address SKEPTIC's top concerns\n"
                f"4. **ACTION STEPS** — Exactly what to do next, in order, with who should own each step\n"
                f"5. **SUCCESS METRICS** — How we'll know this is working\n\n"
                f"This is the deliverable the CEO will act on. Make it clear, decisive, and actionable."
            )
            retention_result = _call_llm("RETENTION", council_model, claude_api_key, grok_api_key,
                                          [{"role": "user", "content": retention_prompt}])
            decision["steps"]["RETENTION"] = retention_result
            st.markdown(retention_result)

        st.session_state.council_decisions.append(decision)
        st.success("✅ Council decision pipeline complete. Final brief delivered above.")

    # ── Previous decisions ──
    if st.session_state.council_decisions:
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📁 PREVIOUS DECISIONS</div>', unsafe_allow_html=True)
        for i, dec in enumerate(reversed(st.session_state.council_decisions)):
            with st.expander(f"Decision #{len(st.session_state.council_decisions) - i}: {dec['idea'][:80]}"):
                st.markdown("**📈 GROWTH — Opportunity:**")
                st.markdown(dec["steps"].get("GROWTH", "_pending_"))
                st.markdown("**🤔 SKEPTIC — Stress Test:**")
                st.markdown(dec["steps"].get("SKEPTIC", "_pending_"))
                st.markdown("**🔄 RETENTION — Final Brief:**")
                st.markdown(dec["steps"].get("RETENTION", "_pending_"))

        if st.button("🗑️ Clear all decisions"):
            st.session_state.council_decisions = []
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
            f"**Version:** 4.1"
        )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="footer-text">'
    f'AI AGENT HOME BASE · V4.1 · STREAMLIT + PLOTLY · '
    f'CLAUDE (ANTHROPIC) + GROK (XAI) · '
    f'{datetime.now().strftime("%Y-%m-%d")}'
    f'</div>',
    unsafe_allow_html=True,
)
