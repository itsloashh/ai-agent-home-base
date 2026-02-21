import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

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
# AGENT DATABASE — single source of truth for all agents
# =============================================================================
AGENTS = {
    "JARVIS":    {"role": "Chief Strategy Officer",  "dept": "EXECUTIVE",   "status": "online",  "icon": "🤖", "color": "#8b5cf6",
                  "prompt": "You are JARVIS, Loash's Chief Strategy Officer. You oversee all agents and provide high-level strategic advice. Be executive-level, concise, and actionable. Address the CEO as Loash."},
    "GROWTH":    {"role": "Growth Advisor",           "dept": "COUNCIL",     "status": "online",  "icon": "📈", "color": "#a78bfa",
                  "prompt": "You are GROWTH, a council advisor focused on growth strategy, user acquisition, and scaling. Give aggressive but smart growth advice to CEO Loash."},
    "RETENTION": {"role": "Retention Advisor",        "dept": "COUNCIL",     "status": "online",  "icon": "🔄", "color": "#a78bfa",
                  "prompt": "You are RETENTION, a council advisor focused on keeping users, reducing churn, and building loyalty. Advise CEO Loash on retention strategy."},
    "SKEPTIC":   {"role": "Devil's Advocate",         "dept": "COUNCIL",     "status": "online",  "icon": "🤔", "color": "#a78bfa",
                  "prompt": "You are SKEPTIC, a council advisor who challenges assumptions, finds flaws in plans, and stress-tests ideas. Push back constructively on CEO Loash's ideas."},
    "CLAWD":     {"role": "Senior Developer",         "dept": "DEVELOPMENT", "status": "online",  "icon": "🧑‍💻", "color": "#3b82f6",
                  "prompt": "You are CLAWD, the senior full-stack developer. You write clean, production-ready code. Help CEO Loash with coding, debugging, architecture, and technical decisions. Output code when asked."},
    "SENTINEL":  {"role": "QA Monitor",               "dept": "DEVELOPMENT", "status": "online",  "icon": "🛡️", "color": "#3b82f6",
                  "prompt": "You are SENTINEL, the QA and security monitor. You review code for bugs, security issues, and quality. Be thorough and flag risks for CEO Loash."},
    "SCRIBE":    {"role": "Content Director",         "dept": "CONTENT",     "status": "online",  "icon": "✍️", "color": "#10b981",
                  "prompt": "You are SCRIBE, the content director. You write blog posts, social threads, scripts, emails, and marketing copy. Match the tone CEO Loash requests. Output polished content."},
    "ATLAS":     {"role": "Research Analyst",         "dept": "RESEARCH",    "status": "online",  "icon": "🗺️", "color": "#06b6d4",
                  "prompt": "You are ATLAS, the research analyst. You research topics deeply, summarize findings, and present actionable insights to CEO Loash. Be thorough but concise."},
    "TRENDY":    {"role": "Viral Scout",              "dept": "RESEARCH",    "status": "offline", "icon": "🔥", "color": "#06b6d4",
                  "prompt": "You are TRENDY, the viral trend scout. You identify trending topics, viral formats, and cultural moments. Advise CEO Loash on what's hot right now."},
    "PIXEL":     {"role": "Lead Designer",            "dept": "CREATIVE",    "status": "online",  "icon": "🎨", "color": "#f59e0b",
                  "prompt": "You are PIXEL, the lead designer. You advise on UI/UX, branding, color palettes, layouts, and visual strategy for CEO Loash. Describe designs in detail."},
    "NOVA":      {"role": "Production Lead",          "dept": "CREATIVE",    "status": "online",  "icon": "💡", "color": "#f59e0b",
                  "prompt": "You are NOVA, the production lead. You manage creative pipelines, timelines, and asset delivery. Help CEO Loash coordinate production workflows."},
    "VIBE":      {"role": "Motion Designer",          "dept": "CREATIVE",    "status": "offline", "icon": "✨", "color": "#f59e0b",
                  "prompt": "You are VIBE, the motion designer. You create concepts for animations, transitions, motion graphics, and video effects. Describe motion concepts for CEO Loash."},
    "CLIP":      {"role": "Clipping Agent",           "dept": "PRODUCT",     "status": "online",  "icon": "🎬", "color": "#ef4444",
                  "prompt": "You are CLIP, the clipping agent. You take long-form content (transcripts, videos, articles) and identify the best short clips, highlights, and quotable moments for CEO Loash. Output timestamps or excerpts with reasoning."},
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
# SESSION STATE INIT
# =============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
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
# SIDEBAR — API Keys + Agent Roster
# =============================================================================
with st.sidebar:
    st.markdown("## 🔑 API Keys")
    st.caption("Keys stay in your browser session only — never saved to disk.")

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
    online_total = sum(1 for a in AGENTS.values() if a["status"] == "online")
    st.caption(f"{online_total}/{len(AGENTS)} online")

    for name, info in AGENTS.items():
        if info["status"] == "online":
            dot = "🟢"
        elif info["status"] == "idle":
            dot = "🟡"
        else:
            dot = "🔴"
        st.markdown(
            f"{dot} **{name}** — {info['role']}  \n"
            f"<small style='opacity:0.55'>{info['dept']}</small>",
            unsafe_allow_html=True,
        )

# =============================================================================
# MAIN TITLE
# =============================================================================
st.title("🏢 AI Agent Team — CEO Dashboard")
st.caption(
    f"**You (Loash)** are CEO · {datetime.now().strftime('%A, %B %d %Y · %I:%M %p')}"
)

# =============================================================================
# TABS — all 5 from the master plan
# =============================================================================
tab_mission, tab_tasks, tab_chat, tab_org, tab_office = st.tabs(
    ["🎯 Mission Control", "📋 Tasks", "💬 Chat", "🏗️ Org Chart", "🏠 Office"]
)

# =============================================================================
# TAB 1 — MISSION CONTROL
# =============================================================================
with tab_mission:
    online_count = sum(1 for a in AGENTS.values() if a["status"] == "online")
    active_tasks = sum(1 for t in st.session_state.tasks if t["status"] == "In Progress")
    critical_count = sum(1 for t in st.session_state.tasks if t["priority"] == "Critical")
    done_count = sum(1 for t in st.session_state.tasks if t["status"] == "Done")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🟢 Agents Online", f"{online_count} / {len(AGENTS)}")
    m2.metric("🔄 Tasks Active", str(active_tasks))
    m3.metric("⚠️ Critical", str(critical_count))
    m4.metric("✅ Completed", str(done_count))

    st.markdown("---")
    st.subheader("Departments")

    dept_cols = st.columns(4)
    for idx, (dept_key, dept_info) in enumerate(DEPARTMENTS.items()):
        members = [n for n, a in AGENTS.items() if a["dept"] == dept_key]
        dept_online = sum(1 for n in members if AGENTS[n]["status"] == "online")
        with dept_cols[idx % 4]:
            st.markdown(
                f'<div style="border-left:4px solid {dept_info["color"]};'
                f'padding:10px 14px;margin-bottom:12px;background:#1a1a2e;'
                f'border-radius:0 8px 8px 0">'
                f'<strong style="color:{dept_info["color"]}">{dept_info["label"]}</strong>'
                f'<span style="float:right;font-size:0.8rem">{dept_online}/{len(members)}</span>'
                f'<br/><span style="font-size:0.82rem;opacity:0.7">{", ".join(members)}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.subheader("Active Agents")

    card_cols = st.columns(4)
    online_agents = [(n, a) for n, a in AGENTS.items() if a["status"] == "online"]
    for idx, (name, info) in enumerate(online_agents):
        with card_cols[idx % 4]:
            st.success(f"**{info['icon']} {name}** · 🟢 Active")
            st.caption(f"{info['role']} — {info['dept']}")

# =============================================================================
# TAB 2 — TASKS (Kanban board)
# =============================================================================
with tab_tasks:
    st.subheader("Task Board")

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
            st.markdown(f"**{status_icons[status]} {status}**")
            tasks_here = [t for t in st.session_state.tasks if t["status"] == status]
            for t in tasks_here:
                pcolor = priority_colors.get(t["priority"], "#888")
                agent_icon = AGENTS.get(t["assignee"], {}).get("icon", "")
                st.markdown(
                    f'<div style="background:#1e1e2e;border:1px solid #333;'
                    f'border-radius:8px;padding:10px;margin-bottom:8px;'
                    f'border-left:3px solid {pcolor}">'
                    f'<strong>{t["title"]}</strong><br/>'
                    f'<span style="font-size:0.75rem;opacity:0.7">'
                    f'{agent_icon} {t["assignee"]} · '
                    f'<span style="color:{pcolor}">{t["priority"]}</span>'
                    f'</span></div>',
                    unsafe_allow_html=True,
                )
            if not tasks_here:
                st.caption("No tasks")

    st.markdown("---")
    st.subheader("Update Task Status")
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
# TAB 3 — CHAT (agent-specific with Claude / Grok)
# =============================================================================
with tab_chat:
    st.subheader("Talk to Your AI Team")

    sel1, sel2, sel3 = st.columns([2, 2, 2])
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
    with sel3:
        ai = AGENTS[agent_choice]
        status_txt = "🟢 Online" if ai["status"] == "online" else "🔴 Offline"
        st.markdown(
            f"**{ai['icon']} {agent_choice}** — {ai['role']}  \n"
            f"<small style='opacity:0.6'>{ai['dept']} · {status_txt}</small>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant" and "agent" in msg:
                a = msg["agent"]
                st.caption(f"{AGENTS.get(a, {}).get('icon', '')} {a}")
            st.markdown(msg["content"])

    if prompt := st.chat_input(f"Message {agent_choice}..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            st.caption(f"{ai['icon']} {agent_choice}")
            with st.spinner(f"{agent_choice} is thinking..."):
                response_text = None
                system_prompt = AGENTS[agent_choice]["prompt"]
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history
                ]

                if "Claude" in model_choice:
                    if not claude_api_key:
                        response_text = (
                            "🔑 **Claude API key not set.**\n\n"
                            "Add it in the sidebar or in Streamlit Cloud → "
                            "Settings → Secrets:\n\n"
                            '```toml\nANTHROPIC_API_KEY = "sk-ant-..."\n```'
                        )
                    else:
                        try:
                            import anthropic
                            client = anthropic.Anthropic(api_key=claude_api_key)
                            resp = client.messages.create(
                                model="claude-sonnet-4-20250514",
                                max_tokens=1024,
                                system=system_prompt,
                                messages=api_messages,
                            )
                            response_text = resp.content[0].text
                        except Exception as e:
                            response_text = f"⚠️ Claude API error:\n\n`{e}`"

                elif "Grok" in model_choice:
                    if not grok_api_key:
                        response_text = (
                            "🔑 **Grok API key not set.**\n\n"
                            "Add it in the sidebar or in Streamlit Cloud → "
                            "Settings → Secrets:\n\n"
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
                                    {"role": "system", "content": system_prompt},
                                    *api_messages,
                                ],
                            )
                            response_text = resp.choices[0].message.content
                        except Exception as e:
                            response_text = f"⚠️ Grok API error:\n\n`{e}`"

                st.markdown(response_text)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "agent": agent_choice,
                })

    cc1, cc2 = st.columns(2)
    with cc1:
        if st.session_state.chat_history and st.button("🗑️ Clear chat"):
            st.session_state.chat_history = []
            st.rerun()
    with cc2:
        if st.session_state.chat_history and st.button("📋 Copy last response"):
            last = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
            if last:
                st.code(last[-1]["content"], language=None)

