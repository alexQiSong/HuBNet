# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, dash_table, Input, Output, State
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title = "HuBNet")
server = app.server

df = pd.read_csv("data/network_all.csv").iloc[:,2:]

# Specify the layout of the navigation bar at the top
navbar = dbc.Navbar(
            dbc.Container(
                [
                    
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src = "assets/hubnet_logo.png", height = "50px")),
                                dbc.Col(dbc.NavbarBrand("HuBNet", className="ms-2"))
                            ],
                            align="center",
                            className="g-0"
                        ),
                        href="#",
                        style={"textDecoration":"none"},
                    ),
                    html.Span(
                        [
                            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                            dbc.Collapse(
                                [
                                    dbc.NavItem(
                                        dbc.NavLink("Systems Biology Group", href="http://sb.cs.cmu.edu/", style = {"color":"#adadad"}),
                                    ),
                                    dbc.NavItem(
                                        dbc.NavLink("HuBMAP Project", href="https://portal.hubmapconsortium.org/", style = {"color":"#adadad"}),
                                    )
                                ],
                                id="navbar-collapse",
                                is_open = False,
                                navbar = True,
                            ),
                        ],
                        className = "ml-auto"
                    )
                ],
        ),
    color="dark",
    dark=True,
    fixed="top"
)   

# Specify the layout of the Query tab
query = dbc.Container(
    [
        dbc.Row(
            [
                dcc.Markdown(
                    """
                    ##### **How to use**
                    """,
                    style = {"marginTop":10,"marginLeft":25}
                ),
                dcc.Markdown(
                    """
                    -----
                    """,
                    style = {"marginTop":10,"marginLeft":25,"color":"#b0b0b0"}
                ),
                dcc.Markdown(
                    """
                    - Enter TF/target names (separated by semicolons).
                    
                    - Select a tissue.
                    
                    - If you need to retrive all TFs/targets for the given targets/TFs, simply leave the boxes empty.
                    
                    - Query results will be shown in the table on the left.
                    
                    - The corresponding network will be shown on the right.  
                    """,
                    style = {"marginTop":10,"marginLeft":25}
                ),
                dcc.Markdown(
                    """
                    -----
                    """,
                    style = {"marginLeft":25,"color":"#b0b0b0"}
                ),
                
                dbc.Row(
                    [
                        "Enter TF name(s):  ",
                        dbc.Input(id='tf-name-input', value = 'FOS;JUN', type='text'),
                    ],
                    style = {"width":400,"marginTop":20,"marginLeft":25}
                ),
                    
                dbc.Row(
                    [
                        "Enter target name(s):  ",
                        dbc.Input(id='target-name-input',value = 'ARHGEF40;HES4;WDR86-AS1;S100A10;FCRL5;CASP4LP;RGCC;PLAAT4;ZBTB38;TNF;ARHGEF3;CEMIP2;HBA1;OTULIN-DT;ID3;KLRF1;COLQ;FASLG', type = 'text'),
                    ],
                    style = {"width":400,"marginTop":20,"marginLeft":25}
                ),
                
                dbc.Row(
                    [
                        "Select a tissue:",
                        dcc.Dropdown(
                            id = 'tissue-name-input',
                            options = [
                                'Liver',
                                'Heart',
                                'Spleen',
                                'Left kidney',
                                'Right Lung',
                                'Large intestine'
                                ],
                            value = 'Spleen',
                            
                        ),
                    ],
                    style = {"width":200,"marginTop":20,"marginLeft":10}
                ),
                
            ],
        ),
        dbc.Row(
            align = "start",
            children = [
                dbc.Col(
                    id = "table-container",
                    children = [],
                    sm = 12,
                    md = 4,
                    style = {"width":550,"height":600,'overflowY': 'scroll', "marginLeft":25,"marginTop":25}
                ),
                dbc.Col(
                    id = "network-vis-container",
                    align = "end",
                    children = [],
                    sm = 12,
                    md = 4,
                    style = {"width": 550, "height":600,'overflowY':'hidden',"marginLeft":25, "marginTop":25}
                )
            ],
            style = {"marginTop":25}
        ),
        dcc.Markdown(
                    """
                    -----
                    """,
                    style = {"marginTop":40,"marginLeft":25,"color":"#b0b0b0"}
                ),
        dcc.Markdown(
            """
            Systems Biology Group · School of Computer Science · Carnegie Mellon University  
            5000 Forbes Avenue · Pittsburgh, PA 15213  
            © HuBNet v0.1; Created by Qi (Alex) Song
            """,
            style = {"marginTop":25,"marginLeft":25,"text-align":"center","color":"#949494"}
        )
    ],
    style = {"paddingBottom":25,"paddingRight":50}
)

