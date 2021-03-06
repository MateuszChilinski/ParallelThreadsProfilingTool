import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math
import uuid


class Main():
    def __init__(self):
        self.kernels = []
        self.labels = []
        self.x = []
        self.y = []
        self.text = []
        self.kernels_lines = []

    def set_data(self, data):
        self.kernels = data[data.x == -1]
        internal_data = data[data.x != -1]
        self.labels = internal_data.label.unique()

        self.x.clear()
        self.y.clear()
        self.text.clear()

        for label in self.labels:
            time = internal_data[internal_data['label'] == label]['time']
            self.x.append(time)

            x_id = internal_data[internal_data['label'] == label]['x']
            self.y.append(x_id)

            text = internal_data[internal_data['label'] == label]['label']
            self.text.append(text)

        self.__generate_kernel_lines()

    def __generate_kernel_lines(self):
        self.kernels_lines.clear()

        for _, row in self.kernels.iterrows():
            time = row['time']
            if "start_" in row['label']:
                color = 'rgb(50, 171, 96)'
            else:
                color = 'rgb(220, 20, 60)'

            self.kernels_lines.append({
                'type': 'line',
                'yref': 'paper',
                'x0': time,
                'x1': time,
                'y0': 0,
                'y1': 1,
                'line': {
                        'color':color,
                        'width': 4,
                        'dash': 'dashdot',
                },
            })

    def get_content(self):
        layout = dcc.Graph(
            id='main_graph' + str(uuid.uuid4()),
            style={"height": "78vh"},
            config={"scrollZoom": True},
            figure={
                'data': [
                    go.Scattergl(
                        x=self.x[index],
                        y=self.y[index],
                        text=self.text[index],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=label,
                        hoverinfo='x+y+z+text'
                    ) for index, label in enumerate(self.labels)
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'X-id'},
                    shapes=self.kernels_lines,
                    showlegend=True,
                    hovermode='closest',
                    font=dict(family='Courier New, monospace', size=16, color='#7f7f7f')
                )
            })
        return layout
