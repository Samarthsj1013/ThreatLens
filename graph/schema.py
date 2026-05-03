from py2neo import Graph
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def create_constraints():
    """
    Create uniqueness constraints in Neo4j for clean data.
    Run this once on setup.
    """
    graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Technique) REQUIRE t.technique_id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Report) REQUIRE r.source IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Target) REQUIRE t.name IS UNIQUE",
    ]

    for constraint in constraints:
        try:
            graph.run(constraint)
            print(f"✅ Constraint created")
        except Exception as e:
            print(f"⚠️  Constraint note: {e}")

    print("✅ Schema setup complete")


if __name__ == "__main__":
    create_constraints()