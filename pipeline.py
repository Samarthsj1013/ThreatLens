from ingestion.ingestor import ingest
from mapping.ner_extractor import extract_entities
from mapping.attack_mapper import load_mitre_data, build_technique_lookup, map_ttps_to_attack
from graph.graph_db import GraphDB
from graph.schema import create_constraints


def run_pipeline(source: str) -> dict:
    """
    Full pipeline: ingest → extract → map → store
    """
    print(f"\n{'='*50}")
    print(f"🚀 Running ThreatLens Pipeline")
    print(f"📥 Source: {source}")
    print(f"{'='*50}")

    # Step 1: Ingest
    print("\n[1/4] Ingesting source...")
    ingested = ingest(source)
    text = ingested["full_text"]
    print(f"✅ Ingested {len(text)} characters")

    # Step 2: Extract entities
    print("\n[2/4] Extracting entities with NER...")
    entities = extract_entities(text)
    print(f"✅ Found {len(entities['threat_actors'])} actors, {len(entities['ttps'])} TTPs, {len(entities['targets'])} targets")

    # Step 3: Map to MITRE ATT&CK
    print("\n[3/4] Mapping to MITRE ATT&CK...")
    mitre_data = load_mitre_data()
    technique_lookup = build_technique_lookup(mitre_data)
    mapped_ttps = map_ttps_to_attack(entities["ttps"], technique_lookup)
    print(f"✅ Mapped {len(mapped_ttps)} techniques")

    # Step 4: Store in Neo4j
    print("\n[4/4] Storing in knowledge graph...")
    db = GraphDB()
    db.store_intelligence(
        source=ingested["source"],
        source_type=ingested["source_type"],
        entities=entities,
        mapped_ttps=mapped_ttps
    )

    result = {
        "source": ingested["source"],
        "entities": entities,
        "mapped_ttps": mapped_ttps
    }

    print(f"\n{'='*50}")
    print(f"✅ Pipeline complete for: {ingested['source']}")
    print(f"{'='*50}\n")

    return result


if __name__ == "__main__":
    # Setup schema first
    print("Setting up Neo4j schema...")
    create_constraints()

    # Test with a sample URL
    test_url = "https://unit42.paloaltonetworks.com/unit42-sofacy-groups-parallel-attacks/"
    run_pipeline(test_url)