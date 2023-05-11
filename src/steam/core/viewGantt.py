from django.shortcuts import render, get_object_or_404, redirect
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from textwrap import wrap
from .models import Task, Meeting, Project
from django.utils import timezone
from datetime import datetime
from django_plotly_dash import DjangoDash
import numpy as np

app = DjangoDash('SteamGantt',external_stylesheets=[dbc.themes.BOOTSTRAP])   # replaces dash.Dash

styles = {
    'pre': {
        'overflowX': 'scroll',
        'margin-top': '10px',
    }
}

config = {'displaylogo': False,
          'modeBarButtonsToRemove': ['lasso2d','select2d','autoScale']
          }

# Generate data and return the Gantt chart
def generate_data(id):
    #data gathering

    #df = pd.DataFrame()
    df = pd.DataFrame(list(Task.objects.filter(project_id=id).values()))

    #df2 = pd.DataFrame()
    df2 = pd.DataFrame(list(Meeting.objects.filter(project_id=id).values()))

    df2 = df2.reset_index()
    for i, row in df2.iterrows():
        df2.at[i,'end_date'] = row.start_date + pd.Timedelta(days=1)

    df = pd.concat([df,df2])

    if not (df.empty):
        df.sort_values(by='end_date', inplace = True)
        df.sort_values(by='start_date', inplace = True)
        df.sort_values(by='status', inplace = True)
        df['id'] = df['id'].astype(str)
    else:
        df['name'] = ''
        df['start_date'] = ''
        df['end_date'] = ''
        df['status'] = ''
        df['id'] = ''
    df['index'] = np.arange(len(df))

    #create gantt figure
    global fig
    fig = px.timeline(df,
                        x_start="start_date",
                        x_end="end_date",
                        color="status",
                        y="index",
                        color_discrete_map={'1': '#3CDBEA','2': '#FD8A17', '3': '#63D233'},
                        hover_name="name",
                        hover_data={'name':False,'status':False,'id':False,'index':False},
                        text='name',
                      )

    fig.update_yaxes(autorange="reversed",visible=False)
    fig.update_layout(clickmode='event+select', height=700, margin={'l': 0, 'b': 0, 'r': 0, 't': 30},legend_title="")

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
    Input('item-output', 'children'),
    Input('task-form-output', 'children'),
    Input('meeting-form-output', 'children'),
    State('click-data', 'children'),
    State('graph', 'clickData'),
    State('id','value'))
def update_gantt(*args,**kwargs):
    return generate_data(args[5])

# Display the information of the selected item
@app.callback(
    Output('click-data', 'children'),
    Input('graph', 'clickData'),
    Input('item-output', 'children'),
    Input('task-form-output', 'children'),
    Input('meeting-form-output', 'children'),
    State('graph', 'clickData'))
