# Severity scoring engine
# Scores a report 1-10 based on techniques found

# High severity techniques (score heavily)
HIGH_SEVERITY_TECHNIQUES = {
    "T1486",   # Data Encrypted for Impact (Ransomware)
    "T1490",   # Inhibit System Recovery
    "T1059.001", # PowerShell
    "T1003",   # OS Credential Dumping
    "T1055",   # Process Injection
    "T1078",   # Valid Accounts
    "T1110",   # Brute Force
    "T1195",   # Supply Chain Compromise
    "T1566",   # Phishing
    "T1566.001", # Spearphishing
    "T1021.001", # RDP
    "T1047",   # WMI
    "T1053",   # Scheduled Task
}

# Medium severity techniques
MEDIUM_SEVERITY_TECHNIQUES = {
    "T1071",   # Application Layer Protocol (C2)
    "T1027",   # Obfuscation
    "T1543",   # Create/Modify System Process
    "T1547",   # Boot/Logon Autostart
    "T1068",   # Privilege Escalation
    "T1021",   # Remote Services
    "T1203",   # Exploitation for Client Execution
    "T1218",   # Living off the Land
}

# High risk target sectors
HIGH_RISK_TARGETS = {
    "government", "defense", "military", "critical infrastructure",
    "healthcare", "finance", "banking", "energy", "nuclear"
}

# Known dangerous APT groups
HIGH_RISK_ACTORS = {
    "APT28", "APT29", "APT32", "APT33", "APT34", "APT38", "APT41",
    "Lazarus Group", "Sandworm", "Equation Group",
    "DarkSide", "REvil", "LockBit", "Conti", "BlackCat"
}


def calculate_severity(entities: dict, mapped_ttps: list) -> dict:
    """
    Calculate a severity score 1-10 for a threat intel report.
    Returns score + breakdown explanation.
    """
    score = 0
    breakdown = []

    # Score based on techniques (max 5 points)
    high_count = sum(
        1 for t in mapped_ttps
        if t.get("technique_id") in HIGH_SEVERITY_TECHNIQUES
    )
    medium_count = sum(
        1 for t in mapped_ttps
        if t.get("technique_id") in MEDIUM_SEVERITY_TECHNIQUES
    )

    technique_score = min(high_count * 1.0 + medium_count * 0.5, 5)
    score += technique_score

    if high_count > 0:
        breakdown.append(f"🔴 {high_count} high-severity technique(s) detected")
    if medium_count > 0:
        breakdown.append(f"🟠 {medium_count} medium-severity technique(s) detected")

    # Score based on threat actors (max 2 points)
    actors = entities.get("threat_actors", [])
    known_dangerous = [a for a in actors if a in HIGH_RISK_ACTORS]
    actor_score = min(len(known_dangerous) * 1.0, 2)
    score += actor_score

    if known_dangerous:
        breakdown.append(f"🔴 Known dangerous actor(s): {', '.join(known_dangerous)}")
    elif actors:
        breakdown.append(f"🟡 {len(actors)} threat actor(s) identified")
        score += 0.5

    # Score based on targets (max 2 points)
    targets = [t.lower() for t in entities.get("targets", [])]
    high_risk_targets_found = [
        t for t in targets
        if any(hr in t for hr in HIGH_RISK_TARGETS)
    ]
    target_score = min(len(high_risk_targets_found) * 0.5, 2)
    score += target_score

    if high_risk_targets_found:
        breakdown.append(f"🎯 High-risk sectors targeted: {', '.join(set(high_risk_targets_found[:3]))}")

    # Bonus point for ransomware
    technique_ids = [t.get("technique_id") for t in mapped_ttps]
    if "T1486" in technique_ids:
        score += 1
        breakdown.append("💀 Ransomware detected (+1 severity)")

    # Cap at 10
    final_score = min(round(score, 1), 10)

    # Determine severity level
    if final_score >= 8:
        level = "CRITICAL"
        color = "#ff0000"
        emoji = "🚨"
    elif final_score >= 6:
        level = "HIGH"
        color = "#ff6b00"
        emoji = "🔴"
    elif final_score >= 4:
        level = "MEDIUM"
        color = "#ffd93d"
        emoji = "🟡"
    elif final_score >= 2:
        level = "LOW"
        color = "#00ff88"
        emoji = "🟢"
    else:
        level = "MINIMAL"
        color = "#aaaaaa"
        emoji = "⚪"

    return {
        "score": final_score,
        "level": level,
        "color": color,
        "emoji": emoji,
        "breakdown": breakdown,
        "technique_count": len(mapped_ttps),
        "actor_count": len(actors),
        "target_count": len(targets)
    }