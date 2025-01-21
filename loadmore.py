from dash import Dash, html, Input, Output, State

app = Dash(__name__)

# Sample data: 12 blocks (you can replace with your own data)
blocks = [f"Block {i+1}" for i in range(12)]

app.layout = html.Div([
    html.Div(id='blocks-container', children=[
        html.Div(block, className='block', style={'margin': '10px', 'padding': '10px', 'border': '1px solid black'})
        for block in blocks[:8]  # Initially show the first 8 blocks
    ]),
    html.A("Load More", id='load-more-link', href='#', style={'display': 'block', 'margin': '10px'}),
    html.Div(id='hidden-blocks', children=[
        html.Div(block, className='block', style={'margin': '10px', 'padding': '10px', 'border': '1px solid black'})
        for block in blocks[8:]  # Hidden blocks
    ], style={'display': 'none'})  # Hide initially
])

@app.callback(
    Output('hidden-blocks', 'style'),
    Input('load-more-link', 'n_clicks'),
    State('hidden-blocks', 'style')
)
def show_more(n_clicks, hidden_style):
    if n_clicks is None:
        return hidden_style  # Don't modify if no clicks
    return {'display': 'block'}  # Reveal hidden blocks on click

if __name__ == '__main__':
    app.run_server(debug=True)