def display_click_data(clickData,a,b,c,stateData):
    if clickData is None:
        return ''
    df = pd.DataFrame(list(Task.objects.all().values()))
    x = df.loc[df['id'] == int(float(clickData['points'][0]['customdata'][2]))]
    if clickData['points'][0]['customdata'][1] == 'Réunion': # Meeting
        df = pd.DataFrame(list(Meeting.objects.all().values()))
        x = df.loc[df['id'] == int(clickData['points'][0]['customdata'][2])]
        text = html.Form([

            # Name
            html.Div([
                html.Div([
                    html.Label('Nom', className='form-label', htmlFor='name'),
                    dbc.Input(id='name', className='form-control', type='text', value=x.name.iloc[0], disabled=True),
                ], className='mb-3'),
            ], className='form-group'),

            # Description
            html.Div([
                html.Div([
                    html.Label('Description', className='form-label', htmlFor='description'),
                    dbc.Textarea(id='description', className='form-control', value=x.description.iloc[0], disabled=True),
                ], className='mb-3'),
            ], className='form-group'),

            # Date
            html.Div([
                html.Div([
                    html.Label('Date', className='form-label', htmlFor='date'),
                    dbc.Input(id='date', className='form-control', type='text', value=x.start_date.iloc[0].strftime('%d/%m/%y'), disabled=True),
                ], className='mb-3'),
            ], className='form-group'),
        ])

    else: # Task
        text = html.Form([
            html.Div([
                html.Div([
                    html.Label('Nom', className='form-label requiredField', htmlFor='name', style={'font-size': ''}),
                    dbc.Input(id='name', className='form-control', type='text', value=x.name.iloc[0], disabled=True),
                ], className='mb-3'),
            ], className='form-group'),

            # Description
            html.Div([
                html.Div([
                    html.Label('Description', className='form-label', htmlFor='description'),
                    dbc.Textarea(id='description', className='form-control', value=x.description.iloc[0], disabled=True),
                ], className='mb-3'),
            ], className='form-group'),

            # Start date
            html.Div([
                html.Div([
                    html.Label('Date de début', className='form-label', htmlFor='start_date'),
                    dbc.Input(id='start_date', className='form-control', type='text', value=x.start_date.iloc[0].strftime('%d/%m/%y'), disabled=True),
                ], className='mb-3'),
            ], className='form-group'),

            # End date
            html.Div([
                html.Div([
                    html.Label('Date de fin', className='form-label', htmlFor='end_date'),
                    dbc.Input(id='end_date', className='form-control', type='text', value=x.end_date.iloc[0].strftime('%d/%m/%y'), disabled=True),
                ], className='mb-3'),
            ], className='form-group'),
        ])
    fig.for_each_trace(
        lambda trace: trace.update(visible=False)
    )
    return text

@app.callback(
    Output('graph', 'clickData'),
    Input('validate2-update-button', 'n_clicks'),
    Input('validate1-update-button', 'n_clicks'))
def display_click_data(*args,**kwargs):
    return None

# Hide delete button before click
@app.callback(
    Output('item-button', component_property='style'),
    Output('click-data', component_property='style'),
    Input('graph', 'clickData'),
    Input('update-item-button', 'n_clicks'),
    Input('validate2-update-button', 'n_clicks'),
    Input('validate1-update-button', 'n_clicks'))
def display_click_data(*args,**kwargs):
    da = kwargs['callback_context']
    if da.triggered != []:
        triggered = da.triggered[0]['prop_id']
        if triggered == 'graph.clickData':
            if args[0] == None:
                return [{'display':'none'},styles['pre']]
            else:
                return [{'display':'inline'},styles['pre']]
        elif triggered == 'validate2-update-button.n_clicks' or triggered == 'validate1-update-button.n_clicks':
            return [{'display':'none'},styles['pre']]
    return [{'display':'none'},{'display':'none'}]

#call back to delete a task or a meeting
@app.callback(
    Output('item-output', 'children'),
    [Input('delete-item-button', 'n_clicks')],
    [State('graph', 'clickData')])
def select_event_button(*args,**kwargs):
    da = kwargs['callback_context']
    if da.triggered != []:
        triggered = da.triggered[0]['prop_id']
        if triggered == 'delete-item-button.n_clicks':
            return delete_task_meeting(args[1])

# delete a task or a meeting
def delete_task_meeting(clickData):
    id_clicked = int(clickData['points'][0]['customdata'][2])
    if clickData['points'][0]['customdata'][1] != 'Réunion':
        task = Task.objects.get(id=id_clicked)
        task.delete()
    else:
        meeting = Meeting.objects.get(id=id_clicked)
        meeting.delete()

# display or hide forms based on the state
@app.callback(
    Output('task-form', component_property='style'),
    Output('meeting-form', component_property='style'),
    Input('update-item-button', 'n_clicks'),
    Input('graph', 'clickData'),
    Input('validate2-update-button', 'n_clicks'),
    Input('validate1-update-button', 'n_clicks'))
def hide_show_form_title(*args,**kwargs):
    da = kwargs['callback_context']
    if da.triggered != []:
        triggered = da.triggered[0]['prop_id']
        if triggered == 'update-item-button.n_clicks':
            if args[1]['points'][0]['customdata'][1] != 'Réunion':
                return [{'display':'inline'},{'display':'none'}]
            else:
                return [{'display':'none'},{'display':'inline'}]
    return [{'display':'none'},{'display':'none'}]

