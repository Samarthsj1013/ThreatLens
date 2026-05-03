import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


def render_timeline(q):
    st.subheader("📅 Report Ingestion Timeline")
    st.markdown("Track when threat intelligence reports were ingested into ThreatLens.")

    graph_data = q.get_full_graph_data()
    reports = [n for n in graph_data["nodes"] if n["label"] == "Report"]

    if not reports:
        st.info("No reports ingested yet — use the sidebar to ingest reports")
        return

    st.markdown(f"**{len(reports)} reports** in the knowledge base")
    st.markdown("---")

    # Report cards
    for i, report in enumerate(reports):
        name = report.get("name", "Unknown")
        is_pdf = not (name.startswith("http") or name.startswith("https"))
        icon = "📄" if is_pdf else "🌐"
        source_type = "PDF Report" if is_pdf else "Web Article"

        # Truncate long URLs for display
        display_name = name if len(name) <= 80 else name[:77] + "..."

        st.markdown(f"""
        <div style='background:#1a1a2e; padding:15px; border-radius:10px; margin:8px 0;
                    border-left:4px solid {"#6bceff" if is_pdf else "#00ff88"};
                    display:flex; align-items:center; gap:15px;'>
            <span style='font-size:24px;'>{icon}</span>
            <div>
                <b style='color:{"#6bceff" if is_pdf else "#00ff88"};'>{source_type}</b><br>
                <span style='color:#ccc; font-size:13px;'>{display_name}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats breakdown
    pdf_count = sum(1 for r in reports if not (r.get("name", "").startswith("http")))
    url_count = len(reports) - pdf_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 PDF Reports", pdf_count)
    with col2:
        st.metric("🌐 Web Articles", url_count)
    with col3:
        actors = q.get_all_actors()
        st.metric("🕵️ Actors Tracked", len(actors))

    # Source type pie chart
    if pdf_count > 0 or url_count > 0:
        fig = go.Figure(go.Pie(
            labels=["PDF Reports", "Web Articles"],
            values=[pdf_count, url_count],
            hole=0.5,
            marker_colors=["#6bceff", "#00ff88"]
        ))
        fig.update_layout(
            paper_bgcolor="#0e1117",
            font_color="#ffffff",
            height=300,
            showlegend=True,
            legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig, use_container_width=True)