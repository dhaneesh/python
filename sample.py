import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from PIL import Image
import base64

image_path = 'assets/my-image.png'

# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')



app = dash.Dash(
    external_stylesheets=[dbc.themes.SANDSTONE],
    suppress_callback_exceptions=True
)
app.layout = dbc.Container(
    dbc.Carousel(
        items=[
            {"key": "1", "src": b64_image('1.jpg')},
            {"key": "2", "src": b64_image('2.jpg')},
            {"key": "3", "src": b64_image('3.jpg')},
            {"key": "4", "src": b64_image('4.jpg')},
            {"key": "5", "src": b64_image('5.jpg')},
            {"key": "6", "src": b64_image('6.jpg')},
        ],
        controls=False,
        indicators=False,
        interval=2000,
        ride="carousel",
)
)

if __name__ == '__main__':
    app.run_server()