# fill form with current values of a task/meeting
@app.callback(
    Output('input1', component_property='value'),
    Output('textarea1', component_property='value'),
    Output('startdate', component_property='value'),
    Output('enddate', component_property='value'),
    Output('statut-field1', component_property='value'),
    Output('input2', component_property='value'),
    Output('textarea2', component_property='value'),
    Output('date', component_property='date'),
    Input('update-item-button', 'n_clicks'),
    [State('graph', 'clickData')])
def modify_placeholder(*args,**kwargs):
    da = kwargs['callback_context']
    if da.triggered != []:
        triggered = da.triggered[0]['prop_id']
        if triggered == 'update-item-button.n_clicks':
            if args[1]['points'][0]['customdata'][1] != 'Réunion':
                df = pd.DataFrame(list(Task.objects.all().values()))
                x = df.loc[df['id'] == int(float(args[1]['points'][0]['customdata'][2]))]
                str_start_date = x.astype(str).tail(1).reset_index().loc[0, 'start_date']
                start_date = datetime.strptime(str_start_date, '%Y-%m-%d')
                str_end_date = x.astype(str).tail(1).reset_index().loc[0, 'end_date']
                end_date = datetime.strptime(str_end_date, '%Y-%m-%d')
                return [x.name,x.description,start_date.date(),end_date.date(),get_string_statut_name(x.status.iloc[0]),"","",None]
            else:
                df = pd.DataFrame(list(Meeting.objects.all().values()))
                x = df.loc[df['id'] == int(float(args[1]['points'][0]['customdata'][2]))]
                str_date = x.astype(str).tail(1).reset_index().loc[0, 'start_date']
                date = datetime.strptime(str_date, '%Y-%m-%d')
                return ["","",None,None,None,x.name,x.description,date.date()]
    return [None,None,None,None,None,None,None,None]

# get the correponding label status based on the id of the status
def get_string_statut_name(x):
    match x:
        case '1':
            return 'À commencer'
        case '2':
            return 'En cours'
        case '3':
            return 'Terminé'

# get the status id based on the label of the status
def get_string_statut_id(x):
    match x:
        case 'À commencer':
            return '1'
        case 'En cours':
            return '2'
        case 'Terminé':
            return '3'

# callback for the validation of a task form update
@app.callback(
    Output('task-form-output', 'children'),
    Input('validate1-update-button', 'n_clicks'),
    State('input1', 'value'),
    State('textarea1', 'value'),
    State('startdate', 'value'),
    State('enddate', 'value'),
    State('statut-field1', 'value'),
    State('graph', 'clickData'))
def validate_update_task(*args,**kwargs):
    da = kwargs['callback_context']
    if da.triggered != []:
        triggered = da.triggered[0]['prop_id']
        if triggered == 'validate1-update-button.n_clicks':
            id_clicked = int(float(args[6]['points'][0]['customdata'][2]))
            task = Task.objects.get(id=id_clicked)
            if type(args[1]) is not list and args[1] != '':
                task.name = args[1]
            if type(args[2]) is not list:
                task.description = args[2]
            if datetime.strptime(args[3], '%Y-%m-%d') <= datetime.strptime(args[4], '%Y-%m-%d'):
                task.start_date = args[3]
                task.end_date = args[4]
            task.status = get_string_statut_id(args[5])
            task.save()

# callback for the validation of a meeting form update
@app.callback(
    Output('meeting-form-output', 'children'),
    Input('validate2-update-button', 'n_clicks'),
    State('input2', 'value'),
    State('textarea2', 'value'),
    State('date', 'date'),
    State('graph', 'clickData'))
def validate_update_meeting(*args,**kwargs):
    da = kwargs['callback_context']
    if da.triggered != []:
        triggered = da.triggered[0]['prop_id']
        if triggered == 'validate2-update-button.n_clicks':
            id_clicked = int(args[4]['points'][0]['customdata'][2])
            meeting = Meeting.objects.get(id=id_clicked)
            if type(args[1]) is not list and args[1] != '':
                meeting.name = args[1]
            if type(args[2]) is not list:
                meeting.description = args[2]
            meeting.start_date = args[3]
            meeting.save()

