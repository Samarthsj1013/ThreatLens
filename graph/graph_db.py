from py2neo import Graph, Node, Relationship
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class GraphDB:
    def __init__(self):
        self.graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        print("✅ Connected to Neo4j")

    def create_threat_actor(self, name: str) -> Node:
        existing = self.graph.nodes.match("ThreatActor", name=name).first()
        if existing:
            return existing
        node = Node("ThreatActor", name=name)
        self.graph.create(node)
        return node

    def create_technique(self, technique_id: str, name: str, tactics: list, url: str) -> Node:
        existing = self.graph.nodes.match("Technique", technique_id=technique_id).first()
        if existing:
            return existing
        node = Node(
            "Technique",
            technique_id=technique_id,
            name=name,
            tactics=", ".join(tactics),
            url=url
        )
        self.graph.create(node)
        return node

    def create_target(self, name: str, target_type: str = "sector") -> Node:
        existing = self.graph.nodes.match("Target", name=name).first()
        if existing:
            return existing
        node = Node("Target", name=name, target_type=target_type)
        self.graph.create(node)
        return node

    def create_report(self, source: str, source_type: str) -> Node:
        existing = self.graph.nodes.match("Report", source=source).first()
        if existing:
            return existing
        node = Node("Report", source=source, source_type=source_type)
        self.graph.create(node)
        return node

    def link_actor_uses_technique(self, actor_node: Node, technique_node: Node):
        rel = Relationship(actor_node, "USES", technique_node)
        self.graph.merge(rel)

    def link_actor_targets(self, actor_node: Node, target_node: Node):
        rel = Relationship(actor_node, "TARGETS", target_node)
        self.graph.merge(rel)

    def link_report_mentions_actor(self, report_node: Node, actor_node: Node):
        rel = Relationship(report_node, "MENTIONS", actor_node)
        self.graph.merge(rel)

    def link_report_contains_technique(self, report_node: Node, technique_node: Node):
        rel = Relationship(report_node, "CONTAINS", technique_node)
        self.graph.merge(rel)

    def store_intelligence(self, source: str, source_type: str, entities: dict, mapped_ttps: list):
        """
        Master method — stores everything from one report into the graph.
        """
        report_node = self.create_report(source, source_type)

        # Store techniques
        technique_nodes = {}
        for ttp in mapped_ttps:
            t_node = self.create_technique(
                technique_id=ttp["technique_id"],
                name=ttp["name"],
                tactics=ttp.get("tactics", []),
                url=ttp.get("url", "")
            )
            technique_nodes[ttp["technique_id"]] = t_node
            self.link_report_contains_technique(report_node, t_node)

        # Store threat actors and link to techniques + targets
        for actor_name in entities.get("threat_actors", []):
            actor_node = self.create_threat_actor(actor_name)
            self.link_report_mentions_actor(report_node, actor_node)

            for t_node in technique_nodes.values():
                self.link_actor_uses_technique(actor_node, t_node)

        # Store targets
        for target_name in entities.get("targets", [])[:10]:
            target_node = self.create_target(target_name)
            for actor_name in entities.get("threat_actors", []):
                actor_node = self.create_threat_actor(actor_name)
                self.link_actor_targets(actor_node, target_node)

        print(f"✅ Stored intelligence for: {source}")