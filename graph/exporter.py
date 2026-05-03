import json
import csv
import os
from config import DATA_DIR


def export_to_json(graph_data: dict, filename: str = "threatlens_export.json") -> str:
    """Export full graph data to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)
    print(f"✅ Exported to {path}")
    return path


def export_techniques_to_csv(techniques: list, filename: str = "techniques.csv") -> str:
    """Export techniques list to CSV."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    if not techniques:
        return ""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=techniques[0].keys())
        writer.writeheader()
        writer.writerows(techniques)
    print(f"✅ Exported {len(techniques)} techniques to {path}")
    return path


def export_actors_to_csv(actors: list, queries, filename: str = "actors.csv") -> str:
    """Export actors with their technique counts to CSV."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    rows = []
    for actor in actors:
        techniques = queries.get_techniques_by_actor(actor)
        targets = queries.get_targets_by_actor(actor)
        rows.append({
            "actor": actor,
            "technique_count": len(techniques),
            "target_count": len(targets),
            "techniques": ", ".join([t["id"] for t in techniques])
        })
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["actor", "technique_count", "target_count", "techniques"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Exported {len(rows)} actors to {path}")
    return path