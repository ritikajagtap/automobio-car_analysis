import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd


import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

from dash_extensions import Lottie
import dash_bootstrap_components as dbc
url_electric = "https://assets9.lottiefiles.com/private_files/lf30_jlatyxnr.json"
url_petrol = "https://assets8.lottiefiles.com/packages/lf20_zqojwy4n.json"
url_deisel = "https://assets1.lottiefiles.com/packages/lf20_lcmbmqz5.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.title = "Automobio-Car Analysis"

df = pd.read_csv (r'dataset.csv')

# Airbags
df_air = df['Airbags'].dropna()
uni = {}
for row in df_air:
    id = row.split(',')
    for typ in id:
        if typ[0] == ' ':
            typ = typ[1:]
        if (typ in uni):
             uni[typ] += 1
        else:
             uni[typ] = 1

airb = pd.DataFrame(uni.items(), columns=['Type', 'Count'])
airBags = px.pie(airb, values='Count', names='Type', title='Airbags', template='plotly_dark')

#AudioSystem
df_audio = df['Audiosystem'].value_counts()
df_audio = pd.DataFrame({'Audiosystem':df_audio.index, 'Count':df_audio.values})
audioSystem = px.pie(df_audio, values='Count', names='Audiosystem', title='Audiosystem', template='plotly_dark')

#EBD
ebd = df['EBD_(Electronic_Brake-force_Distribution)'].value_counts()
ebd = pd.DataFrame({'EBD':ebd.index, 'Count':ebd.values})
ebd_avail = px.bar(ebd, y="Count", x="EBD",  title="Electronic Brake-force Distribution", template='plotly_dark', color_discrete_sequence=["#00C000"])

# Gear Shift Reminder
gsr = df['Gear_Shift_Reminder'].value_counts()
gsr = pd.DataFrame({'GSR':gsr.index, 'Count':gsr.values})
gsrFig = px.bar(gsr, y="Count", x="GSR",  title="Gear Shift Reminder", template='plotly_dark', color_discrete_sequence=["#00C000"])

X = df['City_Mileage'].mean()
df['City_Mileage'] = df['City_Mileage'].replace(0, X)


df_pet = df["Fuel_Type"].value_counts()
df_pet = pd.DataFrame({'Fuel_Type':df_pet.index, 'Count':df_pet.values})

# Bar Chart for the Launch Month
df_bar2 = df['Launch Month'].value_counts()
fig = px.bar(df_bar2, y="Launch Month", labels={"Launch Month": "Count of automobile launched", "index": "Launch Month"}, template='plotly_dark', title="Car Launches VS Month", color_discrete_sequence=["#00C000"])

# Scatter Chart for Kerb Weight vs City_Mileage
fig1 = px.scatter(df, x="Kerb_Weight", y="City_Mileage", color="Fuel_Type", labels={"Kerb_Weight": "Kerb Weight(1 unit = 1kg)", "City_Mileage": "City Mileage (km/litre)/(km/Full Charge)"}, title='City Mileage VS Kerb Weight and ', template="plotly_dark", )
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                           html.Div([
                    html.H2("Automobile Analysis:"),
                ], style={'textAlign': 'center'})

                ])
            ]),
        ], width=12),
    ],className='mb-2 mt-2'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="45%", height="45%", url=url_electric)),
                dbc.CardBody([
                    html.H6('Electric'),
                    html.H2(id='content-connections', children="1.15%")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="80%", height="80%", url=url_petrol)),
                dbc.CardBody([
                      html.H6('Petrol'),
                      html.H2(id='content-companies', children="50.17%")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="80%", height="80%", url=url_petrol)),
                dbc.CardBody([
                      html.H6('Deisel'),
                      html.H2(id='content-msg-in', children="47.53%")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="80%", height="80%", url=url_deisel)),
                dbc.CardBody([
                    html.H6('CNG'),
                    html.H2(id='content-msg-out', children="1.15%")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ],className='mb-2 mt-2'),
     dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                dcc.Dropdown(
                    options=[
                        {'label': 'Petrol', 'value': 'Petrol'},
                        {'label': 'Electric', 'value': 'Electric'},
                        {'label': 'Diesel', 'value': 'Diesel'},
                        {'label': 'CNG', 'value': 'CNG'},
                    ],
                    value='Petrol',
                    className='mb-2',
                    style={'color': 'black'},
                    id='my_dropdown'
                    )
                ])
            ])

        ], width=12),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
