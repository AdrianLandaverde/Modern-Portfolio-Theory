import dash
from dash import dcc
from dash import html
from dash import State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datetime
from utils import *
import time
import os

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

card_input= dbc.Card([
                dbc.CardBody([
                    html.H4('Portfolio Optimization', className="card-title"),
                    
                    html.Label('Select the Dates of the data', className="form-label"),
                    
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text="End Period",
                        display_format='YYYY-MM-DD',
                        max_date_allowed= datetime.datetime.now().date(),
                        style={'width': '100%', 'color': '#FFFFFF'},
                    ),

                    html.Label('Select the Tickers', className="form-label"),
                    
                    dcc.Textarea(
                        id='string-list',
                        placeholder='Write Tickers with space between them: AAPL MSFT GOOGL',
                        style={'width': '100%', 'height': '50%'}
                    ),
                    
                    dbc.Button('Optimize', color='primary', className='mt-2', id='optimize-button',
                                style={'width': '100%', 'border-radius': '10px', 'margin-top': '10px'})
                ])
            ], className="mb-2", style={'height': 'calc(100vh - 20px)', 'margin': '10px',})

card_graph = dbc.Card([
                dbc.CardBody([
                    
                    dcc.Loading( id="loading-output", children=[html.Div(dcc.Graph(id='graph_close', style={'height': 'calc(30vh - 20px)', 'width': '100%'}))], 
                                type="graph", style={'height': 'calc(30vh - 20px)', 'width': '100%', 'z-index': '1000'}),
                    
                ], style= {'margin': '0px', 'padding': '0px', 'height': 'calc(30vh - 20px)', 'width': '100%'})
            ], className="mb-10", style={'height': 'calc(30vh - 20px)', 'margin': '10px'})

card_results = dbc.Card([
                dbc.CardBody([
                    
                    dcc.Loading( id="loading-output2", children=[html.Div(dcc.Graph(id='graph_simulation', style={'height': 'calc(70vh - 20px)', 'width': '100%'}))],
                                type="graph", style={'height': 'calc(70vh - 20px)', 'width': '100%', 'z-index': '1000'})
                ], style= {'margin': '0px', 'padding': '0px', 'height': 'calc(70vh - 20px)', 'width': '100%'})
            ], className="mb-9", style={'height': 'calc(70vh - 20px)', 'margin': '10px', 'margin-left':'20px'})

card_percentages = dbc.Card([
                        dbc.CardBody([
                            dcc.Loading( id="loading-output3", children=[html.Div(dcc.Graph(id='graph_percentages', style={'height': 'calc(45vh - 20px)', 'width': '100%'}))],
                                type="graph", style={'height': 'calc(45vh - 20px)', 'width': '100%', 'z-index': '1000'})
                        ], style= {'margin': '0px', 'padding': '0px', 'height': 'calc(45vh - 20px)', 'width': '100%'})
                    ], style= {'height': 'calc(45vh - 20px)', 'margin': '10px', 'margin-right':'20px'})

card_best_portfolio = dbc.Card([
                        dbc.CardBody([
                            
                            dcc.Loading( id="loading-output4", children=[html.Div(id='best-portfolio', style={'height': 'calc(25vh - 20px)', 'width': '100%'})],
                                type="default", style={'height': 'calc(25vh - 20px)', 'width': '100%', 'z-index': '1000'})
                        ])
                    ], style= {'height': 'calc(25vh - 20px)', 'margin': '10px', 'margin-right':'20px'})

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            card_input
        ], md=2, style={'margin': '0px', 'padding': '0px'}),
        
        dbc.Col([
            card_graph,
            
            dbc.Row([
                dbc.Col([
                    card_results
                ], md=9, style={ 'margin': '0px', 'padding': '0px'}),
                
                dbc.Col([
                    card_percentages,
                    card_best_portfolio
                ], md=3, style={ 'margin': '0px', 'padding': '0px'})
            ])
            
        ], md=10, style={'margin': '0px', 'padding': '0x'} )
    ]),
    
], fluid=True)

@app.callback(
    Output('graph_close', 'figure'),
    [Input('optimize-button', 'n_clicks')], 
    [State('string-list', 'value'), 
    State('date-range', 'start_date'), State('date-range', 'end_date')]
)
def update_output(n_clicks, tickers, start_date, end_date):
    
    if n_clicks is not None: 
        try:
            os.remove("data.csv")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
            
        try:
            os.remove("df_percentages_final.csv")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
            
        try:
            os.remove("df_results_final.csv")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
        
        df= get_data(tickers.split(), start_date, end_date)
        
        df.to_csv('data.csv', index=False)
        
        fig= plot_data(df)
        
        fig= format_graph(fig)
        fig.update_xaxes(title_text="", title_standoff=0)
        
        return fig
    return ''

@app.callback(
    Output('graph_simulation', 'figure'),
    [Input('optimize-button', 'n_clicks')], 
    [State('string-list', 'value'), 
    State('date-range', 'start_date'), State('date-range', 'end_date')]
)
def update_output2(n_clicks, tickers, start_date, end_date):
    
    time.sleep(2)
    
    if n_clicks is not None:    
        
        while not os.path.exists("data.csv"):
            time.sleep(1)
        
        df= pd.read_csv('data.csv')
        
        fig= make_simulation(df)
        
        fig= format_graph(fig)
        
        return fig
    return ''
    
    
@app.callback(
    Output('graph_percentages', 'figure'),
    [Input('optimize-button', 'n_clicks')], 
    [State('string-list', 'value'), 
    State('date-range', 'start_date'), State('date-range', 'end_date')]
)
def update_output3(n_clicks, tickers, start_date, end_date):
    
    time.sleep(2)
    
    
    if n_clicks is not None:    
        
        while not os.path.exists("df_percentages_final.csv"):
            time.sleep(1)
            
        df= pd.read_csv('df_percentages_final.csv')
        
        fig= plot_percentages(df)
        
        fig = format_graph(fig)
        fig.update_layout(showlegend=False)
        
    
        return fig
    return ''

@app.callback(
    Output('best-portfolio', 'children'),
    [Input('optimize-button', 'n_clicks')], 
    [State('string-list', 'value'), 
    State('date-range', 'start_date'), State('date-range', 'end_date')]
)
def update_output4(n_clicks, tickers, start_date, end_date):
    
    time.sleep(2)
    
    
    if n_clicks is not None:    
        
        while not os.path.exists("df_results_final.csv"):
            time.sleep(1)
            
        df= pd.read_csv('df_results_final.csv')
        
        results= get_best_portfolio(df)
        
        format_results= html.Div([html.P(f"Return: {format(results[0], '.2f')}"), 
                    html.P(f"Volatility: {format(results[1], '.2f')}"), 
                    html.P(f"Sharpe Ratio: {format(results[2], '.2f')}")])
        
    
        return format_results
    return ''
    

if __name__ == '__main__':
    app.run_server()
    
    