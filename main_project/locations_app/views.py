from django.shortcuts import render
from .models import Location
from django.core import serializers
from .service import service


table_id = "1oGMujUCtTgLLx6LjzAvCfGPSd1CtFegQvfY3-dmP"


def index(request):
    data = serializers.serialize("python", Location.objects.all())
    return render(request, "index.html", {'data': data})


def delete(request):
    deleteAll()
    data = serializers.serialize("python", Location.objects.all())
    return render(request, "locations-list.html", {'data': data})


def saveLocation(request):
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    address = request.POST.get('address')
    loc = Location(address=address, lat=lat, lng=lng)
    loc.save()
    insertUniqueRow(loc)
    data = serializers.serialize("python", Location.objects.all())
    return render(request, "locations-list.html", {'data': data})


def insertUniqueRow(loc):
    addRow = "INSERT INTO {}(Address,Lat,Lng) VALUES('{}',{},{})".format(table_id, loc.address, loc.lat, loc.lng)
    checkForDuplicates = "SELECT * FROM {} WHERE Address='{}' AND Lat={} AND Lng={}".format(table_id, loc.address, loc.lat, loc.lng)
    if 'rows' not in service.query().sql(sql=checkForDuplicates).execute():
        service.query().sql(sql=addRow).execute()


def deleteAll():
    deleteAllRows = "DELETE FROM {}".format(table_id)
    service.query().sql(sql=deleteAllRows).execute()
    Location.objects.all().delete()
