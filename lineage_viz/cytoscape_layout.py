import dash_cytoscape as cyto
def create_cytoscape_graph(elements):
    return cyto.Cytoscape(
        id='lineage-graph',
        elements=elements,
        style={'width': '100%', 'height': '500px'},
        layout={'name': 'breadthfirst'},
        stylesheet=[
            {'selector': 'node', 'style': {'label': 'data(label)'}},
            {'selector': '.dataset', 'style': {'background-color': '#1f77b4'}},
            {'selector': '.transform', 'style': {'background-color': '#ff7f0e'}},
            {'selector': '.report', 'style': {'background-color': '#2ca02c'}}
        ]
    )