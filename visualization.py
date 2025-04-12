import dash
from dash import dcc, html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample Data: Nodes and Edges for a PPI Network
nodes = [
    {'data': {'id': 'Gene1', 'label': 'Gene1'}},
    {'data': {'id': 'Gene2', 'label': 'Gene2'}},
    {'data': {'id': 'Gene3', 'label': 'Gene3'}},
    {'data': {'id': 'Gene4', 'label': 'Gene4'}}
]

edges = [
    {'data': {'source': 'Gene1', 'target': 'Gene2'}},
    {'data': {'source': 'Gene2', 'target': 'Gene3'}},
    {'data': {'source': 'Gene3', 'target': 'Gene4'}},
    {'data': {'source': 'Gene1', 'target': 'Gene4'}}
]

# Sample Data: Metabolic Pathway Activities
df_pathways = pd.DataFrame({
    'Pathway': ['Glycolysis', 'Oxidative Phosphorylation', 'Cholesterol Metabolism'],
    'Activity': [0.8, 0.5, 0.6]
})

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the application
app.layout = html.Div([
    html.H1("Cancer-specific PPI Networks & Metabolic Pathway Activities"),

    html.Div([
        # Panel for PPI Network Visualization
        html.Div([
            html.H2("PPI Network Visualization"),
            cyto.Cytoscape(
                id='cytoscape-graph',
                elements=nodes + edges,
                layout={'name': 'cose'},
                style={'width': '100%', 'height': '400px'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        # Panel for Metabolic Pathway Activity
        html.Div([
            html.H2("Metabolic Pathway Activities"),
            dcc.Graph(
                id='pathway-activity-graph',
                figure=px.bar(df_pathways, x='Pathway', y='Activity',
                              title="Pathway Activity Scores",
                              labels={"Activity": "Activity Score"})
            )
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ]),

    # Interactive filter controls
    html.Div([
        html.H3("Network Filter Options"),
        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Show All', 'value': 'all'},
                {'label': 'Show only interactions involving Gene1', 'value': 'gene1'}
            ],
            value='all'
        )
    ], style={'width': '50%', 'margin': '20px auto'})
])

# Callback to update the network graph based on dropdown selection
@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('filter-dropdown', 'value')
)
def update_network(selected_filter):
    if selected_filter == 'all':
        return nodes + edges
    elif selected_filter == 'gene1':
        # Filter nodes and edges to only include those related to Gene1
        filtered_nodes = [node for node in nodes if node['data']['id'] == 'Gene1']
        filtered_edges = [edge for edge in edges 
                          if edge['data']['source'] == 'Gene1' or edge['data']['target'] == 'Gene1']
        return filtered_nodes + filtered_edges
    else:
        return nodes + edges

if __name__ == '__main__':
    app.run_server(debug=True)
