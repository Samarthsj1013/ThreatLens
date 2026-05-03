# Pre-loaded demo data for when Neo4j is not connected
# This is shown on Streamlit Cloud deployment

DEMO_ACTORS = [
    "APT28", "APT29", "Lazarus Group", "FIN7",
    "Carbanak", "REvil", "Conti", "DarkSide",
    "Sandworm", "APT41"
]

DEMO_TECHNIQUES = [
    {"id": "T1566.001", "name": "Spearphishing Attachment", "actor_count": 8, "tactics": "initial-access"},
    {"id": "T1059.001", "name": "PowerShell", "actor_count": 9, "tactics": "execution"},
    {"id": "T1003", "name": "OS Credential Dumping", "actor_count": 7, "tactics": "credential-access"},
    {"id": "T1486", "name": "Data Encrypted for Impact", "actor_count": 4, "tactics": "impact"},
    {"id": "T1071", "name": "Application Layer Protocol", "actor_count": 8, "tactics": "command-and-control"},
    {"id": "T1027", "name": "Obfuscated Files or Information", "actor_count": 9, "tactics": "defense-evasion"},
    {"id": "T1195", "name": "Supply Chain Compromise", "actor_count": 5, "tactics": "initial-access"},
    {"id": "T1021.001", "name": "Remote Desktop Protocol", "actor_count": 6, "tactics": "lateral-movement"},
    {"id": "T1547", "name": "Boot or Logon Autostart", "actor_count": 7, "tactics": "persistence"},
    {"id": "T1068", "name": "Exploitation for Privilege Escalation", "actor_count": 6, "tactics": "privilege-escalation"},
]

DEMO_GRAPH_NODES = [
    {"label": "ThreatActor", "name": "APT28", "id": 1},
    {"label": "ThreatActor", "name": "APT29", "id": 2},
    {"label": "ThreatActor", "name": "Lazarus Group", "id": 3},
    {"label": "ThreatActor", "name": "FIN7", "id": 4},
    {"label": "ThreatActor", "name": "Carbanak", "id": 5},
    {"label": "ThreatActor", "name": "REvil", "id": 6},
    {"label": "ThreatActor", "name": "Conti", "id": 7},
    {"label": "ThreatActor", "name": "DarkSide", "id": 8},
    {"label": "Technique", "name": "T1566.001", "id": 9},
    {"label": "Technique", "name": "T1059.001", "id": 10},
    {"label": "Technique", "name": "T1486", "id": 11},
    {"label": "Technique", "name": "T1003", "id": 12},
    {"label": "Technique", "name": "T1071", "id": 13},
    {"label": "Target", "name": "government", "id": 14},
    {"label": "Target", "name": "finance", "id": 15},
    {"label": "Target", "name": "healthcare", "id": 16},
    {"label": "Target", "name": "defense", "id": 17},
    {"label": "Report", "name": "Mandiant APT1 Report", "id": 18},
    {"label": "Report", "name": "Unit42 Sofacy Analysis", "id": 19},
]

DEMO_GRAPH_EDGES = [
    {"source": 1, "target": 9, "relationship": "USES"},
    {"source": 1, "target": 10, "relationship": "USES"},
    {"source": 1, "target": 14, "relationship": "TARGETS"},
    {"source": 2, "target": 9, "relationship": "USES"},
    {"source": 2, "target": 13, "relationship": "USES"},
    {"source": 2, "target": 14, "relationship": "TARGETS"},
    {"source": 3, "target": 11, "relationship": "USES"},
    {"source": 3, "target": 10, "relationship": "USES"},
    {"source": 3, "target": 15, "relationship": "TARGETS"},
    {"source": 4, "target": 9, "relationship": "USES"},
    {"source": 4, "target": 12, "relationship": "USES"},
    {"source": 4, "target": 15, "relationship": "TARGETS"},
    {"source": 5, "target": 12, "relationship": "USES"},
    {"source": 5, "target": 10, "relationship": "USES"},
    {"source": 5, "target": 15, "relationship": "TARGETS"},
    {"source": 6, "target": 11, "relationship": "USES"},
    {"source": 6, "target": 9, "relationship": "USES"},
    {"source": 6, "target": 16, "relationship": "TARGETS"},
    {"source": 7, "target": 11, "relationship": "USES"},
    {"source": 7, "target": 10, "relationship": "USES"},
    {"source": 7, "target": 16, "relationship": "TARGETS"},
    {"source": 8, "target": 11, "relationship": "USES"},
    {"source": 8, "target": 13, "relationship": "USES"},
    {"source": 8, "target": 17, "relationship": "TARGETS"},
    {"source": 18, "target": 1, "relationship": "MENTIONS"},
    {"source": 19, "target": 4, "relationship": "MENTIONS"},
]

DEMO_TACTIC_COUNTS = {
    "initial-access": 3,
    "execution": 4,
    "persistence": 2,
    "privilege-escalation": 3,
    "defense-evasion": 4,
    "credential-access": 2,
    "lateral-movement": 2,
    "command-and-control": 3,
    "impact": 2,
    "exfiltration": 1
}


class DemoQueries:
    """Fallback queries using demo data when Neo4j is unavailable."""

    def get_all_actors(self):
        return DEMO_ACTORS

    def get_top_techniques(self, limit=10):
        return DEMO_TECHNIQUES[:limit]

    def get_full_graph_data(self):
        return {"nodes": DEMO_GRAPH_NODES, "edges": DEMO_GRAPH_EDGES}

    def get_tactic_counts(self):
        return DEMO_TACTIC_COUNTS

    def get_techniques_by_actor(self, actor_name):
        return [
            {"id": "T1566.001", "name": "Spearphishing Attachment", "tactics": "initial-access"},
            {"id": "T1059.001", "name": "PowerShell", "tactics": "execution"},
            {"id": "T1027", "name": "Obfuscated Files or Information", "tactics": "defense-evasion"},
            {"id": "T1071", "name": "Application Layer Protocol", "tactics": "command-and-control"},
        ]

    def get_targets_by_actor(self, actor_name):
        return [
            {"target": "government", "type": "sector"},
            {"target": "defense", "type": "sector"},
            {"target": "finance", "type": "sector"},
        ]

    def get_shared_techniques(self, actor1, actor2):
        return [
            {"id": "T1566.001", "name": "Spearphishing Attachment"},
            {"id": "T1059.001", "name": "PowerShell"},
        ]

    def get_tactic_counts(self):
        return DEMO_TACTIC_COUNTS