from py2neo import Graph
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class GraphQueries:
    def __init__(self):
        self.graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def get_all_actors(self) -> list:
        result = self.graph.run("""
            MATCH (a:ThreatActor)
            RETURN a.name AS actor
            ORDER BY a.name
        """).data()
        return [r["actor"] for r in result]

    def get_techniques_by_actor(self, actor_name: str) -> list:
        result = self.graph.run("""
            MATCH (a:ThreatActor {name: $name})-[:USES]->(t:Technique)
            RETURN t.technique_id AS id, t.name AS name, t.tactics AS tactics
            ORDER BY t.technique_id
        """, name=actor_name).data()
        return result

    def get_actors_by_technique(self, technique_id: str) -> list:
        result = self.graph.run("""
            MATCH (a:ThreatActor)-[:USES]->(t:Technique {technique_id: $tid})
            RETURN a.name AS actor
        """, tid=technique_id).data()
        return [r["actor"] for r in result]

    def get_targets_by_actor(self, actor_name: str) -> list:
        result = self.graph.run("""
            MATCH (a:ThreatActor {name: $name})-[:TARGETS]->(t:Target)
            RETURN t.name AS target, t.target_type AS type
        """, name=actor_name).data()
        return result

    def get_top_techniques(self, limit: int = 10) -> list:
        result = self.graph.run("""
            MATCH (a:ThreatActor)-[:USES]->(t:Technique)
            RETURN t.technique_id AS id, 
                   t.name AS name, 
                   t.tactics AS tactics,
                   COUNT(a) AS actor_count
            ORDER BY actor_count DESC
            LIMIT $limit
        """, limit=limit).data()
        return result

    def get_shared_techniques(self, actor1: str, actor2: str) -> list:
        result = self.graph.run("""
            MATCH (a1:ThreatActor {name: $a1})-[:USES]->(t:Technique)
            MATCH (a2:ThreatActor {name: $a2})-[:USES]->(t)
            RETURN t.technique_id AS id, t.name AS name
        """, a1=actor1, a2=actor2).data()
        return result

    def get_full_graph_data(self) -> dict:
        nodes_result = self.graph.run("""
            MATCH (n)
            RETURN labels(n)[0] AS label,
                   COALESCE(n.name, n.technique_id, n.source) AS name,
                   id(n) AS id
        """).data()

        edges_result = self.graph.run("""
            MATCH (a)-[r]->(b)
            RETURN id(a) AS source, id(b) AS target, type(r) AS relationship
        """).data()

        return {"nodes": nodes_result, "edges": edges_result}

    def get_tactic_counts(self) -> dict:
        """Get technique counts grouped by tactic — fixed for heatmap."""
        result = self.graph.run("""
            MATCH (a:ThreatActor)-[:USES]->(t:Technique)
            WHERE t.tactics IS NOT NULL AND t.tactics <> ''
            RETURN t.tactics AS tactics, COUNT(DISTINCT t) AS count
        """).data()

        tactic_counts = {}
        for row in result:
            tactics_str = row.get("tactics", "") or ""
            count = row.get("count", 0)
            for tactic in tactics_str.split(","):
                tactic = tactic.strip().lower()
                if tactic:
                    tactic_counts[tactic] = tactic_counts.get(tactic, 0) + count

        return tactic_counts