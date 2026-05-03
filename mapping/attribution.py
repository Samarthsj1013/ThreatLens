# APT Attribution Engine
# Given a set of TTPs, guess which known threat actor matches best

# Known actor TTP profiles based on MITRE ATT&CK
ACTOR_PROFILES = {
    "APT28 (Fancy Bear)": {
        "techniques": ["T1566.001", "T1059.001", "T1071", "T1027", "T1078", "T1021.001"],
        "targets": ["government", "defense", "military", "election"],
        "origin": "Russia",
        "motivation": "Espionage"
    },
    "APT29 (Cozy Bear)": {
        "techniques": ["T1566", "T1059.001", "T1078", "T1027", "T1547", "T1195"],
        "targets": ["government", "think tank", "healthcare"],
        "origin": "Russia",
        "motivation": "Espionage"
    },
    "Lazarus Group": {
        "techniques": ["T1566.001", "T1059.001", "T1486", "T1041", "T1027", "T1195"],
        "targets": ["finance", "banking", "cryptocurrency", "defense"],
        "origin": "North Korea",
        "motivation": "Financial + Espionage"
    },
    "FIN7": {
        "techniques": ["T1566.001", "T1059.001", "T1003", "T1021", "T1547", "T1071"],
        "targets": ["retail", "restaurant", "hospitality", "finance"],
        "origin": "Eastern Europe",
        "motivation": "Financial"
    },
    "Carbanak": {
        "techniques": ["T1566.001", "T1003", "T1021.001", "T1027", "T1059.001", "T1071"],
        "targets": ["banking", "finance", "retail"],
        "origin": "Eastern Europe",
        "motivation": "Financial"
    },
    "REvil": {
        "techniques": ["T1486", "T1490", "T1566", "T1027", "T1195", "T1059.001"],
        "targets": ["healthcare", "finance", "manufacturing", "government"],
        "origin": "Russia",
        "motivation": "Ransomware"
    },
    "Conti": {
        "techniques": ["T1486", "T1490", "T1566.001", "T1059.001", "T1003", "T1021"],
        "targets": ["healthcare", "government", "finance", "critical infrastructure"],
        "origin": "Russia",
        "motivation": "Ransomware"
    },
    "APT41": {
        "techniques": ["T1195", "T1059.001", "T1078", "T1027", "T1547", "T1068"],
        "targets": ["healthcare", "technology", "telecom", "gaming"],
        "origin": "China",
        "motivation": "Espionage + Financial"
    },
    "Sandworm": {
        "techniques": ["T1059.001", "T1486", "T1490", "T1195", "T1027", "T1071"],
        "targets": ["energy", "government", "critical infrastructure"],
        "origin": "Russia",
        "motivation": "Disruption"
    },
    "APT33 (Elfin)": {
        "techniques": ["T1566.001", "T1059.001", "T1071", "T1027", "T1547"],
        "targets": ["energy", "aerospace", "defense"],
        "origin": "Iran",
        "motivation": "Espionage"
    }
}


def attribute_ttps(technique_ids: list, targets: list = None) -> list:
    """
    Given a list of technique IDs, score each known actor profile
    and return ranked matches.
    """
    if not technique_ids:
        return []

    targets_lower = [t.lower() for t in (targets or [])]
    results = []

    for actor_name, profile in ACTOR_PROFILES.items():
        profile_techniques = set(profile["techniques"])
        input_techniques = set(technique_ids)

        # Technique overlap
        matched = profile_techniques & input_techniques
        technique_score = len(matched) / max(len(profile_techniques), 1) * 100

        # Target overlap bonus
        target_bonus = 0
        matched_targets = []
        for target in targets_lower:
            for profile_target in profile["targets"]:
                if profile_target in target:
                    target_bonus += 10
                    matched_targets.append(profile_target)
                    break

        total_score = min(technique_score + target_bonus, 100)

        if total_score > 0:
            results.append({
                "actor": actor_name,
                "score": round(total_score, 1),
                "matched_techniques": list(matched),
                "matched_targets": list(set(matched_targets)),
                "origin": profile["origin"],
                "motivation": profile["motivation"],
                "confidence": get_confidence(total_score)
            })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]  # Top 5 matches


def get_confidence(score: float) -> str:
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    elif score >= 20:
        return "LOW"
    else:
        return "MINIMAL"