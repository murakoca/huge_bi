import networkx as nx
from pyvis.network import Network
import sqlite3

CATALOG_DB = "catalog.db"

def build_lineage_graph():
    G = nx.DiGraph()
    conn = sqlite3.connect(CATALOG_DB)
    # datasets -> transformations -> reports
    datasets = conn.execute("SELECT id, name FROM datasets").fetchall()
    for ds_id, name in datasets:
        G.add_node(f"ds_{ds_id}", label=name, group="dataset", title=f"Veri Seti: {name}")
    transforms = conn.execute("SELECT id, dataset_id, step_name FROM transformations").fetchall()
    for t_id, ds_id, step in transforms:
        G.add_node(f"tr_{t_id}", label=step, group="transform")
        G.add_edge(f"ds_{ds_id}", f"tr_{t_id}")
    # Reports
    reports = conn.execute("SELECT name FROM reports").fetchall()  # bu tablo oluşturulmalı
    for rep_name, in reports:
        G.add_node(f"rep_{rep_name}", label=rep_name, group="report")
        # her transformun sonuncusuna bağla (basitlik)
        last_tr = transforms[-1] if transforms else None
        if last_tr:
            G.add_edge(f"tr_{last_tr[0]}", f"rep_{rep_name}")
    conn.close()
    return G

def generate_pyvis_html(G):
    net = Network(height="500px", width="100%", directed=True)
    net.from_nx(G)
    net.toggle_physics(True)
    return net.generate_html()