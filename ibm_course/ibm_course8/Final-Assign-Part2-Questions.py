import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# Load data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'd51iMGfp_t0QpO30Lym-dw/automobile-sales.csv'
)

app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = list(range(1980, 2024))

app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 24
        }
    ),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type'
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980
        )
    ]),

    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex', 'flexDirection': 'column'}
        )
    ])
])


# Enable/disable the year input
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    return True


# Create dashboard charts
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)
def update_output_container(selected_statistics, input_year):

    # Recession statistics
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Chart 1: Sales over recession years
        yearly_rec = recession_data.groupby(
            'Year'
        )['Automobile_Sales'].mean().reset_index()

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Fluctuation over Recession Period'
            )
        )

        # Chart 2: Average vehicle sales by type
        average_sales = recession_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Automobile Sales by Vehicle Type during Recession'
            )
        )

        # Chart 3: Advertising expenditure by vehicle type
        exp_rec = recession_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Total Advertising Expenditure by Vehicle Type during Recession'
            )
        )

        # Chart 4: Unemployment effect
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                [html.Div(R_chart1), html.Div(R_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                [html.Div(R_chart3), html.Div(R_chart4)],
                style={'display': 'flex'}
            )
        ]

    # Yearly statistics
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Chart 1: Sales trend across all years
        yas = data.groupby(
            'Year'
        )['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales by Year'
            )
        )

        # Chart 2: Monthly sales for chosen year
        mas = yearly_data.groupby(
            'Month'
        )['Automobile_Sales'].sum().reset_index()

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Chart 3: Average sales by vehicle type
        avr_vdata = yearly_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the Year {}'.format(input_year)
            )
        )

        # Chart 4: Advertising expenditure by vehicle type
        exp_data = yearly_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Total Advertisement Expenditure by Vehicle Type in {}'.format(input_year)
            )
        )

        return [
            html.Div(
                [html.Div(Y_chart1), html.Div(Y_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                [html.Div(Y_chart3), html.Div(Y_chart4)],
                style={'display': 'flex'}
            )
        ]

    return None


if __name__ == '__main__':
    app.run(debug=True)