# Specify the layout of all tabs
tabs = dbc.Container(
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                         [
                            dbc.Tab(
                                tab_id = "query_tab",
                                label = "Query",
                                label_style = {"font-weight":"bold","font-size":"120%","color":"#4d4d4d"},
                                tab_class_name = "flex-grow-1 text-center"
                            ),
                            dbc.Tab(
                                tab_id = "statistics_tab",
                                label = "Statistics",
                                label_style = {"font-weight":"bold","font-size":"120%","color":"#4d4d4d"},
                                tab_class_name = "flex-grow-1 text-center"
                            ),
                            dbc.Tab(
                                tab_id = "about_tab",
                                label = "About",
                                label_style = {"font-weight":"bold","font-size":"120%","color":"#4d4d4d"},
                                tab_class_name = "flex-grow-1 text-center"
                            ),
                            dbc.Tab(
                                tab_id = "download_tab",
                                label = "Download Data",
                                label_style = {"font-weight":"bold","font-size":"120%","color":"#4d4d4d"},
                                tab_class_name = "flex-grow-1 text-center"
                            ), 
                         ],
                         id = "tabs",
                         active_tab = "query_tab"
                    )
                ),
                dbc.CardBody(
                    id = "tab-content",
                    children = []
                ),
            ],
            style = {"marginTop":80}
    )
)
# Specify the layout of the entire app  
app.layout = html.Div(
    id = "main-container",
    children = [
        navbar,
        tabs,
        dcc.Store(id = "table-data")
    ],
    style = {"background-color":"#f7f7f7"}
    )

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
    
# Generate different content for different tab page
@app.callback(
    Output("tab-content","children"),
    [Input("tabs","active_tab")]
)
def generate_tab_content(active_tab):
    if active_tab == "query_tab":
        return query
    if active_tab == "statistics_tab":
        return dbc.Container(
            [
                html.P("Comming soon!", className = "card-text",style = {"marginLeft":25}),
                dcc.Markdown(
                    """
                    -----
                    """,
                    style = {"marginTop":40,"marginLeft":25,"color":"#b0b0b0"}
                ),
                dcc.Markdown(
                    """
                    Systems Biology Group · School of Computer Science · Carnegie Mellon University  
                    5000 Forbes Avenue · Pittsburgh, PA 15213  
                    © HuBNet v0.1; Created by Qi (Alex) Song 
                    """,
                    style = {"marginTop":25,"marginLeft":25,"text-align":"center","color":"#949494"}
                )
            ],
            style = {"marginTop":20}
        )
    if active_tab == "download_tab":
        return dbc.Container(
            [
                
                dbc.Button(
                    "Download",
                    id = "download-btn",
                    className="me-1",
                    href="/static/network_all.csv",
                    external_link = True,
                    style = {"background-color":"#f0f0f0", "border-color":"#d1d1d1","color":"#4d4d4d","font-weight":"bold","marginLeft":25}
                ),
                dcc.Markdown(
                    """
                    -----
                    """,
                    style = {"marginTop":40,"marginLeft":25,"color":"#b0b0b0"}
                ),
                dcc.Markdown(
                    """
                    Systems Biology Group · School of Computer Science · Carnegie Mellon University  
                    5000 Forbes Avenue · Pittsburgh, PA 15213  
                    © HuBNet v0.1; Created by Qi (Alex) Song  
                    """,
                    style = {"marginTop":25,"marginLeft":25,"text-align":"center","color":"#949494"}
                )
            ],
            style = {"marginTop":20}
        )
    if active_tab == "about_tab":
        return dbc.Container(
            [
                html.P("Comming soon!", className = "card-text",style = {"marginLeft":25}),
                dcc.Markdown(
                    """
                    -----
                    """,
                    style = {"marginTop":40,"marginLeft":25,"color":"#b0b0b0"}
                ),
                dcc.Markdown(
                    """
                    Systems Biology Group · School of Computer Science · Carnegie Mellon University  
                    5000 Forbes Avenue · Pittsburgh, PA 15213  
                    © HuBNet v0.1; Created by Qi (Alex) Song
                    """,
                    style = {"marginTop":25,"marginLeft":25,"text-align":"center","color":"#949494"}
                )
            ],
            style = {"marginTop":20}
        )
    
    