# =============================================================================
# TAB 4 — ORG CHART (Treemap with all agents)
# =============================================================================
with tab_org:
    st.subheader("Organization Hierarchy")

    labels = [
        "Loash (CEO)",
        "JARVIS (Chief Strategy Officer)",
        "COUNCIL (Advisory)",
        "DEVELOPMENT", "CONTENT", "RESEARCH", "CREATIVE", "PRODUCT",
    ]
    parents = [
        "",
        "Loash (CEO)",
        "Loash (CEO)",
        "Loash (CEO)", "Loash (CEO)", "Loash (CEO)", "Loash (CEO)", "Loash (CEO)",
    ]
    colors = [
        "#6366f1", "#8b5cf6", "#a78bfa",
        "#3b82f6", "#10b981", "#06b6d4", "#f59e0b", "#ef4444",
    ]

    dept_parent_map = {
        "EXECUTIVE": "Loash (CEO)",
        "COUNCIL": "COUNCIL (Advisory)",
        "DEVELOPMENT": "DEVELOPMENT",
        "CONTENT": "CONTENT",
        "RESEARCH": "RESEARCH",
        "CREATIVE": "CREATIVE",
        "PRODUCT": "PRODUCT",
    }

    for name, info in AGENTS.items():
        if name == "JARVIS":
            continue
        display = f"{info['icon']} {name} ({info['role']})"
        labels.append(display)
        parents.append(dept_parent_map.get(info["dept"], "Loash (CEO)"))
        colors.append(info["color"])

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        marker_colors=colors,
        textinfo="label",
        hovertemplate="<b>%{label}</b><extra></extra>",
        pathbar=dict(textfont=dict(size=14)),
    ))
    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        height=550,
        paper_bgcolor="#0e1117",
        font=dict(color="white", size=13),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Click any block to zoom in. Click the header bar to zoom back out.")

