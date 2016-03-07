from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
import json
from apiclient.discovery import build


def index(request):
 	return render(request, "index.html")

def create_post(request):
	if request.method == 'POST':
		lat = request.POST.get('lat')
		lng = request.POST.get('lng')
		address = request.POST.get('address')
		loc = Location(address=address,lat=lat,lng=lng)
		loc.save()
		insertRow(loc)
		return HttpResponse(
	    json.dumps({ "ok": "ok"}),
	    content_type="application/json"
		)
	else:
		return HttpResponse(
	    json.dumps({"error": "error"}),
	    content_type="application/json"
	)

def insertRow(loc):
  table_id = "1oGMujUCtTgLLx6LjzAvCfGPSd1CtFegQvfY3-dmP"
  print(loc.address)

  query = "INSERT INTO {}(Address,Lat,Lng) VALUES('{}',{},{})".format(table_id,loc.address,loc.lat,loc.lng) # Single quotes
  print(loc.lat)
  print(loc.lng)
  scopes = ['https://www.googleapis.com/auth/fusiontables']
  HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(HOME, 'test.json'), scopes=scopes)
  http_auth = credentials.authorize(Http())
  service = build("fusiontables", "v1", http=http_auth)
  service.query().sql(sql=query).execute()