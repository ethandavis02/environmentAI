
import openai
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import smtplib
from flask import request, jsonify, redirect, url_for, render_template
import requests
import base64
from flask import request, jsonify
from email.message import EmailMessage

from flask import session

import sqlite3
import warnings
from dotenv import load_dotenv

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
    ],
    update_title=None,
    use_pages=True,  # New in Dash 2.7 - Allows us to register pages
)

app.title = "Env Help"

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=True),
    dash.page_container,
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)