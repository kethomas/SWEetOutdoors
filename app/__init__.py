"""
Main page for routing URL
"""
import os
import requests
from flask import Flask, render_template, request, jsonify
from models import db, State, Event, Campground, Park, app as application
from sqlalchemy import Table, or_, and_
import subprocess

# Actual Webpage Routings


@application.route("/")
def index():
    """
    routes to home page
    """
    return render_template('index.html')


@application.route("/about")
def about():
    """
    routes to about page
    """
    return render_template('about.html')

 # STATES-------------------------


@application.route("/states")
def states():
    """
    routes to states table page
    """
    states = State.query.all()
    return render_template('states.html', states=states)


@application.route("/states/<name>")
def state_instance(name):
    """
    routes to specific state page by name
    """
    state_instance = State.query.filter_by(name=name).first()
    return render_template('StateTemplate.html', state_instance=state_instance)

# PARKS-------------------------


@application.route("/parks", methods=['GET'])
def parks():
    """
    routes to parks table page
    """
    parks = Park.query.all()
    return render_template('parks.html', parks=parks)


@application.route("/parks/<idnum>")
def park_instance(idnum):
    """
    routes to specific park page by IDnum
    """
    park_instance = Park.query.filter_by(idnum=idnum).first()
    return render_template('ParksTemplate.html', park_instance=park_instance)

# Event----------------------------------


@application.route("/events")
def events():
    """
    routes to events table page
    """
    events = Event.query.all()
    return render_template('events.html', events=events)


@application.route("/events/<idnum>")
def event_instance(idnum):
    """
    routes to specific event page by IDnum
    """
    event_instance = Event.query.filter_by(idnum=idnum).first()
    return render_template('EventTemplate.html', event_instance=event_instance)

# Campgrounds-----------------------------------------


@application.route("/campgrounds")
def campgrounds():
    """
    routes to campgrounds table page
    """
    campgrounds = Campground.query.all()
    return render_template('campgrounds.html', campgrounds=campgrounds)


@application.route("/campgrounds/<idnum>")
def campground_instance(idnum):
    """
    routes to specific campground page by IDnum
    """
    campground_instance = Campground.query.filter_by(idnum=idnum).first()
    return render_template('CampgroundTemplate.html', campground_instance=campground_instance)


# Test routing-----------------------------------------

@application.route('/run_tests')
def tests():
    """
    show results of unit tests
    """
    return render_template("test_results.html")


# API calls-----------------------------------------

# Parks-----------------------------------------
@application.route('/api/parks')
def api_parks():
    """
    show list of parks in json format
    if state name is specified (format: /api/parks?state_name=<state_name>), list is filtered
    """
    park_lst = list()
    if 'state_name' in request.args:
        query_lst = Park.query.filter_by(
            state_fk=request.args['state_name']).all()
    else:
        query_lst = Park.query.all()

    for i in query_lst:
        dict_obj = {}
        dict_obj["ID"] = i.idnum
        dict_obj["Name"] = i.name
        dict_obj["Photo URL"] = i.photo_url
        park_lst += [dict_obj]
    return jsonify({"Success:": True, "List Of Parks": park_lst})


@application.route('/api/parks/<id>')
def api_park_details(id):
    """
    Show details of a park by ID
    """
    dict_obj = {}
    try:
        i = Park.query.filter_by(idnum=id).first()
        dict_obj["ID"] = i.idnum
        dict_obj["Name"] = i.name
        dict_obj["Latitude"] = i.latitude
        dict_obj["Longitude"] = i.longitude
        dict_obj["Address"] = i.address
        dict_obj["Phone"] = i.phone
        dict_obj["Rating"] = i.rating
        dict_obj["Website"] = i.website
        dict_obj["Zipcode"] = i.zipcode
        dict_obj["Zipcode Region"] = i.zipregion
        dict_obj["Photo URL"] = i.photo_url
        dict_obj["State"] = i.state_fk
    except AttributeError:
        return jsonify({"Success": False})
    return jsonify({"Details": dict_obj, "Success": True})

# States-----------------------------------------


@application.route('/api/states')
def api_states():
    """
    show list of states in json format
    """
    states_lst = list()
    for i in State.query.all():
        dict_obj = {}
        dict_obj["Name"] = i.name
        states_lst += [dict_obj]
    return jsonify({"Success:": True, "List Of States": states_lst})


