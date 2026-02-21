import streamlit as st
import plotly.graph_objects as go

# =============================================================================
# PAGE CONFIG (must be first Streamlit command)
# =============================================================================
st.set_page_config(
    page_title="AI Agent Home Base - CEO View",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# SESSION STATE INIT
# =============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =============================================================================
# SIDEBAR — API Keys + Agent Roster
# =============================================================================
with st.sidebar:
    st.markdown("## 🔑 API Keys")
    st.caption("Keys stay in your browser session only — never saved to disk.")

    # Try st.secrets first (for Streamlit Cloud), fall back to sidebar input
    # ── To use secrets on Streamlit Cloud: ──
    # Go to your app → Settings → Secrets, paste in TOML format:
    #   ANTHROPIC_API_KEY = "sk-ant-..."
    #   XAI_API_KEY = "xai-..."

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

    claude_api_key = st.text_input(
        "Anthropic (Claude) API Key",
        value=default_claude_key,
        type="password",
        help="Starts with sk-ant-...",
    )
    grok_api_key = st.text_input(
        "xAI (Grok) API Key",
        value=default_grok_key,
        type="password",
        help="Starts with xai-...",
    )

    # Status indicators for keys
    if claude_api_key:
        st.success("✅ Claude key loaded")
    else:
        st.warning("⚠️ Claude key missing")
    if grok_api_key:
        st.success("✅ Grok key loaded")
    else:
        st.warning("⚠️ Grok key missing")

    st.markdown("---")
    st.markdown("## 🤖 Agent Roster")

    # Agent roster: (name, role, department, status_dot)
    roster = [
        ("JARVIS",   "Chief Strategy Officer", "EXECUTIVE",   "🟢"),
        ("CLAWD",    "Senior Developer",       "DEVELOPMENT", "🟢"),
        ("SENTINEL", "QA Monitor",             "DEVELOPMENT", "🟢"),
        ("SCRIBE",   "Content Director",       "CONTENT",     "🟢"),
        ("ATLAS",    "Research Analyst",        "RESEARCH",    "🟢"),
        ("TRENDY",   "Viral Scout",            "RESEARCH",    "🔴"),
        ("PIXEL",    "Lead Designer",          "CREATIVE",    "🟢"),
        ("NOVA",     "Production Lead",        "CREATIVE",    "🟢"),
        ("VIBE",     "Motion Designer",        "CREATIVE",    "🔴"),
        ("CLIP",     "Clipping Agent",         "PRODUCT",     "🟡"),
    ]
    for name, role, dept, dot in roster:
        st.markdown(
            f"{dot} **{name}** — {role}  \n"
            f"<small style='opacity:0.55'>{dept}</small>",
            unsafe_allow_html=True,
        )

# =============================================================================
# MAIN TITLE
# =============================================================================
st.title("🏢 AI Agent Team — CEO Dashboard")
st.caption("**You (Loash)** are CEO. Below is your mission control.")

# =============================================================================
# TABS
# =============================================================================
tab_mission, tab_chat, tab_org = st.tabs(
    ["🎯 Mission Control", "💬 Chat", "🏗️ Org Chart"]
)

# =============================================================================
# TAB 1 — MISSION CONTROL
# =============================================================================
with tab_mission:
    st.subheader("Active Agents")

    cols = st.columns(4)
    cards = [
        ("CLAWD",    "Senior Developer",  "🟢 Active", "Full-stack dev & debugging"),
        ("SCRIBE",   "Content Director",  "🟢 Active", "Blog posts, threads, scripts"),
        ("CLIP",     "Clipping Agent",    "🟡 Idle",   "Video clip ideas from content"),
        ("SENTINEL", "QA Monitor",        "🟢 Active", "Code review & security"),
    ]
    for col, (name, role, status, desc) in zip(cols, cards):
        with col:
            if "Active" in status:
                st.success(f"**{name}** · {status}")
            elif "Idle" in status:
                st.warning(f"**{name}** · {status}")
            else:
                st.error(f"**{name}** · {status}")
            st.caption(f"{role} — {desc}")

    st.markdown("---")
    st.subheader("Quick Stats")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Agents Online", "7 / 10")
    m2.metric("Tasks Active", "3")
    m3.metric("Chat Messages", str(len(st.session_state.chat_history)))
    m4.metric("Departments", "6")

# =============================================================================
# TAB 2 — CHAT (Claude or Grok)
# =============================================================================
with tab_chat:
    st.subheader("Talk to Your AI Team")

    # Model selector row
    col_model, _ = st.columns([2, 4])
    with col_model:
        model_choice = st.selectbox(
            "Choose model",
            ["Claude (Anthropic)", "Grok (xAI)"],
            key="model_select",
        )

    # Show chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input box
    if prompt := st.chat_input("Send a message to JARVIS and your agent team…"):
        # 1. Show + store user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                response_text = None

                SYSTEM_PROMPT = (
                    "You are JARVIS, the Chief Strategy Officer of Loash's AI "
                    "agent team. You manage agents: CLAWD (developer), SENTINEL "
                    "(QA), SCRIBE (content), ATLAS (research), TRENDY (trends), "
                    "PIXEL (design), NOVA (production), VIBE (motion), CLIP "
                    "(video clipping). Be concise, strategic, and helpful. "
                    "Address the CEO as Loash."
                )

                # ── CLAUDE ──
                if "Claude" in model_choice:
                    if not claude_api_key:
                        response_text = (
                            "🔑 **Claude API key not set.**\n\n"
                            "Paste it in the sidebar, or add it to Streamlit "
                            "Cloud → Settings → Secrets:\n\n"
                            '```toml\nANTHROPIC_API_KEY = "sk-ant-..."\n```'
                        )
                    else:
                        try:
                            import anthropic

                            client = anthropic.Anthropic(api_key=claude_api_key)
                            resp = client.messages.create(
                                model="claude-sonnet-4-20250514",
                                max_tokens=1024,
                                system=SYSTEM_PROMPT,
                                messages=[
                                    {"role": m["role"], "content": m["content"]}
                                    for m in st.session_state.chat_history
                                ],
                            )
                            response_text = resp.content[0].text
                        except Exception as e:
                            response_text = f"⚠️ Claude API error:\n\n`{e}`"

                # ── GROK ──
                elif "Grok" in model_choice:
                    if not grok_api_key:
                        response_text = (
                            "🔑 **Grok API key not set.**\n\n"
                            "Paste it in the sidebar, or add it to Streamlit "
                            "Cloud → Settings → Secrets:\n\n"
                            '```toml\nXAI_API_KEY = "xai-..."\n```'
                        )
                    else:
                        try:
                            from openai import OpenAI

                            client = OpenAI(
                                api_key=grok_api_key,
                                base_url="https://api.x.ai/v1",
                            )
                            resp = client.chat.completions.create(
                                model="grok-3-latest",
                                messages=[
                                    {"role": "system", "content": SYSTEM_PROMPT},
                                    *[
                                        {
                                            "role": m["role"],
                                            "content": m["content"],
                                        }
                                        for m in st.session_state.chat_history
                                    ],
                                ],
                            )
                            response_text = resp.choices[0].message.content
                        except Exception as e:
                            response_text = f"⚠️ Grok API error:\n\n`{e}`"

                # Display response
                st.markdown(response_text)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response_text}
                )

    # Clear button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()

