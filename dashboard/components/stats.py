import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def render_stats(q):
    st.subheader("📊 Threat Intelligence Overview")

    # Top metrics
    actors = q.get_all_actors()
    top_techniques = q.get_top_techniques(limit=10)
    graph_data = q.get_full_graph_data()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🕵️ Threat Actors", len(actors))
    with col2:
        st.metric("🔧 Techniques", len(top_techniques))
    with col3:
        st.metric("🗂️ Graph Nodes", len(graph_data["nodes"]))
    with col4:
        st.metric("🔗 Relationships", len(graph_data["edges"]))

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🔥 Top Techniques by Actor Count")
        if top_techniques:
            df = pd.DataFrame(top_techniques)
            fig = px.bar(
                df,
                x="actor_count",
                y="name",
                orientation="h",
                color="actor_count",
                color_continuous_scale="Viridis",
                labels={"actor_count": "Actor Count", "name": "Technique"}
            )
            fig.update_layout(
                paper_bgcolor="#0e1117",
                plot_bgcolor="#0e1117",
                font_color="#ffffff",
                height=400,
                showlegend=False,
                coloraxis_showscale=False
            )
            fig.update_xaxes(gridcolor="#333")
            fig.update_yaxes(gridcolor="#333")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No techniques yet — ingest a report first")

    with col_right:
        st.markdown("#### 🎯 Threat Actors")
        if actors:
            for actor in actors:
                techniques = q.get_techniques_by_actor(actor)
                targets = q.get_targets_by_actor(actor)
                st.markdown(f"""
                <div style='background:#1a1a2e; padding:15px; border-radius:10px; margin:8px 0; border-left:4px solid #00ff88;'>
                    <b style='color:#00ff88; font-size:16px;'>🕵️ {actor}</b><br>
                    <small style='color:#aaa;'>
                        🔧 {len(techniques)} techniques &nbsp;|&nbsp; 🎯 {len(targets)} targets
                    </small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No actors yet — ingest a report first")

    st.markdown("---")
    st.markdown("#### 🗺️ Tactic Coverage")

    if top_techniques:
        tactic_counts = {}
        for t in top_techniques:
            tactics_str = t.get("tactics") or ""
            if isinstance(tactics_str, str) and tactics_str:
                for tactic in tactics_str.split(","):
                    tactic = tactic.strip()
                    if tactic:
                        tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1

        if tactic_counts:
            fig2 = go.Figure(go.Pie(
                labels=list(tactic_counts.keys()),
                values=list(tactic_counts.values()),
                hole=0.4,
                marker_colors=px.colors.sequential.Viridis
            ))
            fig2.update_layout(
                paper_bgcolor="#0e1117",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No tactic data available yet")