@app.callback(
    Output('network-vis-container','children'),
    Input("table-data",'data')
)
def generate_network(data):
    # Convert json data to dataframe
    query_df = pd.read_json(data, orient = "columns")
    
    # Create gene names to ids mapping and node data for network visualization
    node_data = []
    name2id = dict()
    for idx,name in enumerate(pd.concat([query_df["TF name"],query_df["Target name"]]).unique()):
        name2id[name] = str(idx)
        node_data.append({'data':{'id':str(idx), 'label':name}})
    
    # Go through edges and generate edge data for network visualization
    edge_data = []
    for idx,row in query_df.iterrows():
        if row["TF name"] is not None and row['Target name'] is not None:
            edge_data.append({'data':{'source':name2id[row["TF name"]],'target':name2id[row["Target name"]]}})
    
    return[cyto.Cytoscape(
                    id="network_vis",
                    layout={"name": "cose"},
                    #style={"width": "500px", "height": "500px"},
                    elements= node_data + edge_data,
                    #stylesheet=def_stylesheet,
                    minZoom=0.5,
                    maxZoom=3,
                    zoom=1
          )]

@app.callback(
    Output('table-container','children'),
    Output('table-data','data'),
    Input('tf-name-input','value'),
    Input('target-name-input','value'),
    Input('tissue-name-input','value')
)
def generate_table(tf_names,target_names,tissue_name):
    
    df.columns = ["TF name","Target name","TF Marker","Score","Tissue"]
    
    # Remove spaces in the left and right and convert to captial letters.
    tf_names = tf_names.strip().upper()
    target_names = target_names.strip().upper()
    
    # If user leave the input box empty. All TFs/targets of the selected tissue will be returned
    if tf_names == "":
        select1 = df["Tissue"] == tissue_name
    else:
        tf_names = tf_names.split(";")
        select1 = df["TF name"].isin(tf_names)
        
    if target_names == "":
        select2 = df["Tissue"] == tissue_name
    else:
        target_names = target_names.split(";")
        select2 = select2 = df["Target name"].isin(target_names)
 
    select3 = df["Tissue"] == tissue_name
    query_df = df.loc[select1 & select2 & select3,]
    
    # Jsonified the dataframe and store it in "table-data"
    query_js = query_df.loc[:,["TF name","Target name","Score"]].to_json(orient = "columns")
    
    return [dash_table.DataTable(
        id="table",
        sort_action="native",
        filter_action="native",
        row_deletable=True,
        #css=[{
        #    "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;"
        #}],
        style_data={"whiteSpace": "normal"},
        style_cell={
            "padding": "15px",
            "midWidth": "0px",
            "width": "25%",
            "textAlign": "center",
            "border": "grey",
        },
        style_data_conditional=[
            {"if": {"row_index": "even"}, "backgroundColor": "#EFEFEF"}
        ],
        columns=[{"name": i, "id": i} for i in df.columns],
        data=query_df.to_dict("rows"),
    )],query_js
    
if __name__ == '__main__':
    app.run_server(debug=True)