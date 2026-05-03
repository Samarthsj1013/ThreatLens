import streamlit as st


def render_search(q):
    st.subheader("🔎 Search Knowledge Graph")

    search_query = st.text_input(
        "Search actors, techniques, or targets",
        placeholder="e.g. PowerShell, APT28, ransomware, lateral movement..."
    )

    if not search_query or len(search_query) < 2:
        st.info("Type at least 2 characters to search")
        return

    query = search_query.strip().lower()
    results = {"actors": [], "techniques": [], "targets": []}

    # Search actors
    all_actors = q.get_all_actors()
    results["actors"] = [a for a in all_actors if query in a.lower()]

    # Search techniques
    top_techniques = q.get_top_techniques(limit=100)
    results["techniques"] = [
        t for t in top_techniques
        if query in t["name"].lower() or query in t["id"].lower()
    ]

    # Search targets
    graph_data = q.get_full_graph_data()
    all_targets = [n for n in graph_data["nodes"] if n["label"] == "Target"]
    results["targets"] = [
        t for t in all_targets
        if t["name"] and query in t["name"].lower()
    ]

    total = len(results["actors"]) + len(results["techniques"]) + len(results["targets"])

    if total == 0:
        st.warning(f"No results found for **'{search_query}'**")
        return

    st.markdown(f"**{total} results** for `{search_query}`")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🕵️ Threat Actors")
        if results["actors"]:
            for actor in results["actors"]:
                techniques = q.get_techniques_by_actor(actor)
                st.markdown(f"""
                <div style='background:#1a1a2e; padding:12px; border-radius:8px; margin:5px 0; border-left:3px solid #00ff88;'>
                    <b style='color:#00ff88;'>{actor}</b><br>
                    <small style='color:#aaa;'>🔧 {len(techniques)} techniques</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No actors found")

    with col2:
        st.markdown("#### 🔧 Techniques")
        if results["techniques"]:
            for t in results["techniques"][:10]:
                st.markdown(f"""
                <div style='background:#1a1a2e; padding:12px; border-radius:8px; margin:5px 0; border-left:3px solid #ff6b6b;'>
                    <b style='color:#ff6b6b;'>{t['id']}</b> — {t['name']}<br>
                    <small style='color:#aaa;'>Used by {t['actor_count']} actor(s)</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No techniques found")

    with col3:
        st.markdown("#### 🎯 Targets")
        if results["targets"]:
            for t in results["targets"][:10]:
                st.markdown(f"""
                <div style='background:#1a1a2e; padding:12px; border-radius:8px; margin:5px 0; border-left:3px solid #ffd93d;'>
                    🎯 <b style='color:#ffd93d;'>{t['name']}</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No targets found")