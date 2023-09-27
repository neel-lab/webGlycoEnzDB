# Run this app with `python app.py` and
# visit http://127.0.0.1:5000/GlycoEnzDB/human/FUT1/?gene_name=FUT1 in your web browser. Pass the Gene name in the `gene_name` url parameter

import os

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from urllib.parse import urlparse, parse_qs

# %% Define directories
mainDir = os.getcwd()
print('Current working directory: ', mainDir)
heirDir = os.path.join(mainDir, 'inputfiles')
meta_cols = ['cell_id', 'tissue_in_publication', 'cell_type', 'compartment']
sel_gene = 'FPGT' #'A4GALT'
ccle_gene_expr = pd.read_parquet(os.path.join(heirDir, 'CCLE_data_expr.parquet.gzip'), engine='pyarrow')
                                #  columns=['Tissue', 'DepMapID', 'display name'] + [sel_gene])

ccle_gene_expr['Tissue'] = ccle_gene_expr['Tissue'].astype('category')
ccle_gene_expr['display name'] = ccle_gene_expr['display name'].astype('category')

gene_expr_wmeta = (
    pd.read_parquet(os.path.join(heirDir, ''.join(['_'.join(['TS_scvi', 'all', 'glyco']), '_expr.parquet.gzip'])),
                    engine='pyarrow'))
                    # columns=meta_cols + [sel_gene]))
gene_expr_wmeta['compartment'] = gene_expr_wmeta['compartment'].astype('category')
gene_expr_wmeta['tissue_in_publication'] = gene_expr_wmeta['tissue_in_publication'].astype('category')
gene_expr_wmeta['cell_type'] = gene_expr_wmeta['cell_type'].astype('category')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# %% App title
# overall_title = html.H1(sel_gene, style={'textAlign': 'center'})
tabula_plot_color = '#F4F4F4 '
# %% CCLE dataset components

violin_0_graph = dbc.Row(dcc.Graph(id='tissue-violin0', style={'width': '95%'}), justify='center')

# %% Single cell dataset components
tabula_background_col = '#DAE2FE'
tabula_background_col2 = '#DAE2FE'

# tabula_title = html.H3('Single cell', style={'textAlign': 'center', 'padding-top': '0.3em',
#                                              'margin-top': 10})  # , 'background-color': '#FFF0E3'
violin_1_graph = dcc.Graph(id='tissue-violin', style={})
violin_1_comp = dbc.Col([html.B(['Compartment: '],
                                style={'margin-left': '5em', 'width': '50%', 'margin-top': '20px'}),
                         dcc.Dropdown(id='compartment-dropdown',
                                      options=gene_expr_wmeta['compartment'].cat.categories.tolist(),
                                      value='endothelial',
                                      placeholder='Select a compartment',
                                      clearable=False,
                                      style={'margin-left': '2.5em', 'margin-top': '0px', 'width': '50%'}),
                         violin_1_graph
                         ], align='center',
                        style={'background-color': tabula_background_col, 'margin-top': 10,
                               'width': '95%'})

violin_2_graph = dcc.Graph(id='cell-type-violin', style={})
violin_2_comp = dbc.Col([html.B(['Tissue: '], style={'margin-left': '5em', 'width': '50%', 'margin-top': '10px'}),
                         dcc.Dropdown(id='tissue-dropdown',
                                      options=['all'] + gene_expr_wmeta[
                                          'tissue_in_publication'].cat.categories.tolist(),
                                      value='Bladder',
                                      placeholder='Select a tissue',
                                      clearable=False,
                                      style={'margin-left': '2.5em', 'margin-top': '0px', 'width': '50%'}),
                         violin_2_graph
                         ], align='center',
                        style={'background-color': tabula_background_col, 'width': '95%'})

app.layout = html.Div(
    dbc.Stack([violin_0_graph,
             violin_1_comp,
             violin_2_comp,
             dcc.Location(id='url', refresh=False)
             ], className='g-0', style={'margin-top': 10}), className='g-0')

@app.callback(Output('tissue-violin0', 'figure'),
              Input('url', 'search'))
