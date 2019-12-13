from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import rdflib
import re


######################
### Views for HTML ###
######################

def home(request):
    return render(request, 'semanticSearch/home.html', {})

def search_booking(request):
    result = make_query("booking_rdf.owl", request)
    # return HttpResponse(booking_query_text(request))
    return render(request, 'semanticSearch/search_booking.html', {"result": result})

def search_menu_item(request):
    result = make_query("booking_rdf.owl", request)
    # return HttpResponse(menu_query_text(request))
    return render(request, 'semanticSearch/search_menu_item.html', {"result": result})

def search_employee(request):
    result = make_query("booking_rdf.owl", request)
    # return HttpResponse(employee_query_text(request))
    return render(request, 'semanticSearch/search_employee.html', {"result": result})



#################
### functions ###
#################

def make_connection(rdf_file):
    g = rdflib.Graph()
    g.parse(rdf_file)
    return g

def make_query(rdf_file, request):
    g = rdflib.Graph()
    g.parse(rdf_file)
    query_text = makeQueryText(request)
    qres = g.query(query_text)
    return qres


def makeQueryText(request):
    if bool(re.search('booking', request.path)):
        query_text = booking_query_text(request)

    if bool(re.search('menu', request.path)):
        query_text = menu_query_text(request)

    if bool(re.search('employee', request.path)):
        query_text = employee_query_text(request)

    return query_text