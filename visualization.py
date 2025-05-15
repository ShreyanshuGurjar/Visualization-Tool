import dash
from dash import dcc, html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from collections import Counter
import os

# === Load graph data from a TSV file ===
def parse_ppi_graph(path):

    df = pd.read_csv(path, sep='\t', header=None, names=['source', 'interaction', 'target'])

    # Count node degrees
    node_counts = Counter(df['source'].tolist() + df['target'].tolist())
    top_nodes = set([node for node, _ in node_counts.most_common(5)])


    edges = [{'data': {'source': row['source'], 'target': row['target']}} for _, row in df.iterrows()]
    nodes = []
    for node in set(df['source']).union(set(df['target'])):
        if node in top_nodes:
            style = {
                'background-color': 'red',
                'width': 40,
                'height': 40
            }
        else:
            style = {
                'width': 20,
                'height': 20
            }
        
        nodes.append({
            'data': {'id': node, 'label': node},
            'style': style
        })

    return nodes, edges


# === Function to parse pathway activity TSV file ===
def parse_pathways(path):
    df = pd.read_csv(path, sep='\t', header=None, names=['Pathway', 'Activity'])
    return df


# Preload graphs

datasets = {
    'Breast Cancer': {
        'graph': parse_ppi_graph('graph_BRC.tsv'),
        'pathway': parse_pathways('pathways_BRC.tsv')
    },
    'Ovarian Cancer': {
        'graph': parse_ppi_graph('graph_OV.tsv'),
        'pathway': parse_pathways('pathways_OV.tsv')
    },
    'Enometrial Cancer': {
        'graph': parse_ppi_graph('graph_EC.tsv'),
        'pathway': parse_pathways('pathways_EC.tsv')
    }
}




# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server


# Layout
app.layout = html.Div([
    html.H1("Cancer-specific PPI Networks & Metabolic Pathway Activities"),

    html.Div([
        html.Label("Select Dataset"),
        dcc.Dropdown(
            id='dataset-selector',
            options=[{'label': name, 'value': name} for name in datasets.keys()],
            value=next(iter(datasets))  # Default to the first graph
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        cyto.Cytoscape(
            id='cytoscape-network',
            layout={'name': 'cose'},
            style={'width': '100%', 'height': '600px','border': '2px solid #ddd','borderRadius': '8px'},
            elements=[],
            stylesheet=[
                {'selector': 'node', 'style': {'label': 'data(label)'}},
                # {'selector': '.top-node', 'style': {'background-color': 'red'}}
            ]
        )
    ], style={'width': '100%', 'margin': '20px 0'}),

    html.Div([
        html.H2("Metabolic Pathway Activities"),
        dcc.Graph(
        id='pathway-activity-graph',
        figure=px.bar(
            pd.DataFrame({
                "Pathway": [],
                "Activity": pd.Series([], dtype="int")
            }),
            x='Pathway',
            y='Activity',
            title="Pathway Activity Scores",
            labels={"Activity": "Activity Score"}
            ).update_layout(
                paper_bgcolor='#ffefd5',  
                # plot_bgcolor='rgba(0,0,0,0)',  # transparent plot area
                font=dict(color='#333'),  # text color
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200, 200, 200, 0.3)',  # subtle grid lines
                    zeroline=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200, 200, 200, 0.3)',
                    zeroline=False
                )
            )   
        )

    ])
],
style={
    'background': 'linear-gradient(to bottom right, #ffefd5 30%, #f0f4f8 100%)',
    'height': '100vh',
    'margin': 0,
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif'
}

)

# Callback
@app.callback(
    [Output('cytoscape-network', 'elements'),
     Output('pathway-activity-graph', 'figure')],
    [Input('dataset-selector', 'value')]
)
def update_content(dataset_name):
    nodes, edges = datasets[dataset_name]['graph']
    df_pathways = datasets[dataset_name]['pathway']
    fig = px.bar(df_pathways, x='Pathway', y='Activity', title=f'{dataset_name} Pathway Activity')
    return nodes + edges, fig

print("Starting Dash app...")
if __name__ == '__main__':
    app.run(debug=True)
