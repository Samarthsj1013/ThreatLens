import streamlit as st
import plotly.graph_objects as go
import networkx as nx


def render_graph(q):
    st.subheader("🕸️ Knowledge Graph Explorer")

    graph_data = q.get_full_graph_data()
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]

    if not nodes:
        st.info("No graph data yet — ingest a report first using the sidebar")
        return

    # Build networkx graph for layout
    G = nx.Graph()
    node_map = {}

    for n in nodes:
        node_id = n["id"]
        node_map[node_id] = n
        G.add_node(node_id)

    for e in edges:
        G.add_edge(e["source"], e["target"])

    pos = nx.spring_layout(G, seed=42, k=2)

    # Color by label
    color_map = {
        "ThreatActor": "#00ff88",
        "Technique": "#ff6b6b",
        "Target": "#ffd93d",
        "Report": "#6bceff"
    }

    # Build plotly traces
    edge_x, edge_y = [], []
    for e in edges:
        if e["source"] in pos and e["target"] in pos:
            x0, y0 = pos[e["source"]]
            x1, y1 = pos[e["target"]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(width=0.8, color="#444"),
        hoverinfo="none"
    )

    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for node_id, (x, y) in pos.items():
        n = node_map.get(node_id, {})
        label = n.get("label", "Unknown")
        name = n.get("name", str(node_id))
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{label}: {name}")
        node_color.append(color_map.get(label, "#888"))
        node_size.append(20 if label == "ThreatActor" else 14)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=1, color="#222")
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="#ffffff",
            height=600,
            showlegend=False,
            hovermode="closest",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=0, r=0, t=0, b=0)
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Legend
    st.markdown("""
    <div style='display:flex; gap:20px; margin-top:10px;'>
        <span>🟢 Threat Actor</span>
        <span>🔴 Technique</span>
        <span>🟡 Target</span>
        <span>🔵 Report</span>
    </div>
    """, unsafe_allow_html=True)