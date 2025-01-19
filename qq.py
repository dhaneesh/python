from dash import Dash, html, dcc, Input, Output, State, ALL

# Initialize the Dash app
app = Dash(__name__)

# Sample images and options for slides
slides_data = [
    {"id": "slide1", "image": "https://via.placeholder.com/300x200?text=Slide+1", "label": "Option 1"},
    {"id": "slide2", "image": "https://via.placeholder.com/300x200?text=Slide+2", "label": "Option 2"},
    {"id": "slide3", "image": "https://via.placeholder.com/300x200?text=Slide+3", "label": "Option 3"},
    {"id": "slide4", "image": "https://via.placeholder.com/300x200?text=Slide+4", "label": "Option 4"},
]

# Layout
app.layout = html.Div([
    html.H2("Custom Carousel with Radio Buttons (2 Slides at a Time)"),
    
    # Carousel container
    html.Div([
        html.Button("Previous", id="prev-button", n_clicks=0),
        html.Div(id="carousel-slides", style={"display": "inline-block", "margin": "0 20px", "text-align": "center"}),
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
    Output("carousel-slides", "children"),
    [Input("prev-button", "n_clicks"),
     Input("next-button", "n_clicks"),
     Input({"type": "radio-slide", "index": ALL}, "value")],
)
def update_carousel(prev_clicks, next_clicks, selected_values):
    # Calculate the starting index of the visible slides
    total_slides = len(slides_data)
    start_index = (next_clicks - prev_clicks) % total_slides
    # Determine the indices of the two slides to display
    first_slide_index = start_index
    second_slide_index = (start_index + 1) % total_slides
    
    # Get the corresponding slides
    first_slide = slides_data[first_slide_index]
    second_slide = slides_data[second_slide_index]

    # Determine which slide has been selected, if any
    selected_value = next((value for value in selected_values if value is not None), None)
    
    # Determine whether to disable the other radio item
    disable_first = (selected_value is not None and selected_value != first_slide["id"])
    disable_second = (selected_value is not None and selected_value != second_slide["id"])

    # Create options
    first_options = [{"label": first_slide["label"], "value": first_slide["id"]}]
    second_options = [{"label": second_slide["label"], "value": second_slide["id"]}]

    # Adjust the options based on selection
    if disable_first:
        first_options = [{"label": first_slide["label"], "value": first_slide["id"], "disabled": True}]
    if disable_second:
        second_options = [{"label": second_slide["label"], "value": second_slide["id"], "disabled": True}]
        
    # Render the two slides with updated disabled state
    return html.Div([
        html.Div([
            html.Img(src=first_slide["image"], style={"width": "300px", "height": "200px"}),
            dcc.RadioItems(
                options=first_options,
                value=None,
                id={"type": "radio-slide", "index": first_slide["id"]},
                style={"margin-top": "10px", "text-align": "center"}
            ),
        ], style={"display": "inline-block", "margin": "0 10px"}),

        html.Div([
            html.Img(src=second_slide["image"], style={"width": "300px", "height": "200px"}),
            dcc.RadioItems(
                options=second_options,
                value=None,
                id={"type": "radio-slide", "index": second_slide["id"]},
                style={"margin-top": "10px", "text-align": "center"}
            ),
        ], style={"display": "inline-block", "margin": "0 10px"}),
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
