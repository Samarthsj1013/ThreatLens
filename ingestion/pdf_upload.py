import streamlit as st
import tempfile
import os
from ingestion.pdf_ingestor import extract_text_from_pdf


def render_pdf_upload():
    """
    Streamlit component for uploading and ingesting PDF reports.
    Returns extracted text dict or None.
    """
    st.markdown("#### 📎 Upload PDF Threat Report")

    uploaded_file = st.file_uploader(
        "Drop a PDF threat intel report here",
        type=["pdf"],
        help="Supports any PDF — Mandiant, CrowdStrike, Unit42, etc."
    )

    if uploaded_file is not None:
        st.success(f"✅ Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

        # Save to temp file so pdf_ingestor can read it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            with st.spinner("Extracting text from PDF..."):
                result = extract_text_from_pdf(tmp_path)
                result["source"] = uploaded_file.name
                st.info(f"📄 Extracted {len(result['full_text'])} characters from {result['total_pages']} pages")
                return result
        except Exception as e:
            st.error(f"❌ Failed to read PDF: {e}")
            return None
        finally:
            os.unlink(tmp_path)

    return None