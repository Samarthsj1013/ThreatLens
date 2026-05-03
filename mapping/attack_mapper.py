import json
import os
import requests
from config import DATA_DIR

MITRE_LOCAL_PATH = os.path.join(DATA_DIR, "mitre_attack.json")
MITRE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"


def download_mitre_data():
    """Download MITRE ATT&CK enterprise data locally."""
    print("⬇️  Downloading MITRE ATT&CK data...")
    os.makedirs(DATA_DIR, exist_ok=True)
    response = requests.get(MITRE_URL, timeout=60)
    response.raise_for_status()
    with open(MITRE_LOCAL_PATH, "w", encoding="utf-8") as f:
        json.dump(response.json(), f)
    print(f"✅ MITRE data saved to {MITRE_LOCAL_PATH}")


def load_mitre_data() -> dict:
    """Load MITRE ATT&CK data from local file, download if missing."""
    if not os.path.exists(MITRE_LOCAL_PATH):
        download_mitre_data()
    with open(MITRE_LOCAL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_technique_lookup(mitre_data: dict) -> dict:
    """
    Build a lookup dict: technique_id -> technique details
    """
    lookup = {}
    for obj in mitre_data.get("objects", []):
        if obj.get("type") == "attack-pattern":
            ext_refs = obj.get("external_references", [])
            for ref in ext_refs:
                if ref.get("source_name") == "mitre-attack":
                    technique_id = ref.get("external_id", "")
                    lookup[technique_id] = {
                        "id": technique_id,
                        "name": obj.get("name", ""),
                        "description": obj.get("description", "")[:300],
                        "tactics": [
                            phase["phase_name"]
                            for phase in obj.get("kill_chain_phases", [])
                        ],
                        "platforms": obj.get("x_mitre_platforms", []),
                        "url": ref.get("url", "")
                    }
    return lookup


def map_ttps_to_attack(ttps: list, technique_lookup: dict) -> list:
    """
    Maps extracted TTPs to full MITRE ATT&CK technique details.
    """
    mapped = []
    for ttp in ttps:
        technique_id = ttp.get("technique_id")
        base_id = technique_id.split(".")[0] if "." in technique_id else technique_id

        # Try exact match first, then base technique
        detail = technique_lookup.get(technique_id) or technique_lookup.get(base_id)

        if detail:
            mapped.append({
                "keyword": ttp["keyword"],
                "technique_id": technique_id,
                "name": detail["name"],
                "tactics": detail["tactics"],
                "platforms": detail["platforms"],
                "url": detail["url"],
                "description": detail["description"]
            })
        else:
            mapped.append({
                "keyword": ttp["keyword"],
                "technique_id": technique_id,
                "name": "Unknown",
                "tactics": [],
                "platforms": [],
                "url": "",
                "description": ""
            })
    return mapped


if __name__ == "__main__":
    print("Loading MITRE ATT&CK data...")
    data = load_mitre_data()
    lookup = build_technique_lookup(data)
    print(f"✅ Loaded {len(lookup)} techniques")

    # Test mapping
    test_ttps = [
        {"keyword": "spearphishing", "technique_id": "T1566.001"},
        {"keyword": "powershell", "technique_id": "T1059.001"},
    ]
    results = map_ttps_to_attack(test_ttps, lookup)
    for r in results:
        print(f"\n🔧 {r['technique_id']} — {r['name']}")
        print(f"   Tactics: {r['tactics']}")