# =============================================================================
# TAB 3 — ORG CHART (your original Treemap, with colors)
# =============================================================================
with tab_org:
    st.subheader("Organization Hierarchy")

    fig = go.Figure(
        go.Treemap(
            labels=[
                "Loash (CEO)",
                "JARVIS (Chief Strategy Officer)",
                "COUNCIL (Advisory)",
                "DEVELOPMENT",
                "CONTENT",
                "RESEARCH",
                "CREATIVE",
                "PRODUCT",
                "CLAWD (Senior Developer)",
                "SENTINEL (QA Monitor)",
                "SCRIBE (Content Director)",
                "CLIP (Clipping Agent)",
                "ATLAS (Research Analyst)",
                "TRENDY (Viral Scout)",
                "PIXEL (Lead Designer)",
                "NOVA (Production Lead)",
                "VIBE (Motion Designer)",
            ],
            parents=[
                "",
                "Loash (CEO)",
                "Loash (CEO)",
                "Loash (CEO)",
                "Loash (CEO)",
                "Loash (CEO)",
                "Loash (CEO)",
                "Loash (CEO)",
                "DEVELOPMENT",
                "DEVELOPMENT",
                "CONTENT",
                "PRODUCT",
                "RESEARCH",
                "RESEARCH",
                "CREATIVE",
                "CREATIVE",
                "CREATIVE",
            ],
            marker_colors=[
                "#6366f1",  # CEO
                "#8b5cf6",  # JARVIS
                "#a78bfa",  # COUNCIL
                "#3b82f6",  # DEVELOPMENT
                "#10b981",  # CONTENT
                "#06b6d4",  # RESEARCH
                "#f59e0b",  # CREATIVE
                "#ef4444",  # PRODUCT
                "#60a5fa",  # CLAWD
                "#60a5fa",  # SENTINEL
                "#34d399",  # SCRIBE
                "#f87171",  # CLIP
                "#22d3ee",  # ATLAS
                "#22d3ee",  # TRENDY
                "#fbbf24",  # PIXEL
                "#fbbf24",  # NOVA
                "#fbbf24",  # VIBE
            ],
            textinfo="label",
            hovertemplate="<b>%{label}</b><extra></extra>",
        )
    )
    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        height=500,
        paper_bgcolor="#0e1117",
        font=dict(color="white"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Click any block to zoom in. Click the header bar to zoom back out."
    )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption(
    "AI Agent Home Base · Built with Streamlit · "
    "Claude (Anthropic) + Grok (xAI) · 100% free deployment"
)
