from django.db import models
from datetime import datetime

####################################
### Query texts created here ###
####################################
def convert_date(date):
    return str(datetime.strptime(date, "%d/%m/%Y").date())


def prefix():
    return """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX dc: <http://purl.org/dc/terms/>
        PREFIX bk: <http://www.restbook.com/>

        """
def booking_query_text(request):
    base_query = prefix() + """
        SELECT ?id ?name ?email ?phone ?time ?seat ?dname
        WHERE {
                ?book a bk:Booking.
                ?book bk:has_name ?name.
                ?book bk:has_id ?id.
                ?book bk:has_email ?email.
                ?book bk:has_phone ?phone.
                ?book bk:has_seats ?seat.
                ?book bk:has_time ?time.
                OPTIONAL {?book bk:hasDietaryRequirement ?diet.
                          ?diet bk:hasName ?dname. }
                """
    if len(request.POST.keys()) > 1:
        if request.POST['booking_id'] != '':
            base_query = base_query+'\n        FILTER (?id = %s).' %request.POST['booking_id']

        if request.POST['booking_name'] != '':
            base_query = base_query+'\n        FILTER (regex(?name, "%s", "i")).' %request.POST['booking_name']

        if request.POST['diet_req'] != '':
            base_query = base_query+'\n        FILTER (regex(?dname, "%s", "i")).' %request.POST['diet_req']

        if request.POST['seats'] != '-1':
            base_query = base_query+'\n        FILTER (?seat = %s).' %request.POST['seats']

        if request.POST['date'] != '':
            base_query = base_query+'\n        FILTER (regex(str(?time), "%s", "i")).' %convert_date(request.POST['date'])

        base_query = base_query+"\n}"

        if 'order_by' in request.POST.keys():
            base_query = base_query+'\nORDER BY DESC(?time)'
    else:
        base_query = base_query+"\n}"

    return base_query



def menu_query_text(request):
    base_query = prefix() + """
        SELECT ?name
        (GROUP_CONCAT(DISTINCT ?ingredient_name; SEPARATOR=',') AS ?ingredients)
        ?cat_name
        (GROUP_CONCAT(DISTINCT ?diet; SEPARATOR=',') AS ?dietary)
        ?spiciness
        WHERE {
                ?item a ?m_item.
                ?m_item rdfs:subClassOf* bk:Menu_Item.
                ?item bk:has_name ?name.
                ?item bk:hasIngredient ?ingredient.
                ?ingredient bk:has_name ?ingredient_name.
                ?m_item rdfs:subClassOf ?category.
                ?category dc:title ?cat_name.
                ?item bk:satisfiesDietaryRequirement ?diet_req.
                ?diet_req bk:hasName ?diet.
                ?item bk:isSpicy ?spiciness.
                """

    if len(request.POST.keys()) > 1:
        if request.POST['options'] != '-1':
            base_query = base_query+'\n        FILTER (regex(?cat_name, "%s", "i")).' %request.POST['options']

        if request.POST['item_name'] != '':
            base_query = base_query+'\n        FILTER (regex(?name, "%s", "i")).' %request.POST['item_name']

        if request.POST['ingredient'] != '':
            base_query = base_query+'\n        FILTER (regex(?ingredient_name, "%s", "i")).' %request.POST['ingredient']

        if request.POST['diet_req'] != '':
            base_query = base_query+'\n        FILTER (regex(?diet, "%s", "i")).' %request.POST['diet_req']

        if request.POST['spicy'] != '':
            base_query = base_query+'\n        FILTER (regex(?spiciness, "%s", "i")).' %request.POST['spicy']

        base_query = base_query+"} \nGROUP BY ?name ?spiciness ?cat_name"

        if request.POST['orderby'] != '':
            base_query = base_query+'\nORDER BY %s(?%s)' % (request.POST['ASCDESC'], request.POST['orderby'])
    else:
        base_query = base_query+"\n} \nGROUP BY ?name ?spiciness ?cat_name"
    
    return base_query



def employee_query_text(request):
    base_query = prefix() + """
        SELECT ?id ?name (GROUP_CONCAT(?shiftname; SEPARATOR=',') AS ?shifts) ?work
        WHERE {
                ?emp a ?empo.
                ?empo rdfs:subClassOf* bk:Employee.
                ?emp bk:worksIn ?work_area.
                ?work_area bk:has_name ?work.
                ?emp bk:has_employeeName ?name.
                ?emp bk:has_employeeID ?id.
                ?emp bk:hasShift ?shift.
                ?shift bk:has_name ?shiftname.
                """
    if len(request.POST.keys()) > 1:
        if request.POST['employee_id'] != '':
            base_query = base_query+'\n        FILTER (?id = %s).' %request.POST['employee_id']

        if request.POST['employee_name'] != '':
            base_query = base_query+'\n        FILTER (regex(?name, "%s", "i")).' %request.POST['employee_name']

        if request.POST['shift'] != '':
            base_query = base_query+'\n        FILTER (regex(?shiftname, "%s", "i")).' %request.POST['shift']

        if request.POST['work_area'] != '':
            base_query = base_query+'\n        FILTER (regex(?work, "%s", "i")).' %request.POST['work_area']

        base_query = base_query+"\n} \nGROUP BY ?name ?id ?work"
    
    else:
        base_query = base_query+"\n} \nGROUP BY ?name ?id ?work"
    
    return base_query
            
    
 