def update_graph0(search):
    # Parse the search string
    parsed_query = parse_qs(urlparse(search).query)
    # Get the value of the "gene_name" parameter
    sel_gene = parsed_query.get("gene_name", [None])[0]
    fig0 = go.Figure()

    if not sel_gene:
        return fig0

    sel_ccle_gene_expr = ccle_gene_expr[['Tissue', 'DepMapID', 'display name', sel_gene]]
    for tissue in sel_ccle_gene_expr['Tissue'].cat.categories:
        text = ['Cell type: '+e for e in sel_ccle_gene_expr['display name'][sel_ccle_gene_expr['Tissue'] == tissue]]
        fig0.add_trace(
            go.Violin(x=sel_ccle_gene_expr['Tissue'][sel_ccle_gene_expr['Tissue'] == tissue],
                    y=sel_ccle_gene_expr[sel_gene][sel_ccle_gene_expr['Tissue'] == tissue],
                    hovertext=text,
                    box_visible=False, name=tissue, points='all', pointpos=0))

    fig0.update_layout(yaxis_zeroline=True,
                    showlegend=False,
                    yaxis_title='Normalized expression',
                    xaxis_title='Tissues',
                    title={'text': '<b>CCLE dataset</b>',
                            'xanchor': 'left',
                            'yanchor': 'top',
                            'xref': 'paper',
                            'x': 0
                            },
                    plot_bgcolor=tabula_plot_color,
                    paper_bgcolor='#FFF0E3',
                    margin={'t': 40, 'b': 40},
                    height=300)

    return fig0

@app.callback(Output('tissue-violin', 'figure'),
              Input('compartment-dropdown', 'value'),
              Input('url', 'search'))
def update_graph(sel_comp, search):
        # Parse the search string
    parsed_query = parse_qs(urlparse(search).query)
    # Get the value of the "gene_name" parameter
    sel_gene = parsed_query.get("gene_name", [None])[0]

    dff = gene_expr_wmeta[gene_expr_wmeta['compartment'] == sel_comp]
    fig = go.Figure()

    for tissue in dff['tissue_in_publication'].cat.categories:
        fig.add_trace(
            go.Violin(x=dff['tissue_in_publication'][dff['tissue_in_publication'] == tissue],
                      y=dff[sel_gene][dff['tissue_in_publication'] == tissue],
                      box_visible=True, name=tissue))

    fig.update_layout(yaxis_zeroline=True,
                      showlegend=False,
                      title={'text': '<b>Single-cell: Gene expression in ' + sel_comp + ' cells</b>',
                             'xanchor': 'left',
                             'yanchor': 'top',
                             'xref': 'paper',
                             'x': 0
                             },
                      yaxis_title='Normalized expression',
                      xaxis_title='Tissues',
                      plot_bgcolor=tabula_plot_color,
                      paper_bgcolor=tabula_background_col,
                      margin={'t': 40, 'b': 40},
                      height=250)

    return fig


@app.callback(Output('cell-type-violin', 'figure'),
              Input('compartment-dropdown', 'value'),
              Input('tissue-dropdown', 'value'),
              Input('url', 'search'))
def update_graph2(sel_comp, sel_tissue, search):

        # Parse the search string
    parsed_query = parse_qs(urlparse(search).query)
    # Get the value of the "gene_name" parameter
    sel_gene = parsed_query.get("gene_name", [None])[0]

    dff1 = gene_expr_wmeta[gene_expr_wmeta['compartment'] == sel_comp]
    if sel_tissue == 'all':
        dff = dff1
    else:
        dff = dff1[dff1['tissue_in_publication'] == sel_tissue]
    fig = go.Figure()
    for cell_type in dff['cell_type'].cat.categories:
        fig.add_trace(
            go.Violin(x=dff['cell_type'][dff['cell_type'] == cell_type],
                      y=dff[sel_gene][dff['cell_type'] == cell_type],
                      box_visible=True, name=cell_type))

    fig.update_layout(yaxis_zeroline=True,
                      showlegend=False,
                      title={
                          'text': '<b>Single-cell: Gene expression of ' + sel_comp + ' cells in ' + sel_tissue + ' tissue</b>',
                          'xanchor': 'left',
                          'yanchor': 'top',
                          'xref': 'paper',
                          'x': 0
                          },
                      yaxis_title='Normalized expression',
                      xaxis_title='Cell Types',
                      plot_bgcolor=tabula_plot_color,
                      paper_bgcolor=tabula_background_col,
                      margin={'t': 40, 'b': 40},
                      height=250
                      )

    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=5000)
