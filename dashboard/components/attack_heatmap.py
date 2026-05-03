import streamlit as st
import plotly.graph_objects as go

TACTICS = [
    "reconnaissance", "resource-development", "initial-access",
    "execution", "persistence", "privilege-escalation",
    "defense-evasion", "credential-access", "discovery",
    "lateral-movement", "collection", "command-and-control",
    "exfiltration", "impact"
]

TACTIC_LABELS = {
    "reconnaissance": "Recon",
    "resource-development": "Resource Dev",
    "initial-access": "Initial Access",
    "execution": "Execution",
    "persistence": "Persistence",
    "privilege-escalation": "Priv Esc",
    "defense-evasion": "Defense Evasion",
    "credential-access": "Cred Access",
    "discovery": "Discovery",
    "lateral-movement": "Lateral Movement",
    "collection": "Collection",
    "command-and-control": "C2",
    "exfiltration": "Exfiltration",
    "impact": "Impact"
}


def render_attack_heatmap(q):
    st.subheader("🗺️ MITRE ATT&CK Heatmap")
    st.markdown("Visual coverage of tactics detected across all ingested reports.")

    # Use the new dedicated tactic query
    tactic_counts = q.get_tactic_counts()

    if not tactic_counts:
        st.info("No techniques yet — ingest a report first")
        return

    labels = [TACTIC_LABELS.get(t, t) for t in TACTICS]
    values = [tactic_counts.get(t, 0) for t in TACTICS]
    colors = [
        "#ff4444" if v > 5
        else "#ff9900" if v > 2
        else "#ffd93d" if v > 0
        else "#1a1a2e"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=values,
        textposition="auto",
    ))

    fig.update_layout(
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font_color="#ffffff",
        height=420,
        xaxis=dict(tickangle=-30, gridcolor="#222"),
        yaxis=dict(gridcolor="#222", title="Technique Count"),
        title="ATT&CK Tactic Coverage",
        title_font_color="#00ff88"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Coverage summary
    covered = sum(1 for v in values if v > 0)
    high = sum(1 for v in values if v > 5)
    medium = sum(1 for v in values if 2 < v <= 5)

    st.markdown(f"""
    <div style='background:#1a1a2e; padding:15px; border-radius:10px; margin-top:10px; display:flex; gap:30px;'>
        <span>✅ <b style='color:#00ff88;'>Coverage:</b> {covered}/{len(TACTICS)} tactics</span>
        <span>🔴 <b style='color:#ff4444;'>High Activity:</b> {high} tactics</span>
        <span>🟠 <b style='color:#ff9900;'>Medium:</b> {medium} tactics</span>
    </div>
    """, unsafe_allow_html=True)