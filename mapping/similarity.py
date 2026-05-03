from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")


def find_similar_techniques(query: str, technique_lookup: dict, top_k: int = 5) -> list:
    """
    Use semantic similarity to find MITRE techniques
    that match a description even if exact keywords don't match.
    """
    technique_ids = list(technique_lookup.keys())
    technique_texts = [
        f"{v['name']} {v['description']}"
        for v in technique_lookup.values()
    ]

    query_embedding = model.encode(query, convert_to_tensor=True)
    corpus_embeddings = model.encode(technique_texts, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(scores, k=min(top_k, len(technique_ids)))

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        tid = technique_ids[idx]
        results.append({
            "technique_id": tid,
            "name": technique_lookup[tid]["name"],
            "tactics": technique_lookup[tid]["tactics"],
            "similarity_score": round(score.item(), 4),
            "url": technique_lookup[tid]["url"]
        })

    return results


if __name__ == "__main__":
    from mapping.attack_mapper import load_mitre_data, build_technique_lookup

    print("Loading MITRE data for similarity test...")
    data = load_mitre_data()
    lookup = build_technique_lookup(data)

    query = "attacker used stolen credentials to move between systems"
    print(f"\n🔍 Query: {query}")
    results = find_similar_techniques(query, lookup, top_k=3)
    for r in results:
        print(f"  {r['technique_id']} — {r['name']} (score: {r['similarity_score']})")