from dash import Dash, html, dcc, Input, Output, State, ALL

# Initialize the Dash app
app = Dash(__name__)

# Sample images and options for slides
slides_data = [
    {"id": "slide1", "image": "https://via.placeholder.com/300x200?text=Slide+1", "label": "Option 1"},
    {"id": "slide2", "image": "https://via.placeholder.com/300x200?text=Slide+2", "label": "Option 2"},
    {"id": "slide3", "image": "https://via.placeholder.com/300x200?text=Slide+3", "label": "Option 3"},
]

# Layout
app.layout = html.Div([
    html.H2("Custom Carousel with Radio Buttons"),
    
    # Carousel container
    html.Div([
        html.Button("Previous", id="prev-button", n_clicks=0),
        html.Div(id="carousel-slide", style={"display": "inline-block", "margin": "0 20px"}),
        html.Button("Next", id="next-button", n_clicks=0),
    ], style={"text-align": "center", "margin-bottom": "20px"}),

    # Output for selected option
    html.Div([
        html.H4("Selected Option:"),
        html.Div(id="selected-output", style={"font-weight": "bold"})
    ]),
])

# Callback to update the carousel
@app.callback(
    Output("carousel-slide", "children"),
    [Input("prev-button", "n_clicks"),
     Input("next-button", "n_clicks")],
    State("carousel-slide", "children"),
)
def update_carousel(prev_clicks, next_clicks, current_content):
    # Calculate the index of the current slide
    slide_index = (next_clicks - prev_clicks) % len(slides_data)
    slide = slides_data[slide_index]
    
    # Return the current slide with radio buttons
    return html.Div([
        html.Img(src=slide["image"], style={"width": "300px", "height": "200px"}),
        dcc.RadioItems(
            options=[{"label": slide["label"], "value": slide["id"]}],
            value=None,
            id={"type": "radio-slide", "index": slide["id"]},
            style={"margin-top": "10px", "text-align": "center"}
        )
    ])

# Callback to capture the selected radio button
@app.callback(
    Output("selected-output", "children"),
    [Input({"type": "radio-slide", "index": ALL}, "value")],
)
def update_selection(selected_values):
    selected_value = next((value for value in selected_values if value is not None), None)
    return f"You selected: {selected_value}" if selected_value else "No selection made"

if __name__ == "__main__":
    app.run_server(debug=True)