#                     dcc.Graph(id='scatter-chart', figure={}),
                    dcc.Graph(id='scatter-chart', figure={}, config={'displayModeBar': False}),
                    html.P("From the above graph, it is clear that Electric Cars give much better mileage than Petrol, Diesel and CNG Cars at the same price segment.", style={"font-weight": "bold"})
                ])
            ]),
        ], width=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='TBD', figure={}),
                    html.P("From the above pie chart, it can be seen that most of the Diesel, Petrol, CNG cars are emitting BS4 which is more harmful for the environment but Electric Cars are emitting BS6 which is comparatively less Harmful.", style={"font-weight": "bold"})
                ])
            ]),
        ], width=5),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}),
                    html.P("The above pie chart shows the manufacturers of Petrol/ Diesel/ CNG/ Electric Cars respectively. It can be observed that very few manufacturers are producing Electric Cars, which gives a big scope for other companies to capture the market.", style={"font-weight": "bold"})
                ])
            ]),
        ], width=12),

    ],className='mb-2 mt-2' 'align-self-center'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='scatter-chart2', figure=fig1),
                     html.P("In the above Scatter Chart we have City Mileage VS Kerb Weight. It can be observed that for maximum Kerb Weight, City Mileage is minimum. Electric Cars are providing very High City Mileage with low kerb weight, due to this people will prefer electric cars over the other!", style={"font-weight": "bold"})
                ])
            ]),
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='bar-chart', figure=fig),
                     html.P("From the above figure, it is clear that maximum car launches are happening in the month of January and March.", style={"font-weight": "bold"})
                ])
            ]),
        ], width=4),


    ],className='mb-2 mt-2' 'align-self-center'),
     dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
               html.H2("Most Popular Specifications!", style={"font-weight": "bold"})
                ])
            ]),
        ], width=12),

    ],className='mb-2 mt-2' 'align-self-center'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='airbags-chart', figure=airBags),
                    html.P("Driver Frontal Airbag is Provided by most of the automobiles!", style={"font-weight": "bold"})
                ])
            ]),
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=ebd_avail),
                    html.P("Many vehicles with Electronic Brake Force Distribution ae produced!", style={"font-weight": "bold"})
                ])
            ]),
        ], width=4),

    ],className='mb-2 mt-2' ),
    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=audioSystem),
                    html.P("The music system CD Player with USB and Aux-in is provided by maximum vehicles!", style={"font-weight": "bold"})

                ])
            ]),
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=gsrFig),
                    html.P("Gear Shift Reminder feature is given in many vehicles!", style={"font-weight": "bold"})

                ])
            ]),
        ], width=4),

    ],className='mb-2 mt-2' ),
], fluid=True)

@app.callback(
    Output('scatter-chart', 'figure'),
    Input('my_dropdown', 'value')
)
def update_output(value):
    if(value == "Electric"):
        ds1 = df[df['Fuel_Type']=="Electric"]
        fig1 = px.scatter(ds1, x="Electric_Range", y="Ex-Showroom_Price", labels={"Ex-Showroom_Price": "Showroom Price(inr)", "Electric_Range": "Electric Mileage (km/Full charge)"}, hover_data=[ds1.Model], title="Showroom Price(inr) VS City Mileage(km/Full charge)", template="plotly_dark", color_discrete_sequence=["#00C000"])
        return fig1

    else:
        df_scatter = df[df["Fuel_Type"]==value]
        fig1 = px.scatter(df_scatter, x="City_Mileage", y="Ex-Showroom_Price", labels={"Ex-Showroom_Price": "Showroom Price(inr)", "City_Mileage": "City Mileage (km/litre)"}, hover_data=[df_scatter.Model], title="Showroom Price(inr) VS City Mileage(km/lt)", template="plotly_dark", color_discrete_sequence=["#00C000"])
        return fig1

@app.callback(
    Output('TBD', 'figure'),
    Input('my_dropdown', 'value')
)
def update_output2(value):
    df_bar = df[df["Fuel_Type"]==value]
    x1 = df_bar['Emission_Norm'].value_counts()
    df_pie2 = pd.DataFrame({'Emission_Norm':x1.index, 'Count':x1.values})
    fig = px.pie(df_pie2, values='Count', names='Emission_Norm',  title="Emission Norms", template="plotly_dark",)
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    Input('my_dropdown', 'value')
)
def update_output3(value):
    df_pie = df[df["Fuel_Type"]==value]
    x2 = df_pie['Make'].value_counts()
    df_pie2 = pd.DataFrame({'Make':x2.index, 'Count':x2.values})
    fig = px.pie(df_pie2, values='Count', names='Make',  title="Car Manufacturers",labels={"Make": "Manufacturer", "Count": "Cars Launched (units)"},  template="plotly_dark", )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)