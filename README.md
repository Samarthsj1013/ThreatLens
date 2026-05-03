# 🛡️ ThreatLens

> **Automated Cyber Threat Intelligence & MITRE ATT&CK Mapping Platform**

ThreatLens is an end-to-end threat intelligence platform that ingests cybersecurity reports (PDFs and blog posts), extracts threat actors and attack techniques using NLP, maps them to the MITRE ATT&CK framework, and visualizes adversary behavior as an interactive knowledge graph.

---

## 🎯 What It Does
Threat Report (PDF/URL)
↓
NLP Entity Extraction (spaCy + BERT)
↓
MITRE ATT&CK Mapping (TAXII API)
↓
Neo4j Knowledge Graph
↓
Interactive Dashboard (Streamlit)

---

## ✨ Features

- **📥 Multi-Source Ingestion** — Ingest threat intel from PDF reports or blog URLs
- **🧠 NLP Entity Extraction** — Extract threat actors, TTPs, and targets using spaCy NER
- **🗺️ MITRE ATT&CK Mapping** — Auto-map techniques to official ATT&CK IDs via TAXII API
- **🔍 Semantic Search** — Find techniques using sentence-transformers similarity matching
- **🕸️ Knowledge Graph** — Interactive Neo4j graph linking actors → techniques → targets
- **📊 ATT&CK Heatmap** — Visual coverage of 14 MITRE tactics across all reports
- **🔬 VirusTotal Integration** — Hash and URL lookup against 70+ AV engines
- **⚔️ Actor Comparison** — Side-by-side analysis of two threat actors
- **🔎 Search** — Search actors, techniques, and targets across the graph
- **📅 Report Timeline** — Track all ingested intelligence sources
- **📤 Export** — Download graph data as JSON or CSV

---

## 🏗️ Architecture
ThreatLens/
├── ingestion/          # PDF + URL ingestion pipeline
│   ├── pdf_ingestor.py
│   ├── blog_ingestor.py
│   ├── pdf_upload.py
│   └── ingestor.py
├── mapping/            # NER + MITRE ATT&CK mapping
│   ├── ner_extractor.py
│   ├── attack_mapper.py
│   ├── similarity.py
│   └── virustotal.py
├── graph/              # Neo4j graph database
│   ├── graph_db.py
│   ├── queries.py
│   ├── schema.py
│   └── exporter.py
├── dashboard/          # Streamlit UI
│   ├── app.py
│   └── components/
│       ├── stats.py
│       ├── graph_view.py
│       ├── attack_heatmap.py
│       ├── virustotal.py
│       ├── search.py
│       ├── comparison.py
│       └── timeline.py
├── pipeline.py         # Master pipeline
├── config.py
└── .env

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Neo4j Desktop (free)

### Installation

```bash
git clone https://github.com/yourusername/ThreatLens
cd ThreatLens
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### Configuration

Create a `.env` file:
```env
VIRUSTOTAL_API_KEY=your_key_here
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### Run

```bash
# Setup Neo4j schema
python -c "from graph.schema import create_constraints; create_constraints()"

# Launch dashboard
streamlit run dashboard/app.py --server.fileWatcherType none
```

Open `http://localhost:8501`

---

## 🧪 Testing the Pipeline

```bash
# Test ingestion
python -c "from ingestion.ingestor import ingest; print(ingest('https://attack.mitre.org/groups/G0046/'))"

# Test NER
python -c "from mapping.ner_extractor import extract_entities; print(extract_entities('APT28 used spearphishing and PowerShell to target government organizations.'))"

# Test graph connection
python -c "from graph.graph_db import GraphDB; GraphDB()"
```

---

## 📊 Tech Stack

| Layer | Technology |
|---|---|
| NLP / NER | spaCy (`en_core_web_lg`) + HuggingFace |
| Semantic Search | sentence-transformers (`all-MiniLM-L6-v2`) |
| ATT&CK Mapping | MITRE TAXII API + `mitreattack-python` |
| Knowledge Graph | Neo4j + py2neo |
| PDF Parsing | PyMuPDF (fitz) |
| Web Scraping | BeautifulSoup4 + requests |
| Backend | FastAPI |
| Dashboard | Streamlit |
| Visualization | Plotly + NetworkX |
| Threat Intel | VirusTotal API v3 |

---

## 🔗 Related Projects

This project is part of a cybersecurity portfolio trilogy:

| Project | Description |
|---|---|
| [PhishGuard AI](https://github.com/yourusername/PhishGuard) | Chrome extension — phishing URL detection |
| [PE Malware Classifier](https://github.com/yourusername/PE-Classifier) | Static malware analysis on Windows PE files |
| **ThreatLens** | Threat intelligence & ATT&CK mapping platform |

Together they form a complete detection → analysis → attribution pipeline.

---

## 📚 Data Sources

- [MITRE ATT&CK](https://attack.mitre.org/) — Adversary tactics and techniques
- [VirusTotal](https://www.virustotal.com/) — Multi-engine malware scanning
- [Mandiant](https://www.mandiant.com/resources) — Threat intelligence reports
- [Unit 42 (Palo Alto)](https://unit42.paloaltonetworks.com/) — Research blog
- [CISA](https://www.cisa.gov/resources-tools/resources) — US government advisories
- [CERT-In](https://www.cert-in.org.in/) — Indian government cyber reports

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [your-linkedin](https://linkedin.com/in/yourlinkedin)

---

