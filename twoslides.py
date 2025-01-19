from dash import Dash, html, dcc, Input, Output, State, ALL
import base64


def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# Initialize the Dash app
app = Dash(__name__)

# Sample images and options for slides
slides_data = [
    {"id": "slide1", "image": b64_image("1.jpg"), "label": "Option 1"},
    {"id": "slide2", "image": b64_image("2.jpg"), "label": "Option 2"},
    {"id": "slide3", "image": b64_image("3.jpg"), "label": "Option 3"},
    {"id": "slide4", "image": b64_image("4.jpg"), "label": "Option 4"},
    {"id": "slide5", "image": b64_image("5.jpg"), "label": "Option 5"},
    {"id": "slide6", "image": b64_image("6.jpg"), "label": "Option 6"},
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
     Input("next-button", "n_clicks")],
)
def update_carousel(prev_clicks, next_clicks):
    # Calculate the starting index of the visible slides
    print('here on the way')
    print(f'whhich clik is this prev {prev_clicks} and next {next_clicks}')
    total_slides = len(slides_data)
    start_index = (next_clicks - prev_clicks) % total_slides
    print(f'this is start index {start_index}')
    # Determine the indices of the two slides to display
    first_slide_index = start_index
    second_slide_index = (start_index + 1) % total_slides
    print(f'this is second index {second_slide_index}')
    # Get the corresponding slides
    first_slide = slides_data[first_slide_index]
    second_slide = slides_data[second_slide_index]

    # Render the two slides
    return html.Div([
        html.Div([
            html.Img(src=first_slide["image"], style={"width": "300px", "height": "200px"}),
            dcc.RadioItems(
                options=[{"label": first_slide["label"], "value": first_slide["id"]}],
                value=None,
                id={"type": "radio-slide", "index": first_slide["id"]},
                style={"margin-top": "10px", "text-align": "center"}
            ),
        ], style={"display": "inline-block", "margin": "0 10px"}),

        html.Div([
            html.Img(src=second_slide["image"], style={"width": "300px", "height": "200px"}),
            dcc.RadioItems(
                options=[{"label": second_slide["label"], "value": second_slide["id"]}],
                value=None,
                id={"type": "radio-slide", "index": second_slide["id"]},
                style={"margin-top": "10px", "text-align": "center"},
            ),
        ], style={"display": "inline-block", "margin": "0 10px"}),
    ])

# Callback to capture the selected radio button
@app.callback(
    Output("selected-output", "children"),
    [Input({"type": "radio-slide", "index": ALL}, "value")],
)

def update_selection(selected_values):
    print('this is')
    selected_value = next((value for value in selected_values if value is not None), None)
    return f"You selected: {selected_value}" if selected_value else "No selection made"



if __name__ == "__main__":
    app.run_server(debug=True)
