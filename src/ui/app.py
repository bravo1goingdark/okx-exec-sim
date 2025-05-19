# app.py
import dash, dash_core_components as dcc, dash_html_components as html
from dash.dependencies import Input, Output
import asyncio
import threading

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([  # Left panel
        html.Label("Spot Asset"),
        dcc.Dropdown(id='asset', options=[{'label': 'BTC-USDT-SWAP','value':'BTC-USDT-SWAP'}]),
        html.Label("Quantity (USD)"),
        dcc.Input(id='qty', type='number', value=100),
        html.Button('Start', id='start-btn')
    ], style={'width':'30%','display':'inline-block'}),
    html.Div([  # Right panel
        html.Div(id='slippage-output'),
        html.Div(id='fees-output'),
        html.Div(id='impact-output'),
        html.Div(id='net-cost-output'),
        html.Div(id='mt-prop-output'),
        html.Div(id='latency-output')
    ], style={'width':'65%','display':'inline-block','verticalAlign':'top'})
])

@app.callback(
    [Output('slippage-output','children'),
     Output('fees-output','children'),
     Output('impact-output','children'),
     Output('net-cost-output','children'),
     Output('mt-prop-output','children'),
     Output('latency-output','children')],
    [Input('start-btn','n_clicks')],
    [dash.dependencies.State('asset','value'),
     dash.dependencies.State('qty','value')]
)
def update_outputs(n_clicks, asset, qty):
    # Pull latest from a shared state (thread queue)
    # Run models, return formatted strings
    # e.g. f"Expected Slippage: {slippage:.4f} USD"
    pass

def run_dash():
    app.run_server(debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start Dash in a thread so asyncio loop can run concurrently
    threading.Thread(target=run_dash, daemon=True).start()
    asyncio.run(main_event_loop())
