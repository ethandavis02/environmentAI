import dash
from dash import html, dcc, callback, Input, Output, State
from openai import OpenAI
import dash_bootstrap_components as dbc

import dotenv
import os

# Load environment variables
#dotenv.load_dotenv("/home/sustainabilityAI/AI/keys.env")
dotenv.load_dotenv()

key = os.getenv("GPT")
client = OpenAI(
    api_key=key
)
dash.register_page(
    __name__,
    path='/',
    title='EcoCompare - Environmental Decision Analysis',
    name='EcoCompare - Environmental Decision Analysis',
    description="Compare the environmental impact of two decisions and receive a sustainability score with AI-powered insights."
)


def layout():
    return html.Div([
        html.Header(
            "Environmental Decision Impact AI",
            style={
                'backgroundColor': '#4CAF50',
                'color': 'white',
                'padding': '15px 0',
                'textAlign': 'center',
                'fontSize': '24px',
                'fontWeight': 'bold',
                'width': '100%',
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'zIndex': '1000'
            }
        ),
        html.Br(), html.Br(), html.Br(),

        dcc.Tabs(id='tabs', value='compare', children=[
            dcc.Tab(
                label='Compare Two Decisions',
                value='compare',
                style={
                    'fontWeight': 'bold',
                    'padding': '10px 20px',
                    'borderRadius': '50px',
                    'backgroundColor': 'gray',
                    'color': 'white'
                },
                selected_style={
                    'fontWeight': 'bold',
                    'padding': '10px 20px',
                    'borderRadius': '50px',
                    'backgroundColor': '#388E3C',  # darker green for selected
                    'color': 'white',
                    'outline': 'none',  # Remove focus outline
                    'border': 'none'  # Remove border
                }
            ),
            dcc.Tab(
                label='Single Item Analysis',
                value='single',
                style={
                    'fontWeight': 'bold',
                    'padding': '10px 20px',
                    'borderRadius': '50px',
                    'backgroundColor': 'gray',
                    'color': 'white'
                },
                selected_style={
                    'fontWeight': 'bold',
                    'padding': '10px 20px',
                    'borderRadius': '50px',
                    'backgroundColor': '#388E3C',  # darker green for selected
                    'color': 'white',
                    'outline': 'none',  # Remove focus outline
                    'border': 'none'  # Remove border
                }
            )
        ], style={
            'width': '80%',
            'maxWidth': '600px',
            'margin': 'auto',
            'backgroundColor': 'white',
            'padding': '30px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.1)',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'borderRadius': '50px'  # make the tab container pill-shaped
        }),
        html.Br(),
        html.Div(id='tabscontent', style={
            'width': '80%', 'maxWidth': '600px', 'margin': 'auto', 'backgroundColor': 'white',
            'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.1)'
        })
    ])


