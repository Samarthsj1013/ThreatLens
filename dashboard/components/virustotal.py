import streamlit as st
from mapping.virustotal import lookup_hash, lookup_url


def render_virustotal():
    st.subheader("🔬 VirusTotal Lookup")

    tab_hash, tab_url = st.tabs(["🔑 File Hash", "🌐 URL"])

    with tab_hash:
        st.markdown("#### Lookup a file hash (MD5, SHA1, SHA256)")
        hash_input = st.text_input(
            "Enter file hash",
            placeholder="e.g. 44d88612fea8a8f36de82e1278abb02f"
        )
        if st.button("🔍 Scan Hash", use_container_width=True):
            if hash_input.strip():
                with st.spinner("Querying VirusTotal..."):
                    result = lookup_hash(hash_input.strip())
                    render_vt_result(result)
            else:
                st.warning("Please enter a hash")

    with tab_url:
        st.markdown("#### Lookup a URL")
        url_input = st.text_input(
            "Enter URL",
            placeholder="e.g. https://suspicious-site.com"
        )
        if st.button("🔍 Scan URL", use_container_width=True):
            if url_input.strip():
                with st.spinner("Querying VirusTotal..."):
                    result = lookup_url(url_input.strip())
                    render_vt_result(result)
            else:
                st.warning("Please enter a URL")


def render_vt_result(result: dict):
    if "error" in result:
        st.error(f"❌ {result['error']}")
        return

    malicious = result.get("malicious", 0)
    suspicious = result.get("suspicious", 0)
    harmless = result.get("harmless", 0)
    total = result.get("total", 0)

    # Verdict banner
    if malicious > 5:
        st.error(f"🚨 MALICIOUS — {malicious}/{total} engines flagged this")
    elif malicious > 0 or suspicious > 0:
        st.warning(f"⚠️ SUSPICIOUS — {malicious} malicious, {suspicious} suspicious out of {total}")
    else:
        st.success(f"✅ CLEAN — 0/{total} engines flagged this")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 Malicious", malicious)
    with col2:
        st.metric("🟡 Suspicious", suspicious)
    with col3:
        st.metric("🟢 Harmless", harmless)
    with col4:
        st.metric("📊 Total Engines", total)

    # Details
    if result.get("name"):
        st.markdown(f"**Name:** `{result['name']}`")
    if result.get("type"):
        st.markdown(f"**Type:** `{result['type']}`")
    if result.get("size"):
        st.markdown(f"**Size:** `{result['size']} bytes`")

    # Engine detections
    if result.get("detections"):
        st.markdown("#### 🔍 Engine Detections")
        for engine, detection in list(result["detections"].items())[:15]:
            st.markdown(f"""
            <div style='background:#1a1a2e; padding:8px 12px; border-radius:6px; margin:3px 0; border-left:3px solid #ff6b6b;'>
                <b style='color:#ff6b6b;'>{engine}</b> — {detection}
            </div>
            """, unsafe_allow_html=True)