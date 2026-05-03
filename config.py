import os
from dotenv import load_dotenv

load_dotenv()

# Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "threatlens123")

# VirusTotal
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# MITRE ATT&CK
MITRE_TAXII_URL = "https://cti-taxii.mitre.org/taxii/"
MITRE_COLLECTION = "enterprise-attack"

# NER Model
NER_MODEL = "en_core_web_lg"

print("✅ Config loaded successfully")