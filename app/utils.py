import pandas as pd
import yfinance as yf
import plotly.express as px
import numpy as np

def get_data(list_tickers, start_date, end_date):
    df = pd.DataFrame()
    for ticker in list_tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        df[ticker]= data['Adj Close']
    
    return df

def plot_data(df):
    df_plot= df.stack(0).reset_index().rename(columns={'level_1': 'Ticker', 0: 'Price'})
    df_plot= df_plot.sort_values(by=['Ticker', 'Date'], ascending=True)
    fig = px.line(df_plot, x='Date', y='Price', color='Ticker')
    return fig

def format_graph(fig):
    # Remove background color
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # Remove title
    fig.update_layout(
        title=None
    )
    

    # Remove margins
    fig.update_layout(
        autosize=True,
        margin=dict(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0,  # top margin
            pad=0  # padding
        )
    )

    # Change font color to white
    fig.update_layout(
        font=dict(
            color="white"
        )
    )
    
    return fig

def make_simulation(df):
    
    df_adj_close = df
    df_log_return = np.log(df_adj_close/df_adj_close.shift(1))
    
    
    # number of simulation
    n = 5000
    # n = 10

    port_weights = np.zeros(shape=(n,len(df_adj_close.columns)))
    port_volatility = np.zeros(n)
    port_sr = np.zeros(n)
    port_return = np.zeros(n)

    num_securities = len(df_adj_close.columns)
    # num_securities
    for i in range(n):
        # Weight each security
        weights = np.random.random(num_securities)
        # normalize it, so that some is one
        weights /= np.sum(weights)
        port_weights[i,:] = weights 
        #     print(f'Normalized Weights : {weights.flatten()}')

        # Expected return (weighted sum of mean returns). Mult by 252 as we always do annual calculation and year has 252 business days
        exp_ret = df_log_return.mean().dot(weights)*252 
        port_return[i] = exp_ret
    #     print(f'\nExpected return is : {exp_ret[0]}')

        # Exp Volatility (Risk)
        exp_vol = np.sqrt(weights.T.dot(252*df_log_return.cov().dot(weights)))
        port_volatility[i] = exp_vol
    #     print(f'\nVolatility : {exp_vol[0][0]}')

        # Sharpe ratio
        sr = exp_ret / exp_vol
        port_sr[i] = sr
    #     print(f'\nSharpe ratio : {sr[0][0]}')

    df_results= pd.DataFrame({'Return': port_return, 'Volatility': port_volatility, 'Sharpe Ratio': port_sr})

    # Index of max Sharpe Ratio
    max_sr = port_sr.max()
    ind = port_sr.argmax()
    # Return and Volatility at Max SR
    max_sr_ret = port_return[ind]
    max_sr_vol = port_volatility[ind]
    
    fig= px.scatter(df_results, x='Volatility', y='Return', color='Sharpe Ratio', title='Portfolio Optimization')
    #add the max SR point
    fig.add_trace(px.scatter(x=[max_sr_vol], y=[max_sr_ret], color=[max_sr], size=[100]).data[0])
    
    df_percentages_final= pd.DataFrame()
    for weight, stock in zip(port_weights[ind],(df_adj_close.columns)):
        df_percentages_final[stock]= [weight*100]
        
    df_results_final= pd.DataFrame({'Return': [max_sr_ret], 'Volatility': [max_sr_vol], 'Sharpe Ratio': [max_sr]})
    
    df_percentages_final= df_percentages_final.T.reset_index().rename(columns={'index': 'Ticker', 0: 'Weight'})
    
    df_percentages_final.to_csv('df_percentages_final.csv', index=False)
    df_results_final.to_csv('df_results_final.csv', index=False)
    
    print(df_percentages_final)
    print(df_results_final)
    
    return fig

def plot_percentages(df):    
    # Sort the DataFrame
    df = df.sort_values(by='Ticker', ascending=True)
    
    # Get the default color sequence
    colors = px.colors.qualitative.Plotly
    
    # Create a color map based on the sorted 'Ticker' values
    color_map = {ticker: colors[i % len(colors)] for i, ticker in enumerate(df['Ticker'].unique())}
    
    # Create the pie chart
    fig = px.pie(df, values='Weight', names='Ticker', title='Portfolio Composition', color='Ticker', color_discrete_map=color_map)
    
    return fig

def get_best_portfolio(df):
    
    e_ret = df['Return'].values[0]
    e_vol = df['Volatility'].values[0]
    e_sr = df['Sharpe Ratio'].values[0]
    
    results= [e_ret, e_vol, e_sr]
    
    return results