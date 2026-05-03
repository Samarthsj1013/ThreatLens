from py2neo import Graph
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class TimelineDB:
    def __init__(self):
        self.graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def get_all_reports(self) -> list:
        result = self.graph.run("""
            MATCH (r:Report)
            RETURN r.source AS source, r.source_type AS source_type
            ORDER BY r.source
        """).data()
        return result