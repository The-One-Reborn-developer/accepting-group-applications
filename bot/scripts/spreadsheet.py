import os
import gspread
import logging

from google.oauth2.service_account import Credentials


def initialize_spreadsheet() -> gspread.Worksheet:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = Credentials.from_service_account_file(
        "credentials.json", scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    spreadsheet = client.open_by_key(spreadsheet_id)

    worksheet = spreadsheet.sheet1

    return worksheet
