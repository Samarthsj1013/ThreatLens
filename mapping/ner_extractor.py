import spacy
import re
from config import NER_MODEL

nlp = spacy.load(NER_MODEL)

# Known threat actor names to help NER
KNOWN_THREAT_ACTORS = [
    "APT28", "APT29", "APT32", "APT33", "APT34", "APT38", "APT41",
    "Lazarus Group", "Cozy Bear", "Fancy Bear", "Sandworm", "Charming Kitten",
    "Carbanak", "FIN7", "FIN8", "Turla", "Equation Group", "DarkSide",
    "REvil", "LockBit", "BlackCat", "Conti", "Ryuk", "Maze", "BlackMatter"
]

# TTP keywords that map to MITRE techniques
TTP_KEYWORDS = {
    "spearphishing": "T1566.001",
    "phishing": "T1566",
    "powershell": "T1059.001",
    "mimikatz": "T1003",
    "credential dumping": "T1003",
    "lateral movement": "T1021",
    "ransomware": "T1486",
    "data exfiltration": "T1041",
    "command and control": "T1071",
    "c2": "T1071",
    "persistence": "T1053",
    "scheduled task": "T1053.005",
    "registry": "T1547.001",
    "dropper": "T1105",
    "backdoor": "T1543",
    "keylogger": "T1056.001",
    "privilege escalation": "T1068",
    "defense evasion": "T1562",
    "obfuscation": "T1027",
    "living off the land": "T1218",
    "lolbas": "T1218",
    "zero day": "T1203",
    "exploit": "T1203",
    "brute force": "T1110",
    "password spray": "T1110.003",
    "vpn": "T1133",
    "remote desktop": "T1021.001",
    "rdp": "T1021.001",
    "supply chain": "T1195",
    "watering hole": "T1189",
}

# Target sectors
TARGET_SECTORS = [
    "healthcare", "finance", "banking", "energy", "government",
    "defense", "education", "retail", "manufacturing", "telecom",
    "technology", "critical infrastructure", "military", "aerospace"
]


def extract_entities(text: str) -> dict:
    """
    Extract threat actors, TTPs, targets from raw text.
    Returns structured dict of entities.
    """
    doc = nlp(text[:100000])  # spacy limit safeguard
    text_lower = text.lower()

    threat_actors = extract_threat_actors(text, doc)
    ttps = extract_ttps(text_lower)
    targets = extract_targets(text_lower, doc)
    countries = extract_countries(doc)

    return {
        "threat_actors": list(set(threat_actors)),
        "ttps": ttps,
        "targets": list(set(targets)),
        "countries": list(set(countries))
    }


def extract_threat_actors(text: str, doc) -> list:
    actors = []

    # Match known threat actors by name
    for actor in KNOWN_THREAT_ACTORS:
        if actor.lower() in text.lower():
            actors.append(actor)

    # Also grab ORG entities from spaCy — but filter noisy ones
    for ent in doc.ents:
        if ent.label_ == "ORG" and len(ent.text) > 3:
            name = ent.text.strip()
            # Skip if too long (likely a sentence fragment)
            if len(name) > 40:
                continue
            # Skip if it contains common noise words
            noise_words = ["research", "malware", "threat", "center", "parallel", "report", "blog", "unit"]
            if any(w in name.lower() for w in noise_words):
                continue
            if any(kw in name.lower() for kw in ["apt", "group", "team", "bear", "panda", "tiger", "kitten"]):
                actors.append(name)

    return actors

    # Match known threat actors by name
    for actor in KNOWN_THREAT_ACTORS:
        if actor.lower() in text.lower():
            actors.append(actor)

    # Also grab ORG entities from spaCy that look like APT groups
    for ent in doc.ents:
        if ent.label_ == "ORG" and len(ent.text) > 3:
            if any(kw in ent.text.lower() for kw in ["apt", "group", "team", "bear", "panda", "tiger", "kitten"]):
                actors.append(ent.text)

    return actors


def extract_ttps(text_lower: str) -> list:
    found = []
    for keyword, technique_id in TTP_KEYWORDS.items():
        if keyword in text_lower:
            found.append({
                "keyword": keyword,
                "technique_id": technique_id
            })
    return found


def extract_targets(text_lower: str, doc) -> list:
    targets = []

    # Match known sectors
    for sector in TARGET_SECTORS:
        if sector in text_lower:
            targets.append(sector)

    # Also grab GPE (geopolitical) and ORG entities
    for ent in doc.ents:
        if ent.label_ in ["GPE", "ORG"] and len(ent.text) > 2:
            targets.append(ent.text)

    return targets[:20]  # Cap to avoid noise


def extract_countries(doc) -> list:
    return [ent.text for ent in doc.ents if ent.label_ == "GPE"]


if __name__ == "__main__":
    sample = """
    APT28, also known as Fancy Bear, has been using spearphishing emails
    to target government and defense organizations in Ukraine and Germany.
    The group uses PowerShell scripts for lateral movement and credential
    dumping via Mimikatz. Their C2 infrastructure relies on compromised VPN endpoints.
    """
    result = extract_entities(sample)
    print("🎯 Threat Actors:", result["threat_actors"])
    print("🔧 TTPs:", result["ttps"])
    print("🎯 Targets:", result["targets"])
    print("🌍 Countries:", result["countries"])