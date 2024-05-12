import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datetime

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
                    html.H4('Graph', className="card-title"),
                ])
            ], className="mb-10", style={'height': 'calc(30vh - 20px)', 'margin': '10px'})

card_results = dbc.Card([
                dbc.CardBody([
                    html.H4('Results', className="card-title"),
                    html.Div(id='output')
                ])
            ], className="mb-9", style={'height': 'calc(70vh - 20px)', 'margin': '10px', 'margin-left':'20px'})

card_percentages = dbc.Card([
                        dbc.CardBody([
                            html.H4('Percentages', className="card-title"),
                        ])
                    ], style= {'height': 'calc(50vh - 20px)', 'margin': '10px', 'margin-right':'20px'})

card_best_portfolio = dbc.Card([
                        dbc.CardBody([
                            html.H4('Best Portfolio', className="card-title"),
                        ])
                    ], style= {'height': 'calc(20vh - 20px)', 'margin': '10px', 'margin-right':'20px'})

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
    Output('output', 'children'),
    [Input('string-list', 'value'), Input('date-range', 'start_date'), Input('date-range', 'end_date')]
)
def update_output(tickers, start_date, end_date):
    tickers = tickers.split(' ')
    if tickers:
        return f'Tickers: {tickers} Start Date: {start_date} End Date: {end_date}'
    else:
        return ''

if __name__ == '__main__':
    app.run_server()
    
    