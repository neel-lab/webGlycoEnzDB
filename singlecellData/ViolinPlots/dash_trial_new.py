# Run this app with `python app.py` and
# visit http://127.0.0.1:5000/GlycoEnzDB/human/FUT1/?gene_name=FUT1 in your web browser. Pass the Gene name in the `gene_name` url parameter

import os

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme
from urllib.parse import urlparse, parse_qs

# %% Define directories
mainDir = os.getcwd()
print('Current working directory: ', mainDir)
heirDir = os.path.join(mainDir, 'inputfiles')

meta_cols = ['cell_id', 'tissue_in_publication', 'cell_type', 'compartment']
sel_gene = 'FPGT' #'A4GALT'

ccle_gene_expr = pd.read_parquet(os.path.join(heirDir, 'CCLE_data_expr.parquet.gzip'), engine='pyarrow')
                                 # , columns=['Tissue', 'DepMapID', 'display name'] + [sel_gene])
ccle_gene_expr['Tissue'] = ccle_gene_expr['Tissue'].astype('category')
ccle_gene_expr['display name'] = ccle_gene_expr['display name'].astype('category')

gene_expr_wmeta = (
    pd.read_parquet(os.path.join(heirDir, ''.join(['_'.join(['TS_scvi', 'all', 'glyco']), '_expr.parquet.gzip'])),
                    engine='pyarrow'))  # , columns=meta_cols + [sel_gene]))
gene_expr_wmeta['compartment'] = gene_expr_wmeta['compartment'].astype('category')
gene_expr_wmeta['tissue_in_publication'] = gene_expr_wmeta['tissue_in_publication'].astype('category')
gene_expr_wmeta['cell_type'] = gene_expr_wmeta['cell_type'].astype('category')

tabula_expr_summary = pd.read_csv(os.path.join(heirDir, 'tabulaSummaryTable_new.csv'), index_col=0)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# %% App title
# overall_title = html.H1(sel_gene, style={'textAlign': 'center'})

tabula_plot_color = '#F4F4F4'

# %% CCLE dataset components
# %% CCLE summary table

gene_disp_columns = ([{"name": "Tissue type", "id": "Tissue"},
                      {"name": "Cell name", "id": "display name"}] +
                     [{"name": i, "id": i, "format": Format(precision=3, scheme=Scheme.fixed), "type": "numeric"} for i
                      in ccle_gene_expr.columns[3:]])

table_0 = dbc.Offcanvas(id="offcanvas", title="CCLE", is_open=False)
offcanvas = dbc.Col([dbc.Button([html.I(className="bi bi-info-circle-fill me-2"), "Data"], color="primary",
                                id="open-offcanvas", n_clicks=0, style={'margin': 5}),
                     table_0],
                    className="justify-content-md-start", style={'width': '95%', 'background-color': '#FFF0E3'},
                    align='center')

# %% CCLE Violin

violin_0_graph = dbc.Row(dcc.Graph(id='tissue-violin0', style={'width': '95%'}), justify='center')

# %% Single cell dataset components
tabula_background_col = '#DAE2FE'

# Tabula summary table
table_1 = dbc.Offcanvas(id="offcanvas1", title="Single cell", is_open=False, style={'width': '45%'})

offcanvas_tabula = dbc.Col([dbc.Button([html.I(className="bi bi-info-circle-fill me-2"), "Data"], color="primary",
                                       id="open-offcanvas1", n_clicks=0, style={'margin': 5}),
                            table_1],
                           className="justify-content-md-start",
                           style={'width': '95%', 'background-color': tabula_background_col, 'margin-top': 10},
                           align='center')

# %% Tabula violin 1
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
                        style={'background-color': tabula_background_col, 'margin-top': 0,
                               'width': '95%'})

