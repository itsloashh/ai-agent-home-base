import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="AI Agent Home Base - CEO View", layout="wide")

st.title("AI Agent Team - CEO Dashboard")
st.markdown("**You (Loash)** are CEO. Below is your current team hierarchy.")

# Simple tree data mimicking your photo
fig = go.Figure(go.Treemap(
    labels = [
        "Loash (CEO)",
        "JARVIS (Chief Strategy Officer)",
        "COUNCIL (Advisory)",
        "DEVELOPMENT", "CONTENT", "RESEARCH", "CREATIVE", "PRODUCT",
        "CLAWD (Senior Developer)", "SENTINEL (QA Monitor)",
        "SCRIBE (Content Director)", "CLIP (Clipping Agent)",
        "ATLAS (Research Analyst)", "TRENDY (Viral Scout)",
        "PIXEL (Lead Designer)", "NOVA (Production Lead)", "VIBE (Motion Designer)"
    ],
    parents = [
        "", 
        "Loash (CEO)", 
        "Loash (CEO)",
        "Loash (CEO)", "Loash (CEO)", "Loash (CEO)", "Loash (CEO)", "Loash (CEO)",
        "DEVELOPMENT", "DEVELOPMENT",
        "CONTENT",
        "PRODUCT",
        "RESEARCH", "RESEARCH",
        "CREATIVE", "CREATIVE", "CREATIVE"
    ],
    marker_colors = ["#1f77b4"] * 17  # blue theme; can customize later
))

fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Active Agents")
cols = st.columns(3)
with cols[0]:
    st.success("CLAWD · Active")
    st.info("Full-stack dev")
with cols[1]:
    st.success("SCRIBE · Active")
    st.info("Content creation")
with cols[2]:
    st.warning("CLIP · Idle")
    st.info("Video clipping")
