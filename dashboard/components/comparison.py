import streamlit as st
import plotly.graph_objects as go


def render_comparison(q):
    st.subheader("⚔️ Actor Comparison")
    st.markdown("Compare two threat actors side by side — shared techniques, unique TTPs, targets.")

    actors = q.get_all_actors()

    if len(actors) < 2:
        st.info("Need at least 2 threat actors in the graph. Ingest more reports first.")
        return

    col1, col2 = st.columns(2)
    with col1:
        actor1 = st.selectbox("🕵️ Actor 1", actors, index=0)
    with col2:
        actor2 = st.selectbox("🕵️ Actor 2", actors, index=1)

    if actor1 == actor2:
        st.warning("Please select two different actors")
        return

    # Get data
    techniques1 = q.get_techniques_by_actor(actor1)
    techniques2 = q.get_techniques_by_actor(actor2)
    targets1 = q.get_targets_by_actor(actor1)
    targets2 = q.get_targets_by_actor(actor2)
    shared = q.get_shared_techniques(actor1, actor2)

    ids1 = set(t["id"] for t in techniques1)
    ids2 = set(t["id"] for t in techniques2)
    shared_ids = set(t["id"] for t in shared)
    unique1 = ids1 - shared_ids
    unique2 = ids2 - shared_ids

    # Top metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(f"🔧 {actor1[:12]} Techniques", len(techniques1))
    with m2:
        st.metric(f"🔧 {actor2[:12]} Techniques", len(techniques2))
    with m3:
        st.metric("🤝 Shared", len(shared))
    with m4:
        overlap = round(len(shared) / max(len(ids1 | ids2), 1) * 100)
        st.metric("📊 Overlap", f"{overlap}%")

    st.markdown("---")

    # Venn-style bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=actor1,
        x=["Unique Techniques", "Shared Techniques", "Targets"],
        y=[len(unique1), len(shared), len(targets1)],
        marker_color="#00ff88"
    ))
    fig.add_trace(go.Bar(
        name=actor2,
        x=["Unique Techniques", "Shared Techniques", "Targets"],
        y=[len(unique2), len(shared), len(targets2)],
        marker_color="#ff6b6b"
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font_color="#ffffff",
        height=350,
        legend=dict(bgcolor="#1a1a2e"),
        xaxis=dict(gridcolor="#222"),
        yaxis=dict(gridcolor="#222")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Side by side detail
    left, middle, right = st.columns(3)

    with left:
        st.markdown(f"#### 🟢 {actor1} Only")
        unique_techniques1 = [t for t in techniques1 if t["id"] in unique1]
        for t in unique_techniques1[:8]:
            st.markdown(f"""
            <div style='background:#1a1a2e; padding:8px; border-radius:6px; margin:3px 0; border-left:3px solid #00ff88;'>
                <b style='color:#00ff88; font-size:12px;'>{t['id']}</b><br>
                <span style='font-size:12px;'>{t['name']}</span>
            </div>
            """, unsafe_allow_html=True)

    with middle:
        st.markdown("#### 🤝 Shared")
        for t in shared[:8]:
            st.markdown(f"""
            <div style='background:#1a1a2e; padding:8px; border-radius:6px; margin:3px 0; border-left:3px solid #ffd93d;'>
                <b style='color:#ffd93d; font-size:12px;'>{t['id']}</b><br>
                <span style='font-size:12px;'>{t['name']}</span>
            </div>
            """, unsafe_allow_html=True)
        if not shared:
            st.info("No shared techniques")

    with right:
        st.markdown(f"#### 🔴 {actor2} Only")
        unique_techniques2 = [t for t in techniques2 if t["id"] in unique2]
        for t in unique_techniques2[:8]:
            st.markdown(f"""
            <div style='background:#1a1a2e; padding:8px; border-radius:6px; margin:3px 0; border-left:3px solid #ff6b6b;'>
                <b style='color:#ff6b6b; font-size:12px;'>{t['id']}</b><br>
                <span style='font-size:12px;'>{t['name']}</span>
            </div>
            """, unsafe_allow_html=True)