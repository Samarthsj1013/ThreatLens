from py2neo import Graph
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class GraphStats:
    def __init__(self):
        self.graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def get_summary(self) -> dict:
        result = self.graph.run("""
            MATCH (n)
            RETURN labels(n)[0] AS label, COUNT(n) AS count
        """).data()

        summary = {r["label"]: r["count"] for r in result}

        rel_count = self.graph.run("""
            MATCH ()-[r]->() RETURN COUNT(r) AS count
        """).evaluate()

        summary["relationships"] = rel_count
        return summary