@callback(
    Output('tabscontent', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    print(tab)
    if tab == 'compare':
        return html.Div([
            html.H2("Compare Two Environmental Decisions", style={'textAlign': 'center', 'color': '#333'}),
            html.Br(),
            html.P('Use this website to compare the environmental impact of two decisions. '
                   'For more accurate results, make sure you include details such as location '
                   'and any other relevant information.'),
            html.Br(),
            html.Div([
                html.Label("Decision 1", style={'fontWeight': 'bold', 'color': '#555'}),
                dcc.Textarea(id='decision1', placeholder="Describe decision 1...", rows=4,
                             style={'width': '100%', 'padding': '10px'}),
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Label("Decision 2", style={'fontWeight': 'bold', 'color': '#555'}),
                dcc.Textarea(id='decision2', placeholder="Describe decision 2...", rows=4,
                             style={'width': '100%', 'padding': '10px'}),
            ], style={'marginBottom': '20px'}),

            html.Button("Compare Decisions", id='comparebtn', n_clicks=0, style={
                'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none', 'padding': '12px 20px',
                'fontSize': '16px', 'borderRadius': '5px', 'cursor': 'pointer', 'width': '100%'
            }),

            dbc.Spinner(html.Div(id="spinner")),

            html.Div(id='outputcontainer', style={
                'marginTop': '30px', 'padding': '20px', 'borderRadius': '10px',
                'backgroundColor': 'white', 'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.1)', 'display': 'block'
            })
        ])
    elif tab == 'single':
        return html.Div([
            html.H2("Single Item Environmental Analysis", style={'textAlign': 'center', 'color': '#333'}),
            html.Br(),
            html.P('Use this tool to analyze the environmental impact of a single product or action.'
                   'Provide as much detail as possible to ensure accurate results.'),
            html.Br(),
            html.Div([
                html.Label("Describe the Item", style={'fontWeight': 'bold', 'color': '#555'}),
                dcc.Textarea(id='singleitem', placeholder="Describe the item...", rows=4,
                             style={'width': '100%', 'padding': '10px'}),
            ], style={'marginBottom': '20px'}),

            html.Button("Analyze", id='analyzebtn', n_clicks=0, style={
                'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none', 'padding': '12px 20px',
                'fontSize': '16px', 'borderRadius': '5px', 'cursor': 'pointer', 'width': '100%'
            }),
            dbc.Spinner(html.Div(id="spinner1")),

            html.Div(id='singleoutputcontainer', style={
                'marginTop': '30px', 'padding': '20px', 'borderRadius': '10px',
                'backgroundColor': 'white', 'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.1)', 'display': 'block'
            })
        ])


@callback(
    [Output('outputcontainer', 'children'),
     Output('outputcontainer', 'style'),
     Output('spinner', 'children')],
    Input('comparebtn', 'n_clicks'),
    State('decision1', 'value'),
    State('decision2', 'value'),
    prevent_initial_call=True
)
def compare_decisions(n_clicks, decision1, decision2):
    if not decision1 or not decision2:
        return "Please fill out both decision fields.", {'display': 'block', 'color': 'red'}, ''

    # Call GPT-4 API
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in environmental sustainability."},
                {"role": "user", "content": (
                    f"Compare the environmental impact of these two decisions:"
                    f"\nDecision 1: {decision1}"
                    f"\nDecision 2: {decision2}"
                    "\nOutput format: "
                    "Decision 1 impact description (max one sentence) | Decision 1 ~carbon emissions (give this a comparision so users can understand more then just a number) |"
                    "Decision 2 impact description (max one sentence) | Decision 2 ~carbon emissions (give this a comparision so users can understand more then just a number) |"
                    "A comparison of the two and advice on which is better."
                )}
            ]
        )
        result_text = response.choices[0].message.content
        result_text = str(result_text)
        parts = result_text.split("|")
        impact1 = parts[0].replace("Decision 1 impact description: ", "")
        emissions1 = parts[1].replace("Decision 1 ~carbon emissions: ", "")
        impact2 = parts[2].replace("Decision 2 impact description: ", "")
        emissions2 = parts[3].replace("Decision 2 ~carbon emissions: ", "")
        comparison_advice = "".join(parts[4:]).replace("Comparison and advice: ", "")

        return html.Div([
            html.Br(),
            html.H3("Results", style={'color': '#333'}),
            html.Br(),
            html.H5("Decision 1:", style={'color': '#1E90FF'}),
            html.P(impact1),
            html.P(f"Carbon Emissions: {emissions1}"),
            html.H5("Decision 2:", style={'color': '#32CD32'}),
            html.P(impact2),
            html.P(f"Carbon Emissions: {emissions2}"),
            html.H5("Comparison & Advice:", style={'color': '#FF4500'}),
            html.P(comparison_advice),
        ]), {'display': 'block'}, ''

    except Exception as e:
        return f"Error processing request: {str(e)}", {'display': 'block', 'color': 'red'}, ''


@callback(
    [Output('singleoutputcontainer', 'children'),
     Output('singleoutputcontainer', 'style'),
     Output('spinner1', 'children')],
    Input('analyzebtn', 'n_clicks'),
    State('singleitem', 'value'),
    prevent_initial_call=True
)
def analyze_environmental_impact(n_clicks, item):
    if not item:
        return "Please describe the item to analyze.", {'display': 'block', 'color': 'red'}, ''

    # Call GPT-4 API for detailed analysis
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in sustainability analysis."},
                {"role": "user", "content": (
                    f"Provide an environmental impact assessment for the following item:\n"
                    f"{item}\n"
                    "Include carbon footprint, resource consumption, pollution impact, and recommendations. "
                    "\n Output Format:"
                    "Brief environmental impact description (max one sentence) | "
                    "~ carbon footprint (give this a comparision so users can understand more then just a number) |"
                    "Sustainable alternative"
                )}
            ]
        )

        result_text = response.choices[0].message.content
        parts = result_text.split("|")
        desc = parts[0].replace("Brief environmental impact description: ", "")
        footprint = parts[1].replace("~ Carbon footprint: ", "")
        alt = parts[2].replace("Sustainable alternative: ", "")
        return html.Div([
            html.Br(),
            html.H3("Environmental Impact Analysis", style={'color': '#333'}),
            html.Br(),
            html.H5("Enironmental Impact Description", style={'color': '#4CAF50'}),
            html.P(desc),
            html.H5("~ Carbon Footprint", style={'color': '#4CAF50'}),
            html.P(footprint),
            html.H5("Sustainable Alternative", style={'color': '#4CAF50'}),
            html.P(alt),
            # html.P(result_text, style={'fontSize': '16px', 'whiteSpace': 'pre-wrap'})
        ]), {"display": "block"}, ''

    except Exception as e:
        return f"Error processing request: {str(e)}", {'display': 'block', 'color': 'red'}, ''
