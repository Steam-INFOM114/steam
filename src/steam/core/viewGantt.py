from django.shortcuts import render
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
from .models import Task, Meeting
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

# Generate data and return the Gantt chart
def generate_data():
    #data gathering
    df = pd.DataFrame(list(Task.objects.all().values()))

    df2 = pd.DataFrame(list(Meeting.objects.all().values()))
    df2 = df2.reset_index()
    for i, row in df2.iterrows():
        df2.at[i,'end_date'] = row.start_date + pd.Timedelta(days=1)

    df = pd.concat([df,df2])

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
    global fig
    fig = px.timeline(df, x_start="start_date", x_end="end_date", y="name", color="status", color_discrete_map={'1': '#3CDBEA','2': '#FD8A17', '3': '#63D233'}, hover_name="name",
                             hover_data={'name':False,
                                         'status':False
                            })

    fig.for_each_trace(
        lambda trace: trace.update(visible=True,marker=dict(opacity=[1,0.5,0.5,0.5,0,0,0,0])) if trace.name == '1' else (),
    )

    fig.for_each_trace(
        lambda trace: print(trace)
    )

    #fig.update_traces(marker=dict(opacity=[1,0.5,0.5,0.5,0,0,0,0]))

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(clickmode='event+select', height=700, margin={'l': 0, 'b': 0, 'r': 0, 't': 30},yaxis_title=None,legend_title="")
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    newnames = {'1':'À commencer', '2': 'En cours', '3': 'Terminé', 'Réunion': 'Réunion'}
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

    return fig

# Update Gantt chart according to some event
@app.callback(
    Output('graph', 'figure'),
    [Input('delete-item-output', 'children')]
)
def update_gantt(_):
    return generate_data()

# Display the information of the selected item
@app.callback(
    Output('click-data', 'children'),
    Input('graph', 'clickData'))
def display_click_data(clickData):
    if clickData is None:
        return ''

    df = pd.DataFrame(list(Task.objects.all().values()))
    x = df.loc[df['name'] == clickData['points'][0]['y']]
    if x.empty:
        df = pd.DataFrame(list(Meeting.objects.all().values()))
        x = df.loc[df['name'] == clickData['points'][0]['y']]
        text = "Nom: " + x.name + "\n"
        text = text + "Description: " + x.description + "\n"
        text = text + "Date de la réunion: " + x.astype(str).tail(1).reset_index().loc[0, 'start_date'] + "\n"
    else:
        text = "Nom: " + x.name + "\n"
        text = text + "Description: " + x.description + "\n"
        text = text + "Date de départ: " + x.astype(str).tail(1).reset_index().loc[0, 'start_date'] + "\n"
        text = text + "Date de fin: " + x.astype(str).tail(1).reset_index().loc[0, 'end_date'] + "\n"
    print(fig)
    fig.for_each_trace(
        lambda trace: trace.update(visible=False)
    )
    return text

# Delete the selected item when the delete button is clicked
@app.callback(
    Output('delete-item-output', 'children'),
    [Input('delete-item-button', 'n_clicks')],
    [State('graph', 'clickData')])
def delete_task_meeting(n_clicks, clickData):
    # TODO : delete according to id
    if n_clicks is not None and clickData is not None:
        name = clickData['points'][0]['y']
        task = Task.objects.filter(name=name)
        if task:
            task.delete()
        else:
            meeting = Meeting.objects.filter(name=name)
            meeting.delete()

# TODO : update the task or meeting when the update button is clicked
def update_task_meeting(clickData):
    pass

# Create the layout of the page
app.layout = html.Div([
    dcc.Graph(
        id='graph',
        figure=generate_data(),
        config=config
    ),

    html.Div([
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns'),

    # Add delete button
    html.Div([
        html.Button("Supprimer", id="delete-item-button") ,
        html.Div(id='delete-item-output')
    ]),

])

# View to display the gantt chart
def gantt(request):
    return render(request, 'tasks/tasks.html', {'my_app': app, 'tasks': Task.objects.all().values(), 'meetings': Meeting.objects.all().values()})
