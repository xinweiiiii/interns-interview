import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import mysql.connector


name_title = 'Stats from SQL Server'
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, BS])


database = mysql.connector.connect(host="localhost", user="root", password="root", port=8889, db="financial_data")
cursor = database.cursor() #Read the database  

@app.callback(Output('example-graph', 'figure'), 
            [Input('graph-update', 'interval')])



def update_graph_scatter(input_data):

    cursor.execute("SELECT * from Profit_Loss")
    rows = cursor.fetchall()
    data_sql = []

    data_sql.append(rows[0])
    
    df = pd.DataFrame.from_records(data_sql)
    new_df = df.transpose()

    x = ["Year_2005", "Year_2006", "Year_2007", "Year_2008", "Year_2009", "Year_2010", "Year_2011", "Year_2012", "Year_2013", "Year_2014", "Year_2015", "Year_2016", "Year_2017", "Year_2018", "Year_2019"]
    y = new_df[0]

    data = plotly.graph_objs.Scatter(
        x=list(x),
        y=list(y),
        name='Scatter',
        mode= 'lines+markers'
    )

    return {'data': [data],'layout' : go.Layout(
                                    xaxis=dict(range=[min(x),max(x)]),
                                    yaxis=dict(range=[min(y),max(y)]),)}

def get_num_rows_all_data():
    cursor.execute("SELECT * from Profit_Loss")
    profit_loss = cursor.fetchall()
    no_of_profit_loss = len(profit_loss)

    cursor.execute("SELECT * from Balance_Sheet")
    balance_sheet = cursor.fetchall()
    no_of_balance_sheet = len(balance_sheet)

    cursor.execute("SELECT * from Cash_Flow")
    cash_flow = cursor.fetchall()
    no_of_cash_flow = len(cash_flow)

    cursor.execute("SELECT * from Financial_Ratio")
    Financial_Ratio = cursor.fetchall()
    no_of_financial_ratio = len(Financial_Ratio)

    total_data = no_of_financial_ratio + no_of_cash_flow + no_of_balance_sheet + no_of_profit_loss
    return [total_data, no_of_profit_loss, no_of_balance_sheet, no_of_cash_flow, no_of_financial_ratio]

def get_num_cols_data():
    cursor.execute("SELECT * from Profit_Loss")
    profit_loss = cursor.fetchall()
    col_count = len(profit_loss[0][0])

    return col_count

def retrieve_empty_data():
    cursor.execute("SELECT * from Profit_Loss")
    profit_loss = cursor.fetchall()
    counter_pl = 0
    for row in profit_loss:
        for col in row:
            if col == "-":
                counter_pl += 1

    cursor.execute("SELECT * from Balance_Sheet")
    balance_sheet = cursor.fetchall()
    counter_bs = 0
    for row in balance_sheet:
        for col in row:
            if col == "-":
                counter_bs += 1
    
    cursor.execute("SELECT * from Cash_Flow")
    cash_flow = cursor.fetchall()
    counter_cf = 0
    for row in cash_flow:
        for col in row:
            if col == "-":
                counter_cf += 1

    cursor.execute("SELECT * from Financial_Ratio")
    Financial_Ratio = cursor.fetchall()
    counter_fr = 0
    for row in Financial_Ratio:
        for col in row:
            if col == "-":
                counter_fr += 1

    total_empty = counter_pl + counter_fr + counter_cf + counter_bs

    return [total_empty,counter_pl,counter_bs, counter_cf, counter_fr]

row_count = get_num_rows_all_data()
col_count = get_num_cols_data()
empty_count = retrieve_empty_data()
total_data = col_count * row_count[0]

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
app.layout = dbc.Container(html.Div(children=[
    dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="#",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
        ],
        color="dark",
        dark=True,
        ),
    html.H1(""),
    html.H1(children="Revenue Data Breakdown"),
    dcc.Graph(
        id='example-graph',
        animate=True),
    dcc.Interval(
        id='graph-update',
           interval=1*500),
    dbc.Row(dbc.Col(html.H1(children="Metadata Breakdown"))),
    dbc.Row(
        [
            dbc.Col(html.Div("Total Data Row Count: ")),
            dbc.Col(html.Div("Total Data Column Count")),
            dbc.Col(html.Div("Total No of Empty Data")),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H3(row_count[0])),
            dbc.Col(html.H3(col_count)),
            dbc.Col(html.H3(empty_count[0])),
        ]
    ),
    html.Br(),
    html.Br(),

    html.H2("Empty Data vs Total Number of Data"),
    html.Div(
    [
        dbc.Progress(value=(empty_count[0]/total_data * 100), style={"height": "1px"}, className="mb-3"),
        dbc.Progress(value=(empty_count[0]/total_data * 100), style={"height": "30px"}),
    ]
    ), 
    html.Br(),
    html.Br(),
    html.H2("Total Data Row Count Breakdown"),
    dbc.Row(
        [
            dbc.Col(html.Div("Row Count Profit & Loss: ")),
            dbc.Col(html.Div("Row Count Balance Sheet")),
            dbc.Col(html.Div("Row Count Cash Flow")),
            dbc.Col(html.Div("Row Count Financial Ratio")),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H3(row_count[1])),
            dbc.Col(html.H3(row_count[2])),
            dbc.Col(html.H3(row_count[3])),
            dbc.Col(html.H3(row_count[4])),
        ]
    ),
      html.Br(),
    html.Br(),
]))

if __name__ == "__main__":
    app.run_server(debug=True)
