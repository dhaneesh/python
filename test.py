from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import base64

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    html.Div([
        html.Div(id='carousel-track', className='carousel-track', style={'display': 'flex', 'transition': 'transform 0.5s ease-in-out', 'transform': 'translateX(0px)'}, children=[
            html.Div(className='carousel-slide', style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center', 'min-width': '50%'}, children=[
                html.Div(className='item', children=[
                    dcc.RadioItems(
                        id='group-1',
                        options=[
                            {'label': html.Img(src=b64_image('1.jpg'), style={'width': '200px', 'height': '200px', 'borderRadius': '8px', 'margin': '0 auto'}), 'value': '1'},
                            {'label': html.Img(src=b64_image('2.jpg'), style={'width': '200px', 'height': '200px', 'borderRadius': '8px', 'margin': '0 auto'}), 'value': '2'},
                            {'label': html.Img(src=b64_image('3.jpg'), style={'width': '200px', 'height': '200px', 'borderRadius': '8px', 'margin': '0 auto'}), 'value': '3'},
                            {'label': html.Img(src=b64_image('4.jpg'), style={'width': '200px', 'height': '200px', 'borderRadius': '8px', 'margin': '0 auto'}), 'value': '4'},
                            {'label': html.Img(src=b64_image('5.jpg'), style={'width': '200px', 'height': '200px', 'borderRadius': '8px', 'margin': '0 auto'}), 'value': '5'},
                            {'label': html.Img(src=b64_image('6.jpg'), style={'width': '200px', 'height': '200px', 'borderRadius': '8px', 'margin': '0 auto'}), 'value': '6'},
                        ],
                        labelStyle={'display': 'inline-block'},
                        value='1'  # Default selected value
                    )
                ])
            ])
        ])
    ], className='carousel', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'overflow': 'hidden', 'width': 'auto', 'margin': 'auto', 'borderRadius': '8px'}),

    # Display current slide number
    html.Div(id='slide-number', style={'textAlign': 'center', 'margin': '10px', 'fontSize': '18px'}),

    # Display selected value under the carousel
    html.Div(id='selected-value', style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '10px'}),

    html.Div([
        dbc.Button("Previous", id="prev-button", disabled=True, style={'marginRight': '10px'}),
        dbc.Button("Next", id="next-button")
    ], className='carousel-controls', style={'display': 'flex', 'justify-content': 'space-between', 'width': '80%', 'margin': '20px auto'})
])

# Callback to handle the previous and next buttons
@app.callback(
    [Output('carousel-track', 'style'),
     Output('prev-button', 'disabled'),
     Output('next-button', 'disabled'),
     Output('group-1', 'value'),
     Output('slide-number', 'children'),
     Output('selected-value', 'children')],
    [Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks'),
     Input('group-1', 'value')],  # Listen to the radio button value changes
    [State('carousel-track', 'style')]
)
def update_carousel(prev_clicks, next_clicks, selected_value, current_style):
    # Track the current position using a variable that will store the index of the carousel
    if prev_clicks is None: prev_clicks = 0
    if next_clicks is None: next_clicks = 0
    
    num_items = 6  # Total number of items
    slides_width = 50  # Width of each slide in percentage (showing 2 items at once)
    max_offset = (num_items - 2) * slides_width  # Maximum offset for the last slide (2 items visible at once)
    current_offset = int(current_style.get('transform', 'translateX(0px)').split('(')[-1].split('px')[0])

    # Calculate the offset for the next and previous button clicks
    if next_clicks > prev_clicks:
        new_offset = current_offset - slides_width
    elif prev_clicks > next_clicks:
        new_offset = current_offset + slides_width
    else:
        new_offset = current_offset

    # Set limits for scrolling
    if new_offset > 0:
        new_offset = 0
    if new_offset < -max_offset:
        new_offset = -max_offset

    # Enable or disable buttons based on the position
    prev_disabled = new_offset == 0
    next_disabled = new_offset == -max_offset

    # Update the carousel track style
    updated_style = {
        'display': 'flex',
        'transition': 'transform 0.5s ease-in-out',
        'transform': f'translateX({new_offset}px)'
    }

    # Calculate the current slide number
    current_slide = int(-new_offset / slides_width) + 1
    slide_number = f"Slide {current_slide} of {num_items}"

    # Update the selected radio item value based on the offset
    current_item_value = str(current_slide)

    # Display selected value under the carousel
    selected_value_text = f"Selected Item: {selected_value}"

    return updated_style, prev_disabled, next_disabled, current_item_value, slide_number, selected_value_text


if __name__ == '__main__':
    app.run_server(debug=True)