# =============================================================================
# TAB 5 — OFFICE (Team overview + Quick actions)
# =============================================================================
with tab_office:
    st.subheader("🏠 The Office — Team Overview")

    office_cols = st.columns(3)
    for idx, (name, info) in enumerate(AGENTS.items()):
        with office_cols[idx % 3]:
            if info["status"] == "online":
                border_color = "#22c55e"
                status_label = "🟢 Online"
            elif info["status"] == "idle":
                border_color = "#f59e0b"
                status_label = "🟡 Idle"
            else:
                border_color = "#ef4444"
                status_label = "🔴 Offline"
            dept_color = DEPARTMENTS.get(info["dept"], {}).get("color", "#666")
            st.markdown(
                f'<div style="background:#1a1a2e;border:1px solid #333;'
                f'border-radius:12px;padding:16px;margin-bottom:12px;'
                f'border-top:3px solid {border_color}">'
                f'<div style="font-size:1.4rem;margin-bottom:4px">{info["icon"]}</div>'
                f'<strong style="font-size:1.1rem">{name}</strong>'
                f'<span style="float:right;font-size:0.8rem">{status_label}</span><br/>'
                f'<span style="opacity:0.7">{info["role"]}</span><br/>'
                f'<span style="display:inline-block;background:{dept_color};'
                f'color:white;padding:2px 10px;border-radius:12px;font-size:0.7rem;'
                f'margin-top:6px;font-weight:600">{info["dept"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.subheader("⚡ Quick Actions")

    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("✍️ Draft a post with SCRIBE", use_container_width=True):
            st.session_state.active_agent = "SCRIBE"
            st.session_state.chat_history = []
            st.info("→ Switched to SCRIBE. Go to the **Chat** tab to start writing!")
    with qa2:
        if st.button("🧑‍💻 Code with CLAWD", use_container_width=True):
            st.session_state.active_agent = "CLAWD"
            st.session_state.chat_history = []
            st.info("→ Switched to CLAWD. Go to the **Chat** tab to start coding!")
    with qa3:
        if st.button("🎬 Clip content with CLIP", use_container_width=True):
            st.session_state.active_agent = "CLIP"
            st.session_state.chat_history = []
            st.info("→ Switched to CLIP. Go to the **Chat** tab and paste your content!")

    qa4, qa5, qa6 = st.columns(3)
    with qa4:
        if st.button("🗺️ Research with ATLAS", use_container_width=True):
            st.session_state.active_agent = "ATLAS"
            st.session_state.chat_history = []
            st.info("→ Switched to ATLAS. Go to the **Chat** tab to start researching!")
    with qa5:
        if st.button("🤔 Challenge idea with SKEPTIC", use_container_width=True):
            st.session_state.active_agent = "SKEPTIC"
            st.session_state.chat_history = []
            st.info("→ Switched to SKEPTIC. Go to the **Chat** tab to stress-test your idea!")
    with qa6:
        if st.button("🎨 Design with PIXEL", use_container_width=True):
            st.session_state.active_agent = "PIXEL"
            st.session_state.chat_history = []
            st.info("→ Switched to PIXEL. Go to the **Chat** tab for design advice!")

    st.markdown("---")
    st.subheader("📊 System Info")

    si1, si2 = st.columns(2)
    with si1:
        st.markdown(
            f"**Total agents:** {len(AGENTS)}  \n"
            f"**Departments:** {len(DEPARTMENTS)}  \n"
            f"**Tasks in queue:** {len(st.session_state.tasks)}  \n"
            f"**Chat messages this session:** {len(st.session_state.chat_history)}"
        )
    with si2:
        claude_status = "✅ Connected" if claude_api_key else "❌ Not set"
        grok_status = "✅ Connected" if grok_api_key else "❌ Not set"
        st.markdown(
            f"**Claude API:** {claude_status}  \n"
            f"**Grok API:** {grok_status}  \n"
            f"**Deployment:** Streamlit Community Cloud  \n"
            f"**Cost:** 100% Free"
        )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption(
    "AI Agent Home Base · Streamlit + Plotly · "
    "Claude (Anthropic) + Grok (xAI) · 100% free · "
    f"v2.0 · {datetime.now().strftime('%Y-%m-%d')}"
)
