import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import base64

# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# Define the slides data
slides = [
    {"id": 1, "image": b64_image('1.jpg'), "label": "Option 1"},
    {"id": 2, "image": b64_image('2.jpg'), "label": "Option 2"},
    {"id": 3, "image": b64_image('3.jpg'), "label": "Option 3"},
    {"id": 4, "image": b64_image('4.jpg'), "label": "Option 4"},
    {"id": 5, "image": b64_image('5.jpg'), "label": "Option 5"},
    {"id": 6, "image": b64_image('6.jpg'), "label": "Option 6"},
]

# Define the app layout
app.layout = dbc.Container(
    [
        html.H1("Carousel Showing Two Items", className="text-center my-4"),
        dcc.Store(id="carousel-index", data=0),  # Store for tracking the start index
        # Carousel container
        html.Div(
            id="carousel-container",
            children=[
                html.Div(
                    id="carousel-items",
                    style={"display": "flex", "justifyContent": "center", "gap": "20px"},
                )
            ],
        ),
        # Navigation buttons
        html.Div(
            [
                dbc.Button("Previous", id="prev-btn", className="btn-secondary mx-2"),
                dbc.Button("Next", id="next-btn", className="btn-primary mx-2"),
            ],
            className="text-center my-4",
        ),
        # Output for selected option
        html.Div(id="selected-output", className="text-center my-4"),
        # Submit button
        dbc.Button("Submit", id="submit-btn", className="btn-success my-2"),
        html.Div(id="form-output", className="text-center my-4"),
    ],
    fluid=True,
)

# Callback to manage the visible slides
@app.callback(
    Output("carousel-items", "children"),
    Output("carousel-index", "data"),
    [Input("prev-btn", "n_clicks"), Input("next-btn", "n_clicks")],
    State("carousel-index", "data"),
)
def update_carousel(prev_clicks, next_clicks, start):
    # Update the start index based on navigation
    print('this is ctx triggered')
    print(ctx.triggered)
    if not ctx.triggered:
        start = 0
    else:
        print('in the else')
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "next-btn":
            start = min(start + 2, len(slides) - 2)
        elif button_id == "prev-btn":
            start = max(start - 2, 0)

    # Create the visible items
    visible_slides = slides[start : start + 2]
    print(f'visibale slides {visible_slides}')
    items = [
        html.Div(
            [
                html.Img(src=slide["image"], style={"width": "100px", "height": "100px"}),
                dcc.RadioItems(
                    id=f"radio-{slide['id']}",
                    options=[{"label": slide["label"], "value": slide["id"]}],
                    value=None,
                    labelStyle={"marginTop": "10px", "display": "block"},
                ),
            ],
            style={"textAlign": "center"},
        )
        for slide in visible_slides
    ]
    print(f'this is items {items} and start {start}')
    return items, start


# Callback to capture the selected radio button values
@app.callback(
    Output("selected-output", "children"),
    [Input(f"radio-{slide['id']}", "value") for slide in slides],
)
def display_selected(*selected_values):
    selected = [f"Slide {i + 1}: {val}" for i, val in enumerate(selected_values) if val]
    print(selected)
    return html.Div([html.P(s) for s in selected]) if selected else "No selection yet."


# # Callback for submit button
# @app.callback(
#     Output("form-output", "children"),
#     Input("submit-btn", "n_clicks"),
#     [State(f"radio-{slide['id']}", "value") for slide in slides],
# )
# def handle_submit(n_clicks, *selected_values):
#     if not n_clicks:
#         return ""
#     selections = [f"Slide {i + 1}: {val}" for i, val in enumerate(selected_values) if val]
#     if not selections:
#         return "Please make at least one selection before submitting!"
#     return f"Submitted selections: {', '.join(selections)}"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
