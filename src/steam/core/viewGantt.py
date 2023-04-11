from django.shortcuts import render
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from .models import Task
from django.utils import timezone
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample')   # replaces dash.Dash

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

config = {'displaylogo': False,
          'modeBarButtonsToRemove': ['lasso2d','select2d','autoScale']
          }

currentId = {'Id': 0}

def update_gantt():
    #data gathering
    df = pd.DataFrame(list(Task.objects.all().values()))
    if not (df.empty):
        df.sort_values(by='end_date', inplace = True)
        df.sort_values(by='start_date', inplace = True)
        df.sort_values(by='status', inplace = True)
    else:
        df['name'] = ''
        df['start_date'] = ''
        df['end_date'] = ''
        df['status'] = ''

    #create gantt figure
    fig = px.timeline(df, x_start="start_date", x_end="end_date", y="name", color="status",color_discrete_map={'1': '#3CDBEA','2': '#FD8A17', '3': '#63D233'}, hover_name="name",
                             hover_data={'name':False,
                                         'status':False
                            })

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(clickmode='event+select', height=700, margin={'l': 0, 'b': 0, 'r': 0, 't': 30},yaxis_title=None,legend_title="")
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    newnames = {'1':'À commencer', '2': 'En cours', '3': 'Terminé'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )

    fig.update_traces(marker_line_color='rgb(0,48,107)', marker_line_width=1, opacity=1)

    #Draw line for the current day
    fig.update_layout(shapes=[
        dict(
        type='line',
        yref='paper', y0=0, y1=1,
        xref='x', x0=timezone.now().date(), x1=timezone.now().date()
        )
    ])

    app.layout = html.Div([
        dcc.Graph(
            id='basic-interactions',
            figure=fig,
            config=config
        ),
        dcc.Store(id='currentId'),

        html.Div([
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),
    ])

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    df = pd.DataFrame(list(Task.objects.all().values()))
    x = df.loc[df['name'] == clickData['points'][0]['y']]
    text = "Nom: " + x.name + "\n"
    text = text + "Description: " + x.description + "\n"
    text = text + "Date de départ: " + x.astype(str).tail(1).reset_index().loc[0, 'start_date'] + "\n"
    text = text + "Date de fin: " + x.astype(str).tail(1).reset_index().loc[0, 'end_date'] + "\n"
    currentId['Id'] = x.id
    return text

def gantt(request):
    update_gantt()
    return render(request, 'tasks/tasks.html', {'my_app': app, 'tasks': Task.objects.all().values(), 'selected': currentId['Id']})
