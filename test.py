from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    html.Div([
        html.Div(id='carousel-track', className='carousel-track', style={'display': 'flex', 'transition': 'transform 0.5s ease-in-out', 'transform': 'translateX(0px)'}, children=[
            html.Div(className='carousel-slide', style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center', 'min-width': '100%'}, children=[
                html.Div(className='item', children=[
                    html.Label([
                        html.Input(type='radio', name='group-1', value='1', style={'cursor': 'pointer'}),
                        html.Img(src='1.jpg', alt='Item 1', style={'width': '100px', 'height': '100px', 'borderRadius': '8px', 'margin': '0 auto'})
                    ])
                ]),
                html.Div(className='item', children=[
                    html.Label([
                        html.Input(type='radio', name='group-1', value='2', style={'cursor': 'pointer'}),
                        html.Img(src='2.jpg', alt='Item 2', style={'width': '100px', 'height': '100px', 'borderRadius': '8px', 'margin': '0 auto'})
                    ])
                ])
            ]),
            html.Div(className='carousel-slide', style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center', 'min-width': '100%'}, children=[
                html.Div(className='item', children=[
                    html.Label([
                        html.Input(type='radio', name='group-2', value='3', style={'cursor': 'pointer'}),
                        html.Img(src='3.jpg', alt='Item 3', style={'width': '100px', 'height': '100px', 'borderRadius': '8px', 'margin': '0 auto'})
                    ])
                ]),
                html.Div(className='item', children=[
                    html.Label([
                        html.Input(type='radio', name='group-2', value='4', style={'cursor': 'pointer'}),
                        html.Img(src='4.jpg', alt='Item 4', style={'width': '100px', 'height': '100px', 'borderRadius': '8px', 'margin': '0 auto'})
                    ])
                ])
            ]),
            html.Div(className='carousel-slide', style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center', 'min-width': '100%'}, children=[
                html.Div(className='item', children=[
                    html.Label([
                        html.Input(type='radio', name='group-3', value='5', style={'cursor': 'pointer'}),
                        html.Img(src='5.jpg', alt='Item 5', style={'width': '100px', 'height': '100px', 'borderRadius': '8px', 'margin': '0 auto'})
                    ])
                ]),
                html.Div(className='item', children=[
                    html.Label([
                        html.Input(type='radio', name='group-3', value='6', style={'cursor': 'pointer'}),
                        html.Img(src='6.jpg', alt='Item 6', style={'width': '100px', 'height': '100px', 'borderRadius': '8px', 'margin': '0 auto'})
                    ])
                ])
            ])
        ])
    ], className='carousel', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'overflow': 'hidden', 'width': '60%', 'margin': 'auto', 'border': '2px solid #ccc', 'borderRadius': '8px'}),

    html.Div([
        dbc.Button("Previous", id="prev-button", disabled=True, style={'marginRight': '10px'}),
        dbc.Button("Next", id="next-button")
    ], className='carousel-controls', style={'display': 'flex', 'justify-content': 'space-between', 'width': '80%', 'margin': '20px auto'})
])

# Callback to handle navigation
@app.callback(
    [Output('carousel-track', 'style'),
     Output('prev-button', 'disabled'),
     Output('next-button', 'disabled')],
    [Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('carousel-track', 'style')]
)
def update_carousel(prev_clicks, next_clicks, style):
    if prev_clicks is None:
        prev_clicks = 0
    if next_clicks is None:
        next_clicks = 0

    slide_width = 600  # Adjust to match the actual slide width in pixels
    current_transform = float(style.get('transform', 'translateX(0px)').replace('translateX(', '').replace('px)', ''))
    total_slides = 3
    current_index = int(-current_transform / slide_width)

    if next_clicks > prev_clicks and current_index < total_slides - 1:
        current_index += 1
    elif prev_clicks > next_clicks and current_index > 0:
        current_index -= 1

    transform = -current_index * slide_width
    return {'display': 'flex', 'transition': 'transform 0.5s ease-in-out', 'transform': f'translateX({transform}px)'}, current_index == 0, current_index == total_slides - 1

if __name__ == '__main__':
    app.run_server(debug=True)
