import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import plotly.figure_factory as ff

import copy
import numpy as np
import pandas as pd

df = pd.read_csv('~/Projects/text-analyze/CSV/all-data-valid-commits.csv')

# 2
classes=np.unique(df['score'].values).tolist()

# 3
class_code={classes[k]: k for k in range(9)}

# 4
color_vals=[class_code[cl] for cl in df['score']]


# 5
pl_colorscale=[[0.0, '#f00'], 
               [0.111, '#f00'],
               [0.222, '#da1717'],
               [0.222, '#da1717'],
               [0.333, '#cc5029'],
               [0.333, '#cc5029'],
               [0.444, '#c56f22'],
               [0.444, '#c56f22'],
               [0.555, '#3f51b5'], # 0
               [0.555, '#3f51b5'], # 0
               [0.666, '#b2ff3b'],
               [0.666, '#b2ff3b'],
               [0.777, '#7de81d'],
               [0.777, '#7de81d'],
               [0.888, '#0dea0b'],
               [0.888, '#0dea0b'],
               [0.999, '#00ff68'],
               [1, '#00ff68']]

# 6
text=[df.loc[k, 'score'] for k in range(len(df))]

# 7
trace1 = go.Splom(dimensions=[dict(label='new',
                                 values=df['new']),
                            dict(label='resolved',
                                 values=df['resolved']),
                            dict(label='unresolved',
                                 values=df['unresolved']),
                            dict(label='insertions',
                                 values=df['insertions'])],
                text=text,
                marker=dict(color=color_vals,
                            size=7,
                            colorscale=pl_colorscale,
                            showscale=False,
                            line=dict(width=0.5,
                                      color='rgb(230,230,230)'))
                )

# 8
axis = dict(showline=True,
          zeroline=False,
          gridcolor='#fff',
          ticklen=4)

layout = go.Layout(
    title='Iris Data set',
    dragmode='select',
    width=600,
    height=600,
    autosize=False,
    hovermode='closest',
    plot_bgcolor='rgba(240,240,240, 0.95)',
    xaxis1=dict(axis),
    xaxis2=dict(axis),
    xaxis3=dict(axis),
    xaxis4=dict(axis),
    yaxis1=dict(axis),
    yaxis2=dict(axis),
    yaxis3=dict(axis),
    yaxis4=dict(axis)
)

fig1 = dict(data=[trace1], layout=layout)
py.plot(fig1, filename='splom-scores')