import os
import gspread

from google.oauth2.service_account import Credentials


def initialize_spreadsheet() -> gspread.Spreadsheet:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = Credentials.from_service_account_file(
        "credentials.json", scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    spreadsheet = client.open_by_key(spreadsheet_id)

    return spreadsheet


def scrape_ru_group_links(spreadsheet: gspread.Spreadsheet) -> list[str]:
    ru_groups_worksheet = spreadsheet.get_worksheet(0)

    return ru_groups_worksheet.col_values(4)


def scrape_en_group_links(spreadsheet: gspread.Spreadsheet) -> list[str]:
    en_groups_worksheet = spreadsheet.get_worksheet(1)

    return en_groups_worksheet.col_values(4)


def scrape_channels_links(spreadsheet: gspread.Spreadsheet) -> list[str]:
    channels_worksheet = spreadsheet.get_worksheet(2)

    return channels_worksheet.col_values(4)
