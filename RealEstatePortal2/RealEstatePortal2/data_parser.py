# Подключаем библиотеки
import datetime
import time
import httplib2
import googleapiclient.discovery
import os
import requests
import lxml.html
from datetime import date
from lxml import etree

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'forward-entity-375213-be9bf9b937e1.json'  # Имя файла с закрытым ключом, вы должны подставить свое
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

spreadsheetId = '1-vbqifmAR3bcf1JQIwYEMCHkyUi07lApyaYLq_St8BA'  # сохраняем идентификатор файла



class data_parser():
    property_unit = {}

    def __init__(self):
        self.parse_from_QL_public()

    def parse_from_QL_public(self):
        self.property_unit={
            "ref": "75725",
            "prop_type": "Apartments",
            "prop_location": "St. Julian's",
            "price": "1500",
            "status": "Available",
            "bedrooms": 1,
            "bathrooms": 1,
            "description": "Introducing a brand new (2023), elegantly designed one-bedroom apartment, boasting a "
                           "stunning living room and a captivating balcony, offering an unparalleled blend of "
                           "modernity and comfort. The flat is fully air-conditioned, with new appliances, "
                           "a dishwasher, and a washing machine./n/nWorth a viewing!"
        }


    def get_property(self):
        return self.property_unit