@application.route('/api/states/<name>')
def api_state_detail(name):
    """
    show details of a specific state by name
    """
    dict_obj = {}
    try:
        i = State.query.filter_by(name=name).first()
        dict_obj["Name"] = i.name
        dict_obj["Description"] = i.description
        dict_obj["Total Area"] = i.total_area
        dict_obj["Population"] = i.population
        dict_obj["Highest Point"] = i.highest_point
        dict_obj["Map URL"] = i.url
    except AttributeError:
        return jsonify({"Success": False})
    return jsonify({"Details": dict_obj, "Success": True})

# Campgrounds-----------------------------------------


@application.route('/api/campgrounds')
def api_campgrounds():
    """
    show list of campgrounds in json format
    """
    camp_lst = list()
    for i in Campground.query.all():
        dict_obj = {}
        dict_obj["ID"] = i.idnum
        dict_obj["Name"] = i.name
        camp_lst += [dict_obj]
    return jsonify({"Success": True, "List Of Campgrounds": camp_lst})


@application.route('/api/campgrounds/<id>')
def api_campground_detail(id):
    """
    show details of a campground by id
    """
    dict_obj = {}
    try:
        i = Campground.query.filter_by(idnum=id).first()
        dict_obj["ID"] = i.idnum
        dict_obj["Name"] = i.name
        dict_obj["Description"] = i.description
        dict_obj["Latitude"] = i.latitude
        dict_obj["Longitude"] = i.longitude
        dict_obj["Direction"] = i.direction
        dict_obj["Phone"] = i.phone
        dict_obj["Email"] = i.email
        dict_obj["Zipcode"] = i.zipcode
        dict_obj["Park ID"] = i.park_fk
        dict_obj["State Name"] = i.state_fk
    except AttributeError:
        return jsonify({"Success": False})
    return jsonify({"Success": True, "Details": dict_obj})

# Events-----------------------------------------


@application.route('/api/events/')
def api_events():
    """
    give list of events in json format
    if park_id is given, list only returns events near that park
    if state_name is given, list only events in that state_instance
    """
    events_lst = list()
    if 'park_id' in request.args:
        query_lst = Event.query.filter_by(
            park_fk=request.args['park_id']).all()
    elif 'state_name' in request.args:
        query_lst = Event.query.filter_by(
            state_fk=request.args['state_name']).all()
    else:
        query_lst = Event.query.all()

    for i in query_lst:
        dict_obj = {}
        dict_obj["ID"] = i.idnum
        dict_obj["org_name"] = i.org_name
        dict_obj["Topics"] = i.topics
        dict_obj["Start Date"] = i.start_date
        events_lst += [dict_obj]
    return jsonify({"Success": True, "List Of Events": events_lst})


@application.route('/api/events/<id>')
def api_event_details(id):
    """
    give details of a specific event, by ID
    """
    dict_obj = {}
    try:
        i = Event.query.filter_by(idnum=id).first()
        dict_obj["ID"] = i.idnum
        dict_obj["Latitude"] = i.latitude
        dict_obj["Longitude"] = i.longitude
        dict_obj["Topics"] = i.topics
        dict_obj["Start Date"] = i.start_date
        dict_obj["End Date"] = i.end_date
        dict_obj["Pic URL"] = i.pic_url
        dict_obj["Name"] = i.org_name
        dict_obj["Phone"] = i.contact_phone_num
        dict_obj["Closest Park ID"] = i.park_fk
        dict_obj["State Name"] = i.state_fk
    except AttributeError:
        return jsonify({"Success": False})
    return jsonify({"Success": True, "Details": dict_obj})


