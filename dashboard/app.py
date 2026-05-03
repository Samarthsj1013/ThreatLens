import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.queries import GraphQueries
from graph.exporter import export_to_json, export_techniques_to_csv
from dashboard.components.stats import render_stats
from dashboard.components.graph_view import render_graph
from dashboard.components.virustotal import render_virustotal
from dashboard.components.attack_heatmap import render_attack_heatmap
from ingestion.pdf_upload import render_pdf_upload
from demo_data import DemoQueries

st.set_page_config(
    page_title="ThreatLens",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align:center; color:#00ff88;'>🛡️ ThreatLens</h1>
    <p style='text-align:center; color:#aaa;'>Automated Cyber Threat Intelligence & MITRE ATT&CK Mapping Platform</p>
    <hr style='border-color:#333;'>
""", unsafe_allow_html=True)

# Try to connect to Neo4j — fall back to demo mode if unavailable
DEMO_MODE = False
try:
    q = GraphQueries()
    # Test the connection actually works
    q.get_all_actors()
except Exception:
    q = DemoQueries()
    DEMO_MODE = True

if DEMO_MODE:
    st.warning("⚠️ Running in Demo Mode — Neo4j not connected. Showing sample threat intelligence data.", icon="🔌")

# Sidebar
st.sidebar.title("⚙️ Controls")
st.sidebar.markdown("---")

if DEMO_MODE:
    st.sidebar.info("🔌 Demo Mode — ingestion disabled. Run locally with Neo4j for full functionality.")
else:
    ingest_mode = st.sidebar.radio("📥 Ingest Mode", ["🌐 URL", "📄 PDF Upload"])
    st.sidebar.markdown("---")

    if ingest_mode == "🌐 URL":
        st.sidebar.subheader("🌐 Ingest from URL")
        source_input = st.sidebar.text_input(
            "Blog or report URL",
            placeholder="https://..."
        )
        if st.sidebar.button("🚀 Run Pipeline", use_container_width=True):
            if source_input.strip():
                with st.spinner("Running ThreatLens pipeline..."):
                    try:
                        from pipeline import run_pipeline
                        result = run_pipeline(source_input.strip())
                        st.sidebar.success("✅ Pipeline complete!")
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"❌ Error: {e}")
            else:
                st.sidebar.warning("Please enter a URL")

    else:
        st.sidebar.subheader("📄 Upload PDF")
        pdf_result = render_pdf_upload()
        if pdf_result and st.sidebar.button("🚀 Run Pipeline on PDF", use_container_width=True):
            with st.spinner("Running pipeline on PDF..."):
                try:
                    from mapping.ner_extractor import extract_entities
                    from mapping.attack_mapper import load_mitre_data, build_technique_lookup, map_ttps_to_attack
                    from graph.graph_db import GraphDB

                    entities = extract_entities(pdf_result["full_text"])
                    mitre_data = load_mitre_data()
                    lookup = build_technique_lookup(mitre_data)
                    mapped_ttps = map_ttps_to_attack(entities["ttps"], lookup)

                    db = GraphDB()
                    db.store_intelligence(
                        source=pdf_result["source"],
                        source_type="pdf",
                        entities=entities,
                        mapped_ttps=mapped_ttps
                    )
                    st.sidebar.success("✅ PDF ingested!")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"❌ Error: {e}")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔗 Sample Reports")
    samples = {
        "APT28 / Sofacy": "https://unit42.paloaltonetworks.com/unit42-sofacy-groups-parallel-attacks/",
        "FIN7 Tactics": "https://attack.mitre.org/groups/G0046/",
        "Lazarus TTPs": "https://attack.mitre.org/groups/G0032/",
    }
    for label, url in samples.items():
        if st.sidebar.button(label, use_container_width=True):
            with st.spinner(f"Ingesting {label}..."):
                try:
                    from pipeline import run_pipeline
                    run_pipeline(url)
                    st.sidebar.success(f"✅ {label} ingested!")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"❌ {e}")

    st.sidebar.markdown("---")
    st.sidebar.subheader("📤 Export Data")
    if st.sidebar.button("⬇️ Export JSON", use_container_width=True):
        graph_data = q.get_full_graph_data()
        path = export_to_json(graph_data)
        st.sidebar.success(f"✅ Exported to data/")

    if st.sidebar.button("⬇️ Export CSV", use_container_width=True):
        techniques = q.get_top_techniques(50)
        path = export_techniques_to_csv(techniques)
        st.sidebar.success(f"✅ Exported to data/")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📊 Dashboard",
    "🕸️ Knowledge Graph",
    "🗺️ ATT&CK Heatmap",
    "🔬 VirusTotal",
    "🔍 Query",
    "🔎 Search",
    "⚔️ Compare",
    "📅 Timeline",
    "⚠️ Severity",
    "🎯 Attribution"
])

with tab1:
    render_stats(q)

with tab2:
    render_graph(q)

with tab3:
    render_attack_heatmap(q)

with tab4:
    render_virustotal()

with tab5:
    st.subheader("🔍 Query the Knowledge Graph")
    col1, col2 = st.columns(2)
    actors = q.get_all_actors()

    with col1:
        st.markdown("#### Techniques by Actor")
        if actors:
            selected_actor = st.selectbox("Select Threat Actor", actors)
            techniques = q.get_techniques_by_actor(selected_actor)
            if techniques:
                for t in techniques:
                    st.markdown(f"""
                    <div style='background:#1a1a2e; padding:10px; border-radius:8px; margin:5px 0; border-left:3px solid #00ff88;'>
                        <b style='color:#00ff88;'>{t['id']}</b> — {t['name']}<br>
                        <small style='color:#aaa;'>Tactics: {t['tactics']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No techniques found")
        else:
            st.info("No actors yet — ingest a report first")

    with col2:
        st.markdown("#### Targets by Actor")
        if actors:
            selected_actor2 = st.selectbox("Select Actor", actors, key="actor2")
            targets = q.get_targets_by_actor(selected_actor2)
            if targets:
                for t in targets:
                    st.markdown(f"""
                    <div style='background:#1a1a2e; padding:10px; border-radius:8px; margin:5px 0; border-left:3px solid #ff6b6b;'>
                        🎯 <b style='color:#ff6b6b;'>{t['target']}</b>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No targets found")

with tab6:
    from dashboard.components.search import render_search
    render_search(q)

with tab7:
    from dashboard.components.comparison import render_comparison
    render_comparison(q)

with tab8:
    from dashboard.components.timeline import render_timeline
    render_timeline(q)

with tab9:
    from dashboard.components.severity import render_severity
    render_severity()

with tab10:
    from dashboard.components.attribution import render_attribution
    render_attribution(q)