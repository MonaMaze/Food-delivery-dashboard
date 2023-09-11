#----------------------------# Load Your Dependencies#--------------------------#
import dash
from dash import  dcc    # Dash core Components
from dash import html   # HTML for Layout and Fonts
import plotly.express as px           # Plotly Graphs uses graph objects internally
from plotly.subplots import make_subplots
import plotly.graph_objects as go     # Plotly Graph  more customized 
import pandas as pd                   # Pandas For Data Wrangling
import numpy as np
from dash import Input, Output, dash_table  # Input, Output for  Call back functions
import dash_pivottable

#--------------------------#Instanitiate Your App#--------------------------#

app = dash.Dash(__name__)  
server = app.server

#--------------------------# Pandas Section #------------------------------#

df =pd.read_csv('onlinedeliverydata.csv')
group = ['Consumer demographics', 'Meal perefernces', 'Satisfaction', 'Not purchasing concerns', 'Cancellation concerns', 'Pereferences', 'Loyality']
demog = ['Age', 'Gender', 'Marital Status',"Occupation", 'Monthly Income', "Educational Qualifications", 'Family size']
peref= ['Medium (P1)', 'Medium (P2)', 'Meal(P1)', 'Meal(P2)', 'Perference(P1)', 'Perference(P2)']
satis = ['Ease and convenient', 'Time saving', 'More restaurant choices', 'Easy Payment option', 'More Offers and Discount', 'Good Food quality', 'Good Tracking system']
purc = ['Self Cooking', 'Health Concern', 'Late Delivery', 'Poor Hygiene', 'Bad past experience', 'Unavailability', 'Unaffordable']
canc = ['Long delivery time', 'Delay of delivery person getting assigned', 'Delay of delivery person picking up food', 'Wrong order delivered', 'Missing item', 'Order placed by mistake']
perf = ['Influence of time', 'Order Time', 'Maximum wait time', 'Residence in busy location', 'Google Maps Accuracy', 'Good Road Condition', 'Low quantity low time', 'Delivery person ability']
loyl = ['Influence of rating', 'Less Delivery time', 'High Quality of package', 'Number of calls', 'Politeness', 'Freshness ', 'Temperature', 'Good Taste ', 'Good Quantity', 'Output']
all_g = [demog, peref, satis, purc, canc, perf, loyl]
df_lst = [df.columns.values.tolist()] + df.values.tolist()
#--------------------------------------------------------------------------#
    