# Create the layout of the page
app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(
                id='graph',
                #figure=generate_data(0),
                config=config
            ),
        ])]
    ),
    dcc.Input(id = 'id', value = None, persistence=False, style = {'display':'none'}),
    html.Div([
        html.Div(id='click-data', style=styles['pre']),
    ], className='three columns'),

    # delete button and update button
    html.Div([
        dbc.Button("Modifier", color="primary", className="me-1", id='update-item-button'),
        dbc.Button("Supprimer", color="danger", className="me-1", id='delete-item-button'),
    ],id='item-button', style= {'display':'none'}),
    html.Div(id='item-output'),
    # the form for the tasks updates
    html.Div(
        dbc.Card([
            dbc.CardBody([

                # Name
                html.Div([
                    html.Div([
                        html.Label('Nom*', className='form-label', htmlFor='input1'),
                        dbc.Input(id='input1', className='form-control', type='text'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Description
                html.Div([
                    html.Div([
                        html.Label('Description', className='form-label', htmlFor='textarea1'),
                        dbc.Textarea(id='textarea1', className='form-control'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Start date
                html.Div([
                    html.Div([
                        html.Label('Date de début*', className='form-label', htmlFor='startdate'),
                        dbc.Input(id='startdate', className='form-control date-input', type='date'),
                    ], className='mb-3'),
                ], className='form-group'),

                # End date
                html.Div([
                    html.Div([
                        html.Label('Date de fin*', className='form-label', htmlFor='enddate'),
                        dbc.Input(id='enddate', className='form-control date-input', type='date'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Status
                html.Div([
                    html.Div([
                        html.Label('Status*', className='form-label', htmlFor='statut-field1'),
                        dbc.Select(options=[choice[1] for choice in Task.CHOICES],id='statut-field1'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Validate button
                html.Div(
                    dbc.Button("Valider", id="validate1-update-button", className="btn btn-primary mt-3", style={"width": "100%"}),
                    className='d-grip gap-2'
                )

            ])], className='mt-3 mb-3'
        ),id='task-form', style= {'display':'none'}
    ),
    html.Div(id='task-form-output'),

    # the form for the meetings updates
    html.Div(
        dbc.Card([
            dbc.CardHeader(
                html.H4("Modifier la réunion sélectionnée"),
            ),
            dbc.CardBody([

                # Name
                html.Div([
                    html.Div([
                        html.Label('Nom*', className='form-label', htmlFor='input2'),
                        dbc.Input(id='input2', className='form-control', type='text'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Description
                html.Div([
                    html.Div([
                        html.Label('Description', className='form-label', htmlFor='textarea2'),
                        dbc.Textarea(id='textarea2', className='form-control'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Date
                html.Div([
                    html.Div([
                        html.Label('Date*', className='form-label', htmlFor='date'),
                        dbc.Input(id='date', className='form-control date-input', type='date'),
                    ], className='mb-3'),
                ], className='form-group'),

                # Validate button
                html.Div(
                    dbc.Button("Valider", id="validate2-update-button", className="btn btn-primary mt-3", style={"width": "100%"}),
                    className='d-grip gap-2'
                )

            ])], className='mt-3 mb-3'
        ),id='meeting-form', style= {'display':'none'}
    ),
    html.Div(id='meeting-form-output'),
])

# View to display the gantt chart
def gantt(request, **kwargs):
    # Check that the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Check that the user is a member of the project or the owner
    if not Project.objects.filter(id=kwargs['pk'], members=request.user).exists() \
        and not Project.objects.filter(id=kwargs['pk'], owner=request.user).exists():
        return redirect('projects')

    # Filter the tasks and meetings based on the project id
    tasks = Task.objects.filter(project_id=kwargs['pk'])
    meetings = Meeting.objects.filter(project_id=kwargs['pk'])

    # Get the project or 404
    project = get_object_or_404(Project, pk=kwargs['pk'])

    return render(request, 'tasks/tasks.html', {'my_app': app, 'tasks': tasks, 'meetings': meetings, 'project': project, 'context' : {'id': {'value': kwargs['pk']}}})
