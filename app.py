import streamlit as st
import json as _json
import re
from datetime import datetime

st.set_page_config(page_title="AI Agent Home Base", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# === PASSWORD GATE ===
def check_password():
    correct_pw = ""
    try: correct_pw = st.secrets.get("APP_PASSWORD", "")
    except Exception: pass
    if not correct_pw: return True
    if st.session_state.get("authenticated", False): return True
    st.markdown('<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:60vh;text-align:center"><div style="font-size:3rem;margin-bottom:10px">🏢</div><div style="font-size:1.5rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">AI Agent Home Base</div><div style="font-size:0.8rem;color:#64748b;margin-bottom:30px">CEO Access Required</div></div>', unsafe_allow_html=True)
    pw = st.text_input("Enter password", type="password", key="pw_input")
    if st.button("Unlock", use_container_width=True):
        if pw == correct_pw:
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("Wrong password")
    st.stop()

if not check_password(): st.stop()

# === CLEAN CSS ===
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
.stApp{background:#0a0a0f;color:#e2e8f0;font-family:'Inter',sans-serif}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:#0f0f18;border-right:1px solid #1e1e2e}
.block-container{padding-top:1rem;max-width:1200px}
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:0;border-bottom:1px solid #1e1e2e}
[data-testid="stTabs"] [data-baseweb="tab"]{font-family:'Inter',sans-serif;font-size:.85rem;font-weight:500;color:#64748b;padding:10px 20px;border-bottom:2px solid transparent}
[data-testid="stTabs"] [aria-selected="true"]{color:#e2e8f0;border-bottom-color:#8b5cf6}
.app-header{display:flex;align-items:center;justify-content:space-between;padding:8px 0 16px 0;border-bottom:1px solid #1e1e2e;margin-bottom:16px}
.app-title{font-size:1.1rem;font-weight:700;color:#e2e8f0}
.app-subtitle{font-size:.75rem;color:#64748b}
.status-pill{display:inline-block;padding:3px 10px;border-radius:12px;font-size:.7rem;font-weight:500;background:#22c55e15;color:#22c55e;border:1px solid #22c55e30}
.j-msg-user{background:#1e1e2e;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:6px 0;font-size:.9rem;line-height:1.6;max-width:85%;margin-left:auto;color:#e2e8f0}
.j-msg-bot{background:#12121e;border:1px solid #1e1e2e;border-radius:12px 12px 12px 4px;padding:12px 16px;margin:6px 0;font-size:.9rem;line-height:1.6;max-width:90%;color:#cbd5e1}
.j-label{font-size:.65rem;font-weight:600;color:#8b5cf6;margin-bottom:2px;letter-spacing:.05em}
.j-label-user{font-size:.65rem;font-weight:600;color:#64748b;margin-bottom:2px;letter-spacing:.05em;text-align:right}
.op-card{background:#12121e;border:1px solid #1e1e2e;border-radius:10px;padding:16px;margin:8px 0}
.op-card:hover{border-color:#8b5cf630}
.op-metric{font-size:1.5rem;font-weight:700;color:#e2e8f0}
.op-metric-label{font-size:.65rem;color:#64748b;text-transform:uppercase;letter-spacing:.05em}
.op-card-title{font-size:.85rem;font-weight:600;color:#e2e8f0;margin-bottom:4px}
.op-card-sub{font-size:.73rem;color:#64748b;line-height:1.5}
.dispatch-card{background:#8b5cf608;border:1px solid #8b5cf620;border-radius:8px;padding:10px 14px;margin:6px 0;font-size:.82rem}
.dispatch-agent{font-weight:600;color:#8b5cf6}
.pipeline{display:flex;align-items:center;gap:8px;margin:12px 0;flex-wrap:wrap}
.pipe-dot{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.8rem;border:2px solid #1e1e2e}
.pipe-line{width:20px;height:2px;background:#1e1e2e}
.divider{height:1px;background:#1e1e2e;margin:16px 0}
#MainMenu,footer,[data-testid="stDecoration"],div[data-testid="stStatusWidget"]{display:none}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#12121e!important;border-color:#1e1e2e!important;color:#e2e8f0!important;font-family:'Inter',sans-serif!important;border-radius:8px!important}
.stSelectbox>div>div{background:#12121e!important;border-color:#1e1e2e!important}
button[kind="primary"],.stButton>button{background:#8b5cf6!important;color:white!important;border:none!important;border-radius:8px!important;font-family:'Inter',sans-serif!important;font-weight:500!important;font-size:.8rem!important}
button[kind="primary"]:hover,.stButton>button:hover{background:#7c3aed!important}
.stExpander{border-color:#1e1e2e!important}
</style>""", unsafe_allow_html=True)

# === AGENTS ===
AGENTS = {
    "JARVIS":{"role":"Chief Strategy Officer","dept":"EXECUTIVE","status":"online","icon":"🤖","color":"#8b5cf6","prompt":"You are JARVIS, Loash's Chief Strategy Officer. Oversee all agents. Be executive-level, concise, actionable."},
    "GROWTH":{"role":"Growth Advisor","dept":"COUNCIL","status":"online","icon":"📈","color":"#a78bfa","prompt":"You are GROWTH. Focus on growth strategy and user acquisition for CEO Loash."},
    "RETENTION":{"role":"Retention Advisor","dept":"COUNCIL","status":"online","icon":"🔄","color":"#a78bfa","prompt":"You are RETENTION. Focus on keeping users and reducing churn for CEO Loash."},
    "SKEPTIC":{"role":"Devil's Advocate","dept":"COUNCIL","status":"online","icon":"🤔","color":"#a78bfa","prompt":"You are SKEPTIC. Challenge assumptions, find flaws, stress-test ideas for CEO Loash."},
    "CLAWD":{"role":"Senior Developer","dept":"DEVELOPMENT","status":"online","icon":"🧑‍💻","color":"#3b82f6","prompt":"You are CLAWD, senior full-stack developer. Write clean production-ready code for CEO Loash."},
    "SENTINEL":{"role":"QA Monitor","dept":"DEVELOPMENT","status":"online","icon":"🛡️","color":"#3b82f6","prompt":"You are SENTINEL, QA/security monitor. Review code for bugs and security for CEO Loash."},
    "SCRIBE":{"role":"Content Director","dept":"CONTENT","status":"online","icon":"✍️","color":"#10b981","prompt":"You are SCRIBE, content director. Write polished, ready-to-publish content for CEO Loash."},
    "ATLAS":{"role":"Research Analyst","dept":"RESEARCH","status":"online","icon":"🗺️","color":"#06b6d4","prompt":"You are ATLAS, research analyst. Research deeply and present actionable insights for CEO Loash."},
    "TRENDY":{"role":"Viral Scout","dept":"RESEARCH","status":"online","icon":"🔥","color":"#06b6d4","prompt":"You are TRENDY, viral trend scout. Identify trending topics and viral formats for CEO Loash."},
    "PIXEL":{"role":"Lead Designer","dept":"CREATIVE","status":"online","icon":"🎨","color":"#f59e0b","prompt":"You are PIXEL, lead designer. Design UI/UX, branding, visuals with specific details for CEO Loash."},
    "NOVA":{"role":"Production Lead","dept":"CREATIVE","status":"online","icon":"💡","color":"#f59e0b","prompt":"You are NOVA, production lead. Manage timelines, assets, workflows for CEO Loash."},
    "VIBE":{"role":"Motion Designer","dept":"CREATIVE","status":"online","icon":"✨","color":"#f59e0b","prompt":"You are VIBE, motion designer. Create animation/motion concepts for CEO Loash."},
    "CLIP":{"role":"Clipping Agent","dept":"PRODUCT","status":"online","icon":"🎬","color":"#ef4444","prompt":"You are CLIP, clipping agent. Extract best clips, highlights, quotable moments for CEO Loash."},
}

# === SESSION STATE ===
for k, v in {"jarvis_chat": [], "agent_chats": {n: [] for n in AGENTS}, "leads": [], "activity_log": []}.items():
    if k not in st.session_state: st.session_state[k] = v
if "shared_memory" not in st.session_state:
    st.session_state.shared_memory = {
        "ceo_name":"Loash",
        "business":"AI Agent Home Base — CEO dashboard with 13 AI agents",
        "goals":["Build wealth through automation","Create the most useful AI assistant","Automate lead generation"],
        "preferences":["Concise communication","Free tools over paid","Wants deliverables not advice","Needs numbered steps"],
        "active_projects":["AI Agent Home Base (Streamlit Cloud)","Lead Engine pipeline","Discord integration"],
        "facts":[],
    }

# === API KEYS ===
claude_api_key = ""
grok_api_key = ""
try: claude_api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
except: pass
try: grok_api_key = st.secrets.get("XAI_API_KEY", "")
except: pass

# === DISCORD ===
DISCORD_WEBHOOKS = {}
DEPT_TO_CHANNEL = {"EXECUTIVE":"jarvis-briefings","COUNCIL":"council-decisions","CONTENT":"content-pipeline","DEVELOPMENT":"dev-updates","RESEARCH":"research-intel","CREATIVE":"creative-assets","PRODUCT":"creative-assets"}
for sk, ch in {"DISCORD_JARVIS":"jarvis-briefings","DISCORD_COUNCIL":"council-decisions","DISCORD_CONTENT":"content-pipeline","DISCORD_DEV":"dev-updates","DISCORD_RESEARCH":"research-intel","DISCORD_CREATIVE":"creative-assets","DISCORD_TASKS":"task-completions","DISCORD_APPROVALS":"ceo-approvals"}.items():
    try: DISCORD_WEBHOOKS[ch] = st.secrets.get(sk, "")
    except: pass

def _send_discord(channel, title, message, agent_name="SYSTEM", color=0x8b5cf6):
    import requests as req
    url = DISCORD_WEBHOOKS.get(channel, "")
    if not url: return False
    if len(message) > 3800: message = message[:3800] + "\n\n*...truncated*"
    ai = AGENTS.get(agent_name, {})
    try:
        return req.post(url, json={"username":"AI Agent Home Base","embeds":[{"title":f"{ai.get('icon','🤖')} {title}","description":message,"color":color,"footer":{"text":f"{agent_name} · {datetime.now().strftime('%b %d %I:%M %p')}"}}]}, timeout=10).status_code in (200, 204)
    except: return False

# === SHARED MEMORY + LLM ===
def _mem_ctx():
    m = st.session_state.shared_memory
    s = f"=== KNOWLEDGE BASE ===\nCEO: {m['ceo_name']}\nBusiness: {m['business']}\nGoals: {'; '.join(m['goals'])}\nPreferences: {'; '.join(m['preferences'])}\nProjects: {'; '.join(m['active_projects'])}\n"
    if m.get("facts"): s += f"Facts: {'; '.join(m['facts'][-10:])}\n"
    return s + "=== END ===\n\n"

def _call_llm(agent_name, history, custom_system=None):
    base = custom_system or AGENTS[agent_name]["prompt"]
    system = _mem_ctx() + base + "\n\nCRITICAL: Produce REAL deliverables. Never say 'I cannot' or 'as an AI'. Do the work. CEO needs results."
    msgs = [{"role":m["role"],"content":m["content"]} for m in history]
    mc = st.session_state.get("model_choice", "Claude")
    if "Claude" in mc and claude_api_key:
        try:
            import anthropic
            return anthropic.Anthropic(api_key=claude_api_key).messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, system=system, messages=msgs).content[0].text
        except Exception as e: return f"⚠️ Error: {e}"
    elif "Grok" in mc and grok_api_key:
        try:
            from openai import OpenAI
            return OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1").chat.completions.create(model="grok-3-latest", messages=[{"role":"system","content":system}, *msgs]).choices[0].message.content
        except Exception as e: return f"⚠️ Error: {e}"
    return "⚠️ No API key set. Open Settings (☰ top-left) to configure."

def _log(agent, action, detail=""):
    st.session_state.activity_log.insert(0, {"time":datetime.now().strftime("%H:%M"),"agent":agent,"action":action,"detail":detail[:200]})
    if len(st.session_state.activity_log) > 50: st.session_state.activity_log = st.session_state.activity_log[:50]

# === JARVIS BRAIN ===
JARVIS_SYS = (
    "You are J.A.R.V.I.S., CEO Loash's Chief Strategy Officer and central intelligence of AI Agent Home Base.\n\n"
    "DETERMINE INTENT:\n"
    "CONVERSATION — chatting, venting, ideas → respond naturally as trusted advisor.\n"
    "INFORMATION — question/advice → give direct answer with actionable steps.\n"
    "TASK — something needs to be DONE → identify what, then use DISPATCH tags.\n\n"
    "FOR TASKS: Use [DISPATCH:AGENT_NAME] task description\n"
    "Example: [DISPATCH:SCRIBE] Write a Twitter thread about AI dashboards\n"
    "For chains: multiple DISPATCH lines in order. Each agent auto-executes.\n\n"
    "AGENTS: GROWTH (growth), RETENTION (retention), SKEPTIC (challenge ideas), "
    "CLAWD (code), SENTINEL (security), SCRIBE (content), ATLAS (research), "
    "TRENDY (trends), PIXEL (design), NOVA (production), VIBE (motion), CLIP (clips)\n\n"
    "RULES: Address Loash by name. Be concise. Never say 'I cannot'. Always use DISPATCH for tasks. "
    "Produce real work, not descriptions of what could be done."
)

# === HEADER ===
online = sum(1 for a in AGENTS.values() if a["status"]=="online")
st.markdown(f'<div class="app-header"><div><div class="app-title">🏢 AI Agent Home Base</div><div class="app-subtitle">CEO Dashboard · {datetime.now().strftime("%A %b %d")}</div></div><div><span class="status-pill">{online}/{len(AGENTS)} online</span></div></div>', unsafe_allow_html=True)

# === SIDEBAR SETTINGS ===
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("**API Keys**")
    nk1 = st.text_input("Anthropic (Claude)", value=claude_api_key, type="password", key="sk1")
    nk2 = st.text_input("xAI (Grok)", value=grok_api_key, type="password", key="sk2")
    if nk1: claude_api_key = nk1
    if nk2: grok_api_key = nk2
    st.caption(f"{'✅' if claude_api_key else '⚠️'} Claude · {'✅' if grok_api_key else '⚠️'} Grok")
    st.selectbox("Model", ["Claude (Anthropic)", "Grok (xAI)"], key="model_choice")
    st.markdown("---")
    st.markdown("**🧠 Knowledge Base**")
    mem = st.session_state.shared_memory
    g = st.text_area("Goals", "\n".join(mem["goals"]), height=60, key="sg")
    p = st.text_area("Preferences", "\n".join(mem["preferences"]), height=60, key="sp")
    pr = st.text_area("Projects", "\n".join(mem["active_projects"]), height=60, key="spr")
    f = st.text_area("Notes", "\n".join(mem.get("facts",[])), height=50, key="sf")
    if st.button("💾 Save", use_container_width=True):
        mem["goals"]=[x.strip() for x in g.split("\n") if x.strip()]
        mem["preferences"]=[x.strip() for x in p.split("\n") if x.strip()]
        mem["active_projects"]=[x.strip() for x in pr.split("\n") if x.strip()]
        mem["facts"]=[x.strip() for x in f.split("\n") if x.strip()]
        st.success("✅ Saved")
    st.markdown("---")
    for n, info in AGENTS.items():
        st.caption(f"{'🟢' if info['status']=='online' else '🔴'} {info['icon']} **{n}** — {info['role']}")

# === TABS ===
tab_j, tab_ops, tab_leads = st.tabs(["💬 JARVIS", "📊 Operations", "🏭 Lead Engine"])

# === TAB 1: JARVIS ===
with tab_j:
    jc1, jc2, jc3 = st.columns([1,4,1])
    with jc1:
        voice_on = st.toggle("🔊", value=False, key="voice_on")
    with jc3:
        if st.button("Clear", key="clr"):
            st.session_state.jarvis_chat = []
            st.rerun()

    if not st.session_state.jarvis_chat:
        st.markdown('<div style="text-align:center;padding:40px 0"><div style="font-size:2.5rem;margin-bottom:8px">🤖</div><div style="font-size:1rem;font-weight:600;color:#e2e8f0">Hey Loash.</div><div style="font-size:.8rem;color:#64748b;margin-top:4px">Talk to me about anything — life, business, ideas. Or give me a task and I\'ll dispatch the right agents.</div></div>', unsafe_allow_html=True)
    else:
        for msg in st.session_state.jarvis_chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="j-label-user">YOU</div><div class="j-msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="j-label">J.A.R.V.I.S.</div><div class="j-msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)

    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        if st.button("📋 Brief", key="q1", use_container_width=True):
            st.session_state.jarvis_chat.append({"role":"user","content":"Give me today's briefing — what should I focus on?"})
            st.rerun()
    with qa2:
        if st.button("🔍 Leads", key="q2", use_container_width=True):
            st.session_state.jarvis_chat.append({"role":"user","content":"Scout 5 restaurant leads in Vancouver, BC and audit their websites"})
            st.rerun()
    with qa3:
        if st.button("✍️ Content", key="q3", use_container_width=True):
            st.session_state.jarvis_chat.append({"role":"user","content":"Write a Twitter thread about AI assistants replacing traditional business tools"})
            st.rerun()
    with qa4:
        if st.button("💡 Idea", key="q4", use_container_width=True):
            st.session_state.jarvis_chat.append({"role":"user","content":"I have a new business idea — help me think through it"})
            st.rerun()

    user_input = st.chat_input("Talk to JARVIS...")

    if user_input:
        st.session_state.jarvis_chat.append({"role":"user","content":user_input})
        # Memory learning
        if any(t in user_input.lower() for t in ["my name is","i prefer","i like","remember that","note that","from now on"]):
            st.session_state.shared_memory["facts"].append(user_input[:200])

        j_hist = [{"role":m["role"],"content":m["content"]} for m in st.session_state.jarvis_chat]
        j_resp = _call_llm("JARVIS", j_hist, custom_system=JARVIS_SYS)
        st.session_state.jarvis_chat.append({"role":"assistant","content":j_resp})
        _log("JARVIS","Responded",j_resp[:100])

        # DISPATCH
        dispatches = re.findall(r'\[DISPATCH:(\w+)\]\s*(.+)', j_resp)
        if dispatches:
            prev = ""
            dispatch_summary = "\n\n---\n\n"
            for idx,(dag,dtask) in enumerate(dispatches):
                dag = dag.strip().upper()
                if dag not in AGENTS: continue
                ai = AGENTS[dag]
                _log(dag, "Dispatched", dtask[:100])
                if prev and idx > 0:
                    prompt = f"Task (step {idx+1}/{len(dispatches)}): {dtask}\n\nPrevious output:\n{prev[:3000]}\n\nBuild on it."
                else:
                    prompt = f"CEO Loash assigned: {dtask}\n\nProduce a complete deliverable."
                result = _call_llm(dag, [{"role":"user","content":prompt}])
                prev = result
                st.session_state.agent_chats[dag].append({"role":"user","content":prompt[:500]})
                st.session_state.agent_chats[dag].append({"role":"assistant","content":result})
                ch = DEPT_TO_CHANNEL.get(ai.get("dept","EXECUTIVE"), "task-completions")
                _send_discord(ch, f"{ai['icon']} {dag}: {dtask[:80]}", result[:3800], dag)
                _send_discord("task-completions", f"✅ {dtask[:80]}", f"**{dag}**\n\n{result[:2000]}", dag, 0x22c55e)
                _log(dag, "Completed", dtask[:100])
                dispatch_summary += f"**{ai['icon']} {dag}** — {dtask}\n\n{result}\n\n---\n\n"
            dispatch_summary += "✅ *Deliverables sent to Discord.*"
            st.session_state.jarvis_chat.append({"role":"assistant","content":dispatch_summary})

        # Voice
        if voice_on and j_resp:
            clean = re.sub(r'[*#`\[\]]','',j_resp).replace("\n"," ").strip()
            if len(clean)>800: clean=clean[:800]+"..."
            try:
                import edge_tts,asyncio,base64,tempfile,os
                async def _s(t,v,o):
                    await edge_tts.Communicate(t,v).save(o)
                with tempfile.NamedTemporaryFile(suffix=".mp3",delete=False) as tmp: tp=tmp.name
                asyncio.run(_s(clean,"en-GB-RyanNeural",tp))
                with open(tp,"rb") as ff: ab=ff.read()
                os.unlink(tp)
                if ab: st.components.v1.html(f'<audio autoplay><source src="data:audio/mpeg;base64,{base64.b64encode(ab).decode()}" type="audio/mpeg"></audio>',height=0)
            except: pass

        st.rerun()

# === TAB 2: OPERATIONS ===
with tab_ops:
    m1,m2,m3,m4 = st.columns(4)
    total_msgs = sum(len(v) for v in st.session_state.agent_chats.values())
    dc_count = sum(1 for v in DISCORD_WEBHOOKS.values() if v)
    with m1: st.markdown(f'<div class="op-card"><div class="op-metric">{online}</div><div class="op-metric-label">Agents Online</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="op-card"><div class="op-metric">{total_msgs}</div><div class="op-metric-label">Messages</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="op-card"><div class="op-metric">{len(st.session_state.leads)}</div><div class="op-metric-label">Leads</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="op-card"><div class="op-metric">{dc_count}/8</div><div class="op-metric-label">Discord</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    cl, cr = st.columns([3,2])
    with cl:
        st.markdown("**Recent Activity**")
        if not st.session_state.activity_log: st.caption("No activity yet.")
        for log in st.session_state.activity_log[:15]:
            ai=AGENTS.get(log["agent"],{})
            st.markdown(f'<div style="padding:6px 0;border-bottom:1px solid #1e1e2e;font-size:.8rem"><span style="color:#64748b">{log["time"]}</span> {ai.get("icon","🤖")} <span style="color:{ai.get("color","#8b5cf6")};font-weight:600">{log["agent"]}</span> {log["action"]} <span style="color:#64748b">— {log["detail"]}</span></div>', unsafe_allow_html=True)
    with cr:
        st.markdown("**Agent History**")
        for name, info in AGENTS.items():
            msgs = st.session_state.agent_chats.get(name,[])
            if msgs:
                with st.expander(f"{info['icon']} {name} ({len(msgs)} msgs)"):
                    for mm in msgs[-6:]:
                        st.caption(f"**{'You' if mm['role']=='user' else name}:** {mm['content'][:300]}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**🧠 Knowledge Base** *(edit in Settings ☰)*")
    mem=st.session_state.shared_memory
    k1,k2,k3=st.columns(3)
    with k1: st.markdown(f'<div class="op-card"><div class="op-card-title">Goals</div><div class="op-card-sub">{"<br>".join("• "+g for g in mem["goals"])}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="op-card"><div class="op-card-title">Projects</div><div class="op-card-sub">{"<br>".join("• "+p for p in mem["active_projects"])}</div></div>', unsafe_allow_html=True)
    with k3:
        fh="<br>".join("• "+ff for ff in mem.get("facts",[])[-5:]) if mem.get("facts") else "No notes yet"
        st.markdown(f'<div class="op-card"><div class="op-card-title">Notes</div><div class="op-card-sub">{fh}</div></div>', unsafe_allow_html=True)

# === TAB 3: LEAD ENGINE ===
with tab_leads:
    st.markdown('<div class="pipeline"><div class="pipe-dot" style="border-color:#22c55e;background:#22c55e15">🔍</div><div class="pipe-line"></div><div class="pipe-dot">🕵️</div><div class="pipe-line"></div><div class="pipe-dot">🏗️</div><div class="pipe-line"></div><div class="pipe-dot">📧</div><div class="pipe-line"></div><div class="pipe-dot">💰</div><span style="margin-left:12px;font-size:.75rem;color:#64748b">Scout → Intel → Builder → Outreach → Closer</span></div>', unsafe_allow_html=True)

    lc1, lc2 = st.columns([2,3])
    with lc1:
        st.markdown("**Find Leads**")
        with st.form("sf"):
            loc=st.text_input("Location",placeholder="Vancouver, BC",key="sl")
            ind=st.text_input("Industry",placeholder="restaurants, dentists...",key="si")
            cnt=st.slider("Count",3,10,5,key="sc")
            go=st.form_submit_button("🔍 Scout",use_container_width=True)
        if go and loc and ind:
            with st.spinner("Scouting..."):
                r=_call_llm("JARVIS",[{"role":"user","content":f"Find {cnt} real {ind} in {loc}. Return ONLY JSON: "+'[{"name":"...","description":"...","website":"...","opportunity":"..."}]'}])
                try:
                    raw=r.strip()
                    if "```" in raw:
                        raw=raw.split("```")[1]
                        if raw.startswith("json"): raw=raw[4:]
                    lds=_json.loads(raw.strip())
                    for l in lds: l["status"]="scouted";l["score"]=None
                    st.session_state.leads.extend(lds)
                    _log("SCOUT","Found",f"{len(lds)} in {loc}")
                    _send_discord("research-intel",f"🔍 {len(lds)} leads in {loc}",", ".join(l["name"] for l in lds),"SCOUT",0x22c55e)
                    st.rerun()
                except: st.warning("Parse error:"); st.markdown(r)

    with lc2:
        st.markdown(f"**Leads** ({len(st.session_state.leads)})")
        if not st.session_state.leads: st.caption("No leads yet.")
        for i,lead in enumerate(st.session_state.leads):
            sd={"scouted":"🟡","audited":"🟢","demo_ready":"🔵","pitch_ready":"🟣","pitch_approved":"✅","closed_won":"💰"}.get(lead.get("status"),"⚪")
            sc=f" · {lead['score']}/100" if lead.get("score") else ""
            with st.expander(f"{sd} {lead['name']}{sc}"):
                st.caption(f"{lead.get('website','No site')} · {lead.get('status','?')}")
                st.caption(lead.get("description",""))
                b1,b2,b3=st.columns(3)

                if lead["status"]=="scouted" and lead.get("website","unknown")!="unknown":
                    with b1:
                        if st.button("🕵️ Audit",key=f"a{i}",use_container_width=True):
                            with st.spinner("Auditing..."):
                                psi={}
                                try:
                                    import requests as req
                                    rr=req.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={lead['website']}&strategy=mobile",timeout=30)
                                    if rr.status_code==200:
                                        lh=rr.json().get("lighthouseResult",{}).get("categories",{})
                                        psi={k:round((lh.get(k,{}).get("score",0) or 0)*100) for k in ["performance","accessibility","seo"]}
                                except: pass
                                brief=_call_llm("JARVIS",[{"role":"user","content":f"Sales brief for {lead['name']} ({lead.get('website')}). PageSpeed: {_json.dumps(psi)}. Include Pain Summary, Score Card, Money Lost, Quick Wins, Pitch Angle. Conversational, not technical."}])
                                lead.update({"status":"audited","score":psi.get("performance",0),"psi":psi,"intel":brief})
                                _log("INTEL","Audited",lead["name"])
                                _send_discord("research-intel",f"🕵️ {lead['name']}",brief[:2000],"INTEL",0x3b82f6)
                                st.rerun()

                elif lead["status"]=="audited":
                    with b1:
                        if st.button("🏗️ Demo",key=f"b{i}",use_container_width=True):
                            with st.spinner("Building..."):
                                h=_call_llm("JARVIS",[{"role":"user","content":f"Create complete single-page HTML site for {lead['name']}. {lead.get('description','')}. Modern, responsive, all CSS inline. placehold.co for images. Return ONLY HTML from <!DOCTYPE html>."}])
                                code=h.strip()
                                if "```" in code:
                                    for pp in code.split("```"):
                                        if "<!DOCTYPE" in pp or "<html" in pp: code=pp.strip().lstrip("html").strip(); break
                                lead.update({"demo_html":code,"status":"demo_ready"})
                                _log("BUILDER","Built",lead["name"])
                                st.rerun()

                elif lead["status"]=="demo_ready":
                    with b1:
                        if st.button("📧 Pitch",key=f"p{i}",use_container_width=True):
                            with st.spinner("Drafting..."):
                                pt=_call_llm("JARVIS",[{"role":"user","content":f"Pitch email for {lead['name']}. Score: {lead.get('score','?')}/100. Intel: {lead.get('intel','')[:500]}. Under 150 words, human feel. Include SUBJECT, EMAIL, SMS (160 chars). Reference their problems, mention free demo."}])
                                lead.update({"pitch":pt,"status":"pitch_ready"})
                                _log("OUTREACH","Drafted",lead["name"])
                                st.rerun()

                elif lead["status"]=="pitch_ready":
                    st.markdown(lead.get("pitch",""))
                    with b1:
                        if st.button("✅ Approve",key=f"ap{i}",use_container_width=True):
                            lead["status"]="pitch_approved"
                            _send_discord("ceo-approvals",f"✅ {lead['name']}",lead.get("pitch","")[:2000],"OUTREACH",0xf59e0b)
                            _log("CEO","Approved",lead["name"]); st.rerun()
                    with b2:
                        if st.button("🔄 Redo",key=f"rd{i}",use_container_width=True):
                            lead.update({"status":"demo_ready","pitch":None}); st.rerun()

                elif lead["status"]=="pitch_approved":
                    with b1:
                        if st.button("💰 Won!",key=f"w{i}",use_container_width=True):
                            lead["status"]="closed_won"
                            _send_discord("task-completions",f"💰 {lead['name']}","Client converted!","CLOSER",0x22c55e)
                            _log("CLOSER","Closed",lead["name"]); st.balloons(); st.rerun()

                if lead.get("psi"):
                    pp=lead["psi"]; st.caption(f"Perf: {pp.get('performance','?')} · SEO: {pp.get('seo','?')} · Access: {pp.get('accessibility','?')}")
                if lead.get("intel"): st.markdown(lead["intel"][:1000])
                if lead.get("demo_html"):
                    if st.button("👁️ Preview",key=f"pv{i}"): st.components.v1.html(lead["demo_html"],height=500,scrolling=True)

        if st.session_state.leads and st.button("🗑️ Clear leads"):
            st.session_state.leads=[]; st.rerun()