@application.route('/search')
def search():
    """
    queries all models and returns matches in both AND and OR format
    """
    search_param = request.args['search']

    # create a list so Big Bend -> [ Big , Bend]
    descriptivename = search_param.split()

    events_or_list = set()
    states_or_list = set()
    campgrounds_or_list = set()
    parks_or_list = set()

    # keep a dictionary of each park that shows up in or search and count of other terms that show up
    # and list is found by filtering dictionary to only intances with the same count as number of search terms
    events_dict = {}
    states_dict = {}
    campgrounds_dict = {}
    parks_dict = {}

    # get or results
    for search in descriptivename:
        print(search)
        park_search_instance = Park.query.filter(or_(Park.name.ilike('%' + search + '%'), 
                                                     Park.latitude.ilike('%' + search + '%'), 
                                                     Park.longitude.ilike('%' + search + '%'), 
                                                     Park.address.ilike('%' + search + '%'), 
                                                     Park.phone.ilike('%' + search + '%'), 
                                                     Park.website.ilike('%' + search + '%'),
                                                     Park.zipcode.ilike('%' + search + '%'), 
                                                     Park.photo_url.ilike('%' + search + '%'), 
                                                     Park.zipregion.ilike('%' + search + '%'), 
                                                     Park.state_fk.ilike('%' + search + '%'))).all()
        for v in park_search_instance:
            parks_or_list.add(v)
            if v in parks_dict:
                parks_dict[v] += 1
            else:
                parks_dict[v] = 1


        event_search_instance = Event.query.filter(or_(Event.latitude.ilike('%' + search + '%'), 
                                                       Event.longitude.ilike('%' + search + '%'), 
                                                       Event.topics.ilike('%' + search + '%'), 
                                                       Event.start_date.ilike('%' + search + '%'), 
                                                       Event.end_date.ilike('%' + search + '%'), 
                                                       Event.pic_url.ilike('%' + search + '%'),
                                                       Event.org_name.ilike('%' + search + '%'), 
                                                       Event.contact_phone_num.ilike('%' + search + '%'), 
                                                       Event.zipregion.ilike('%' + search + '%'), 
                                                       Event.park_fk.ilike('%' + search + '%'), 
                                                       Event.state_fk.ilike('%' + search + '%'), 
                                                       Event.zipcode.ilike('%' + search + '%'))).all()
        for v in event_search_instance:
            events_or_list.add(v)
            if v in events_dict:
                events_dict[v] += 1
            else:
                events_dict[v] = 1


        state_search_instance = State.query.filter(or_(State.name.ilike(search), 
                                                       State.description.ilike('%' + search + '%'), 
                                                       State.total_area.ilike('%' + search + '%'), 
                                                       State.population.ilike('%' + search + '%'), 
                                                       State.highest_point.ilike('%' + search + '%'))).all()
        for v in state_search_instance:
            states_or_list.add(v)
            if v in states_dict:
                states_dict[v] += 1
            else:
                states_dict[v] = 1

        campground_search_instance = Campground.query.filter(or_(Campground.name.ilike('%' + search + '%'), 
                                                                 Campground.description.ilike('%' + search + '%'), 
                                                                 Campground.latitude.ilike('%' + search + '%'), 
                                                                 Campground.longitude.ilike('%' + search + '%'), 
                                                                 Campground.direction.ilike('%' + search + '%'),
                                                                 Campground.phone.ilike('%' + search + '%'), 
                                                                 Campground.email.ilike('%' + search + '%'), 
                                                                 Campground.zipcode.ilike('%' + search + '%'))).all()
        for v in campground_search_instance:
            campgrounds_or_list.add(v)
            if v in campgrounds_dict:
                campgrounds_dict[v] += 1
            else:
                campgrounds_dict[v] = 1

    finalparksand = set()

    # print(testparksand)
    for key in testparksand:
        if testparksand[key] == len(descriptivename):
            finalparksand.add(key)
    # print("finalparksand")
    # print(finalparksand)

    # and search, parks
    parkstate = and_(*[Park.state_fk.ilike('%' + s + '%') for s in descriptivename])
    parkurl = and_(*[Park.photo_url.ilike('%' + s + '%') for s in descriptivename])
    parkzipreg = and_(*[Park.zipregion.ilike('%' + s + '%') for s in descriptivename])
    parkzipcode = and_(*[Park.zipcode.ilike('%' + s + '%') for s in descriptivename])
    parkname = and_(*[Park.name.ilike('%' + s + '%') for s in descriptivename])
    parklat = and_(*[Park.latitude.ilike('%' + s + '%') for s in descriptivename])
    parklong = and_(*[Park.longitude.ilike('%' + s + '%') for s in descriptivename])
    parkaddress = and_(*[Park.address.ilike('%' + s + '%') for s in descriptivename])
    parkweb = and_(*[Park.website.ilike('%' + s + '%') for s in descriptivename])

    parksand = set(Park.query.filter(parkname).all() +
                   Park.query.filter(parkurl).all() +
                   Park.query.filter(parkzipreg).all() +
                   Park.query.filter(parkstate).all() +
                   Park.query.filter(parkzipcode).all() +
                   Park.query.filter(parklat).all() +
                   Park.query.filter(parklong).all() +
                   Park.query.filter(parkaddress).all() +
                   Park.query.filter(parkweb).all())
    # print(parksand)

    # and search, states
    stpop = and_(*[State.population.ilike('%' + s + '%') for s in descriptivename])
    sthigh = and_(*[State.highest_point.ilike('%' + s + '%') for s in descriptivename])
    starea = and_(*[State.total_area.ilike('%' + s + '%')  for s in descriptivename])
    stdesc = and_(*[State.description.ilike('%' + s + '%')  for s in descriptivename])
    stname = and_(*[State.name.ilike('%' + s + '%') for s in descriptivename])

    stateand = set(State.query.filter(stpop).all() +
                   State.query.filter(sthigh).all() +
                   State.query.filter(starea).all() +
                   State.query.filter(stdesc).all() +
                   State.query.filter(stname).all())

    # and search, events
    eventlat = and_(*[Event.latitude.ilike('%' + s + '%') for s in descriptivename])
    eventlong = and_(*[Event.longitude.ilike('%' + s + '%') for s in descriptivename])
    eventtopics = and_(*[Event.topics.ilike('%' + s + '%') for s in descriptivename])
    eventstart = and_(*[Event.start_date.ilike('%' + s + '%') for s in descriptivename])
    eventend = and_(*[Event.end_date.ilike('%' + s + '%') for s in descriptivename])
    eventpic = and_(*[Event.pic_url.ilike('%' + s + '%') for s in descriptivename])
    eventorg = and_(*[Event.org_name.ilike('%' + s + '%') for s in descriptivename])
    eventphone = and_(*[Event.contact_phone_num.ilike('%' + s + '%') for s in descriptivename])
    eventzipreg = and_(*[Event.zipregion.ilike('%' + s + '%') for s in descriptivename])
    eventzipcode = and_(*[Event.zipcode.ilike('%' + s + '%') for s in descriptivename])
    
    eventsand = set(Event.query.filter(eventlat).all() + 
                    Event.query.filter(eventlong).all() + 
                    Event.query.filter(eventtopics).all() + 
                    Event.query.filter(eventstart).all() + 
                    Event.query.filter(eventend).all() + 
                    Event.query.filter(eventpic).all() + 
                    Event.query.filter(eventorg).all() + 
                    Event.query.filter(eventphone).all() + 
                    Event.query.filter(eventzipreg).all() + 
                    Event.query.filter(eventzipcode).all())
    print("eventsand")
    print(eventsand)
    finaleventsand = set()
    for key in testeventsand:
        if testeventsand[key] == len(descriptivename):
            finaleventsand.add(key)
    print("finaleventsand")
    print(finaleventsand)

    # and search, campgrounds
    campname = and_(*[Campground.name.ilike('%' + s + '%') for s in descriptivename])
    campdescript = and_(*[Campground.description.ilike('%' + s + '%') for s in descriptivename])
    camplat = and_(*[Campground.latitude.ilike('%' + s + '%') for s in descriptivename])
    camplong = and_(*[Campground.longitude.ilike('%' + s + '%')  for s in descriptivename])
    campdirect = and_(*[Campground.direction.ilike('%' + s + '%')  for s in descriptivename])
    campphone = and_(*[Campground.phone.ilike('%' + s + '%') for s in descriptivename])
    campemail = and_(*[Campground.email.ilike('%' + s + '%')  for s in descriptivename])
    campzip = and_(*[Campground.zipcode.ilike('%' + s + '%') for s in descriptivename])

    campsand = set(Campground.query.filter(campname).all() +
                   Campground.query.filter(campdescript).all() +
                   Campground.query.filter(camplat).all() +
                   Campground.query.filter(camplong).all() +
                   Campground.query.filter(campdirect).all() +
                   Campground.query.filter(campphone).all() +
                   Campground.query.filter(campemail).all() +
                   Campground.query.filter(campzip).all())


    return render_template('Search.html', events_or_list=events_or_list, states_or_list=states_or_list, campgrounds_or_list=campgrounds_or_list, parks_or_list=parks_or_list, parksandlist=parksand, statesandlist=stateand, campgroundsandlist=campsand, search=search_param)

    #print("before the or code")
    # print parks_or_list
    # print events_or_list
    # print states_or_list
    # print campgrounds_or_list


@application.route('/visualization')
def visualization():
    """
    route to the visualization page for PartyPeople's API
    """
    return render_template('visualization.html')

if __name__ == '__main__':
    """
    main method to run program
    """
    application.debug = True
    application.run(threaded=True)
