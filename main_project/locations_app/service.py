from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import os
from apiclient.discovery import build


scopes = ['https://www.googleapis.com/auth/fusiontables']
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(HOME, 'credentials.json'), scopes=scopes)
http_auth = credentials.authorize(Http())
service = build("fusiontables", "v1", http=http_auth)