# %% Tabula violin 2
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
    dbc.Stack([offcanvas,
               violin_0_graph,
               offcanvas_tabula,
               violin_1_comp,
               violin_2_comp,
               dcc.Location(id='url', refresh=False)
               ], className='g-0', style={'margin-top': 10}), className='g-0')


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output("offcanvas1", "is_open"),
    Input("open-offcanvas1", "n_clicks"),
    [State("offcanvas1", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(Output('tissue-violin0', 'figure'),
              Output('offcanvas', 'children'),
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

    gene_disp_columns = ([{"name": "Tissue type", "id": "Tissue"},
                          {"name": "Cell name", "id": "display name"}] +
                         [{"name": i, "id": i, "format": Format(precision=3, scheme=Scheme.fixed), "type": "numeric"}
                          for i in ccle_gene_expr.columns[3:]])

    table_0_plot = dash_table.DataTable(data=ccle_gene_expr.to_dict('records'),
                                        columns=gene_disp_columns,
                                        id='tissue-table0',
                                        hidden_columns=sorted(set(ccle_gene_expr.columns[3:]) - {sel_gene}),
                                        page_size=10,
                                        fixed_rows={'headers': True},
                                        style_cell={'height': 'auto', 'textAlign': 'left', 'minWidth': '60px',
                                                    'maxWidth': '180px'},
                                        style_cell_conditional=[
                                            {'if': {'column_type': 'numeric'}, 'textAlign': 'right'},
                                            {'if': {'column_id': 'display name'}, 'width': '100px'}
                                            ],
                                        style_header={'backgroundColor': '#1E1E1E', 'fontWeight': 'bold',
                                                      'color': 'white'},
                                        style_data={'whiteSpace': 'normal', 'height': 'auto', 'color': 'black',
                                                    'backgroundColor': '#C1C1C1', 'border': '1px solid black'},
                                        style_data_conditional=[
                                            {'if': {'row_index': 'odd'}, 'color': 'black', 'backgroundColor': 'white'}],
                                        style_table={'height': '350px', 'weight': '100px', 'overflowY': 'auto',
                                                     'overflowX': 'auto'},
                                        sort_action="native",
                                        sort_mode='multi',
                                        export_format="xlsx", export_columns='all',
                                        css=[{"selector": ".show-hide", "rule": "display: none"},
                                             {"selector": ".export:after", "rule": 'content: " raw data"'}])

    return fig0, table_0_plot


@app.callback(Output('tissue-violin', 'figure'),
              Output('offcanvas1', 'children'),
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

    gene_disp_columns_tabula = ([{"name": ["", "Tissue"], "id": "Tissue"},
                                 {"name": ["", "Cell type"], "id": "Cell type"},
                                 {"name": ["", "Compartment"], "id": "Compartment"}])
    for gene_temp in tabula_expr_summary.columns[3:]:
        if gene_temp.endswith('expression'):
            gene_disp_columns_tabula.append(
                {"name": [gene_temp.split('_', 1)[0].replace('.', ''), "Median expression"], "id": gene_temp,
                 "type": "numeric", "format": Format(precision=3, scheme=Scheme.fixed)})
        else:
            gene_disp_columns_tabula.append(
                {"name": [gene_temp.split('_', 1)[0].replace('.', ''), "STD"], "id": gene_temp,
                 "type": "numeric", "format": Format(precision=3, scheme=Scheme.fixed)})

    table_1_plot = dash_table.DataTable(data=tabula_expr_summary.to_dict('records'),
                                        columns=gene_disp_columns_tabula,
                                        id='tissue-table1',
                                        hidden_columns=[i for i in tabula_expr_summary.columns[3:] if
                                                        not i.split('_', 1)[0]==sel_gene],
                                        page_size=10,
                                        fixed_rows={'headers': True},
                                        style_cell={'height': 'auto', 'textAlign': 'left', 'minWidth': '60px',
                                                    'maxWidth': '180px'},
                                        style_cell_conditional=[
                                            {'if': {'column_type': 'numeric'}, 'textAlign': 'right'},
                                            {'if': {'column_id': 'display name'}, 'width': '100px'}
                                            ],
                                        style_header={'backgroundColor': '#1E1E1E', 'fontWeight': 'bold',
                                                      'color': 'white'},
                                        style_data={'whiteSpace': 'normal', 'height': 'auto', 'color': 'black',
                                                    'backgroundColor': '#C1C1C1', 'border': '1px solid black'},
                                        style_data_conditional=[
                                            {'if': {'row_index': 'odd'}, 'color': 'black',
                                             'backgroundColor': 'white'}],
                                        style_table={'height': '350px', 'weight': '100px', 'overflowY': 'auto',
                                                     'overflowX': 'auto'},
                                        sort_action="native",
                                        sort_mode='multi',
                                        export_format="xlsx", export_columns='all',
                                        css=[{"selector": ".show-hide", "rule": "display: none"},
                                             {"selector": ".export:after", "rule": 'content: " raw data"'}])

    return fig, table_1_plot


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


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