app.layout = html.Div([html.Div([html.A([html.H2('Food Delivery Analysis Dashboard'),html.Img(src='/assets/logo2.png')],  # A for hyper links
                                        href='http://projectnitrous.com/')],className="banner"),
                       # First raw
                       html.Div([
                           html.H4('Univariate Analysis for the data assigned groups'),
                       ], className="eleven columns", style={'padding':10}),
                       # Univariate Analysis
                       html.Div([
                           dcc.Dropdown(
                                id='dropdown_grp',
                                options=[{'label':group[i], 'value':i} for i in range(len(group))],
                                value=0,
                                multi=False,
                                searchable=True,
                                clearable=False
                           ),
                           html.Div(
                               dcc.Graph(id='hist_grp'),
                           ),
                       ], className="eleven columns", style={'backgroundColor': '#2a2b4a', 'padding':10}),
                       
                       html.Div([html.Br(),],className="eleven columns"),
                       # Second raw
                       html.Div([
                           html.H4('Multivariate Analysis (group 1 vs rest)'),
                       ], className="five columns", style={'padding':10}),
                       html.Div([
                           html.H4('Multivariate Analysis (all vs all)'),
                       ], className="five columns", style={'padding':10}),
                       # Multivariate Analysis
                       html.Div([
                           dcc.Dropdown(
                                id='dropdown_var1',
                                options=[{'label':i, 'value':i} for i in df.iloc[:,:7]],
                                value='Age',
                                multi=False,
                                searchable=True,
                                clearable=False
                           ),
                           dcc.Dropdown(
                                id='dropdown_var2',
                                options=[{'label':i, 'value':i} for i in df.iloc[:,10:-2]],
                                value='Medium (P1)',
                                multi=False,
                                searchable=True,
                                clearable=False
                           ),
                           html.Div(
                               dcc.Graph(id='sun_multi1'),
                           ),
                       ], className="five columns", style={'backgroundColor': '#2a2b4a', 'padding':10}),
                       # Multivariate Analysis
                       html.Div([
                           dcc.Dropdown(
                                id='dropdown_var3',
                                options=[{'label':i, 'value':i} for i in df[:7]],
                                value='Age',
                                multi=False,
                                searchable=True,
                                clearable=False
                           ),
                           dcc.Dropdown(
                                id='dropdown_var4',
                                options=[{'label':i, 'value':i} for i in df[11:-2]],
                                value='Medium (P1)',
                                multi=False,
                                searchable=True,
                                clearable=False
                           ),
                           html.Div(
                               dcc.Graph(id='sun_multi2'),
                           ),
                       ], className="five columns", style={'backgroundColor': '#2a2b4a', 'padding':10}),
                       
                       html.Div([html.Br(),],className="eleven columns"),
                       # Third row
                       # Pivot table
                       html.Div([
                           html.H4('Pivot table for the assigned groups'),
                       ], className="eleven columns", style={'padding':10}),
                       html.Div([
                           dcc.RadioItems(
                               id='radio_piv',
                                options=[{'label':group[i], 'value':i} for i in range(len(group))],
                                value=0,
                                labelStyle={'display': 'inline-block'}
                           ),
                           html.Div(
                               id = 'piv'
                           ),
                       ], className="eleven columns", style={'backgroundColor': '#2a2b4a', 'padding':10, 'color':'#ffffff'}),
               ], className="twelve columns", style={'backgroundColor': '#1b203d', 'width':'100%', 'height':'100%', 'top':'0px', 'left':'0px'})

@app.callback(
    Output('hist_grp', 'figure'),
    Input('dropdown_grp', 'value'),
    )
def grp_hist(value):
    for i in range(len(all_g)):
        if i == int(value):
            col_len = len(all_g[i])
            fig = make_subplots(rows=1, cols=col_len)
            for x in range(1, col_len+1):
                x_val=str(all_g[i][x-1])
                fig.add_trace(px.histogram(df, x=x_val, barmode='group', labels=x_val, text_auto=True, color_discrete_sequence=['indianred']).data[0], row=1, col=x)
                fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor':'rgba(255,234,238,1)'}, xaxis_title=x_val)
    return fig

@app.callback(
    Output('sun_multi1', 'figure'),
    Input('dropdown_var1', 'value'),
    Input('dropdown_var2', 'value'),
    )
def multi1_sun(value1, value2):
    fig = px.sunburst(data_frame=df, path=(value1, value2))
    fig.update_traces(textinfo='label+percent parent')
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    return fig

@app.callback(
    Output('sun_multi2', 'figure'),
    Input('dropdown_var3', 'value'),
    Input('dropdown_var4', 'value'),
    )
def multi2_sun(value1, value2):
    fig = px.sunburst(data_frame=df, path=(value1, value2))
    fig.update_traces(textinfo='label+percent parent')
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    return fig

@app.callback(
    Output('piv', 'children'),
    Input('radio_piv', 'value'),
    )
def display_piv(val):
    df_grp = [df[all_g[val]].columns.values.tolist()] + df[all_g[val]].values.tolist()
    piv_tab = dash_pivottable.PivotTable(
                                        id='table',
                                        data=df_grp,
                                        cols=[df_grp[0][0]],
                                        colOrder="key_a_to_z",
                                        rows=[df_grp[0][1]],
                                        rowOrder="key_a_to_z",
                                        rendererName="Table",
                                        aggregatorName="Count",
                                        )
    return piv_tab


if __name__ == '__main__':
    app.run_server()
