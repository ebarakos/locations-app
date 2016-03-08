from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
import json
from apiclient.discovery import build
from django.core import serializers


def index(request):
	if request.POST.get('button'):
		deleteAll()
	data = serializers.serialize( "python", Location.objects.all() )
	return render(request, "index.html", {'data' : data} )

def create_post(request):
	if request.method == 'POST':
		lat = request.POST.get('lat')
		lng = request.POST.get('lng')
		address = request.POST.get('address')
		loc = Location(address=address,lat=lat,lng=lng)
		loc.save()
		insertUniqueRow(loc)
		return HttpResponse(
	    json.dumps({ "ok": "ok"}),
	    content_type="application/json"
		)
	else:
		return HttpResponse(
	    json.dumps({"error": "error"}),
	    content_type="application/json"
	)

def insertUniqueRow(loc):
  table_id = "1oGMujUCtTgLLx6LjzAvCfGPSd1CtFegQvfY3-dmP"
  # print(loc.address)
  checkForDuplicates = "SELECT * FROM {} WHERE Address='{}' AND Lat={} AND Lng={}".format(table_id,loc.address,loc.lat,loc.lng)
  # print (checkForDuplicates)
  addRow = "INSERT INTO {}(Address,Lat,Lng) VALUES('{}',{},{})".format(table_id,loc.address,loc.lat,loc.lng) # Single quotes
  scopes = ['https://www.googleapis.com/auth/fusiontables']
  HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(HOME, 'test.json'), scopes=scopes)
  http_auth = credentials.authorize(Http())
  service = build("fusiontables", "v1", http=http_auth)
  if not 'rows' in service.query().sql(sql=checkForDuplicates).execute():
  	service.query().sql(sql=addRow).execute()

def deleteAll():
  table_id = "1oGMujUCtTgLLx6LjzAvCfGPSd1CtFegQvfY3-dmP"
  deleteAllRows="DELETE FROM {}".format(table_id)

  scopes = ['https://www.googleapis.com/auth/fusiontables']
  HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(HOME, 'test.json'), scopes=scopes)
  http_auth = credentials.authorize(Http())
  service = build("fusiontables", "v1", http=http_auth)
  service.query().sql(sql=deleteAllRows).execute()
  Location.objects.all().delete()


