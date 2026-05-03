import streamlit as st
from mapping.attribution import attribute_ttps


def render_attribution(q):
    st.subheader("🎯 APT Attribution Engine")
    st.markdown("Select techniques you observed and find which threat actor matches best.")

    # Common techniques for quick selection
    COMMON_TECHNIQUES = {
        "T1566 — Phishing": "T1566",
        "T1566.001 — Spearphishing": "T1566.001",
        "T1059.001 — PowerShell": "T1059.001",
        "T1003 — Credential Dumping": "T1003",
        "T1486 — Ransomware (Data Encrypted)": "T1486",
        "T1071 — C2 (App Layer Protocol)": "T1071",
        "T1027 — Obfuscation": "T1027",
        "T1195 — Supply Chain": "T1195",
        "T1021.001 — RDP": "T1021.001",
        "T1078 — Valid Accounts": "T1078",
        "T1547 — Boot Autostart": "T1547",
        "T1068 — Privilege Escalation": "T1068",
        "T1490 — Inhibit Recovery": "T1490",
        "T1041 — Exfiltration over C2": "T1041",
    }

    st.markdown("#### Select observed techniques:")
    selected_labels = st.multiselect(
        "Choose techniques",
        options=list(COMMON_TECHNIQUES.keys()),
        default=["T1566.001 — Spearphishing", "T1059.001 — PowerShell", "T1027 — Obfuscation"]
    )

    # Also allow manual technique ID input
    manual_ids = st.text_input(
        "Or add technique IDs manually (comma separated)",
        placeholder="T1055, T1021, T1110.003"
    )

    # Target sector
    target_sector = st.text_input(
        "Target sector (optional — improves accuracy)",
        placeholder="government, healthcare, finance..."
    )

    if st.button("🔍 Run Attribution", use_container_width=True):
        # Build technique list
        technique_ids = [COMMON_TECHNIQUES[l] for l in selected_labels]

        if manual_ids:
            extra = [t.strip() for t in manual_ids.split(",") if t.strip()]
            technique_ids.extend(extra)

        targets = [target_sector] if target_sector else []

        if not technique_ids:
            st.warning("Please select at least one technique")
            return

        with st.spinner("Running attribution analysis..."):
            results = attribute_ttps(technique_ids, targets)

        if not results:
            st.info("No matches found. Try adding more techniques.")
            return

        st.markdown(f"---")
        st.markdown(f"#### Results for {len(technique_ids)} technique(s):")

        for i, attr in enumerate(results):
            confidence_color = {
                "HIGH": "#ff4444",
                "MEDIUM": "#ff9900",
                "LOW": "#ffd93d",
                "MINIMAL": "#888888"
            }.get(attr["confidence"], "#888888")

            with st.expander(
                f"#{i+1} {attr['actor']} — {attr['score']}% match ({attr['confidence']} confidence)",
                expanded=(i == 0)
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🌍 Origin:** {attr['origin']}")
                    st.markdown(f"**💡 Motivation:** {attr['motivation']}")
                    st.markdown(f"**📊 Match Score:** {attr['score']}%")
                with col2:
                    st.markdown(f"**✅ Matched Techniques:**")
                    for t in attr["matched_techniques"]:
                        st.markdown(f"- `{t}`")
                if attr["matched_targets"]:
                    st.markdown(f"**🎯 Matched Targets:** {', '.join(attr['matched_targets'])}")