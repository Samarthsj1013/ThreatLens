import streamlit as st
import plotly.graph_objects as go
from mapping.severity import calculate_severity
from mapping.attribution import attribute_ttps
from ingestion.ingestor import ingest
from mapping.ner_extractor import extract_entities
from mapping.attack_mapper import load_mitre_data, build_technique_lookup, map_ttps_to_attack


def render_severity():
    st.subheader("⚠️ Report Severity Scorer")
    st.markdown("Analyze any threat report and get an instant risk score + APT attribution.")

    source = st.text_input(
        "Enter URL or PDF path to analyze",
        placeholder="https://... or paste a threat description below"
    )

    # Also allow direct text input
    st.markdown("**Or paste threat description directly:**")
    manual_text = st.text_area(
        "Paste threat intel text",
        placeholder="APT28 used spearphishing emails and PowerShell to target government organizations...",
        height=150,
        label_visibility="collapsed"
    )

    analyze_btn = st.button("🔍 Analyze & Score", use_container_width=True)

    if not analyze_btn:
        return

    if not source and not manual_text:
        st.warning("Please enter a URL or paste some text")
        return

    with st.spinner("Analyzing..."):
        try:
            # Get text
            if manual_text.strip():
                text = manual_text.strip()
                src_name = "Manual Input"
            else:
                ingested = ingest(source.strip())
                text = ingested["full_text"]
                src_name = ingested["source"]

            # Extract + map
            entities = extract_entities(text)
            mitre_data = load_mitre_data()
            lookup = build_technique_lookup(mitre_data)
            mapped_ttps = map_ttps_to_attack(entities["ttps"], lookup)

            # Score
            severity = calculate_severity(entities, mapped_ttps)

            # Attribution
            technique_ids = [t["technique_id"] for t in mapped_ttps]
            attributions = attribute_ttps(technique_ids, entities.get("targets", []))

        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
            return

    # Severity display
    st.markdown("---")
    st.markdown(f"### {severity['emoji']} Severity Score for: `{src_name[:60]}`")

    # Big score display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style='background:#1a1a2e; padding:20px; border-radius:12px; text-align:center;
                    border:2px solid {severity["color"]};'>
            <div style='font-size:48px; font-weight:bold; color:{severity["color"]};'>
                {severity["score"]}
            </div>
            <div style='color:#aaa; font-size:14px;'>/ 10</div>
            <div style='color:{severity["color"]}; font-size:18px; font-weight:bold; margin-top:5px;'>
                {severity["level"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.metric("🔧 Techniques", severity["technique_count"])
    with col3:
        st.metric("🕵️ Actors", severity["actor_count"])
    with col4:
        st.metric("🎯 Targets", severity["target_count"])

    # Severity gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=severity["score"],
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {"range": [0, 10]},
            "bar": {"color": severity["color"]},
            "steps": [
                {"range": [0, 2], "color": "#1a1a2e"},
                {"range": [2, 4], "color": "#1a2e1a"},
                {"range": [4, 6], "color": "#2e2a1a"},
                {"range": [6, 8], "color": "#2e1a1a"},
                {"range": [8, 10], "color": "#3e0000"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 4},
                "thickness": 0.75,
                "value": severity["score"]
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="#0e1117",
        font_color="#ffffff",
        height=250,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Breakdown
    st.markdown("#### 📋 Score Breakdown")
    for item in severity["breakdown"]:
        st.markdown(f"""
        <div style='background:#1a1a2e; padding:10px; border-radius:8px; margin:4px 0;'>
            {item}
        </div>
        """, unsafe_allow_html=True)

    # Attribution
    if attributions:
        st.markdown("---")
        st.markdown("#### 🎯 APT Attribution — Most Likely Threat Actors")
        st.markdown("Based on technique overlap with known actor profiles:")

        for i, attr in enumerate(attributions):
            confidence_color = {
                "HIGH": "#ff4444",
                "MEDIUM": "#ff9900",
                "LOW": "#ffd93d",
                "MINIMAL": "#aaaaaa"
            }.get(attr["confidence"], "#aaaaaa")

            st.markdown(f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:10px; margin:8px 0;
                        border-left:4px solid {confidence_color};'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <b style='color:{confidence_color}; font-size:16px;'>
                        #{i+1} {attr["actor"]}
                    </b>
                    <span style='color:{confidence_color}; font-weight:bold;'>
                        {attr["score"]}% match — {attr["confidence"]} confidence
                    </span>
                </div>
                <div style='color:#aaa; font-size:13px; margin-top:5px;'>
                    🌍 Origin: {attr["origin"]} &nbsp;|&nbsp;
                    💡 Motivation: {attr["motivation"]}
                </div>
                <div style='color:#888; font-size:12px; margin-top:4px;'>
                    Matched techniques: {", ".join(attr["matched_techniques"][:5])}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No strong attribution matches found — try ingesting more detailed reports")