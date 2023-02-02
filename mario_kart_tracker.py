# Name: Vincent Gilliam
# Student Number: 5465483

from flask import Flask, request
from pyhtml import html, select, body, option, form, p, h1, label, input_, br,  head, link, style, img
import json
from operator import itemgetter

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def homepage():
    response = html(
        body(
            link(rel="stylesheet", href="static/mario_kart_style.css")
        ),
        body(
            h1("Welcome to MarioKart!"),      
            p("Please select your difficulty and vehicle type. The higher the cc, the faster the vehicles go."),    
        ),
        form(action="/display_results")(
            label("Difficulty: "),
            select(name = "cc_group")(
                option("50 cc"),
                option("100 cc"),
                option("150 cc"),
                option("200 cc"),
                option("Most Handling"),
                option("Most Weight"),
                option("Most Traction"),
                option("Most Mini-Turbo")
            ),
            br,br,
            label("Vehicle: "),
            select(name = "vehicle_group")(
                option("Kart"),
                option("Bycicle"),
                option("ATV"),
            ),
            br,br,
            input_(type="submit", name= "submit_btn", value = "Submit")
        )
    )
    return str(response)

@app.route('/display_results', methods=["POST"])
def display_results():
    if request.method == 'POST':
        if "submit_btn" in request.form:
            if request.form["cc_group"] != "" and request.form["vehicle_group"] != "":
                cc = request.form["cc_group"]
                vehicle = request.form["vehicle_group"]

    final_choice = determine_vehicle(cc, vehicle)


    response = html(
        body(
            link(rel="stylesheet", href="static/mario_kart_rec_style.css")
        ),
        h1("Results"),
        p("Difficulty Priorities: ", final_choice["Priorities"]),
        p("Vehicle: ", ', '.join(final_choice["Vehicle"])),
        p("Wheels: ", ', '.join(final_choice["Wheels"])),
        p("Glider: ",  ', '.join(final_choice["Glider"])),
        p("Characters: ", ', '.join(final_choice["Characters"])),
        p("Chose a ", vehicle),
        h1("Recommendation"),
        img(src=  FASTEST_BODY_IMAGE, id ="center"),
        img(src=  FASTEST_WHEEL_IMAGE, id = "center"),
        img(src= FASTEST_GLIDER_IMAGE, id = "center"),
        form(action='/')(
            input_(type='submit', value='Back')
        )
    )
    return str(response)

def determine_vehicle(cc, vehicle):
    vehicle_selection = {}
    # data from https://www.kaggle.com/datasets/barelydedicated/mariokart8?resource=download&select=tires.csv
    f = open("bodies.json")
    bodies_list = json.load(f)
    g = open("gliders.json")
    gliders_list = json.load(g)
    h = open("tires.json")
    wheels_list = json.load(h)
    i = open("characters.json")
    character_list = json.load(i)
    if cc == "50 cc":
        vehicle_selection["Priorities"] = "Speed"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Speed", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Speed")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Speed")
        vehicle_selection["Characters"] = character_list["Very Heavy"]

    elif cc == "100 cc":
        vehicle_selection["Priorities"] = "Speed"
        vehicle_selection["Vehicle"] =  sort_body(bodies_list, "Speed", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Speed")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Speed")
        vehicle_selection["Characters"] = character_list["Very Heavy"]

    elif cc == "150 cc":
        vehicle_selection["Priorities"] = "Speed and Handling"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Handling", vehicle)
        vehicle_selection["Wheels"] =  sort_wheels(wheels_list, "Speed")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Speed")
        vehicle_selection["Characters"] = character_list["Heavy"]
    elif cc == "200 cc":
        vehicle_selection["Priorities"] = "Handling and Acceleration"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Handling", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Acceleration")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Acceleration")
        vehicle_selection["Characters"] = character_list["Light"]
    elif cc == "Most Handling":
        vehicle_selection["Priorities"] = "Most Handling"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Handling", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Handling")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Acceleration")
        vehicle_selection["Characters"] = character_list["Light"]
    elif cc == "Most Weight":
        vehicle_selection["Priorities"] = "Most Weight"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Weight", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Weight")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Speed")
        vehicle_selection["Characters"] = character_list["Very Heavy"]
    elif cc == "Most Traction":
        vehicle_selection["Priorities"] = "Most Traction"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Traction", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Traction")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Speed")
        vehicle_selection["Characters"] = character_list["Medium"]
    elif cc == "Most Mini-Turbo":
        vehicle_selection["Priorities"] = "Most Mini-Turbo"
        vehicle_selection["Vehicle"] = sort_body(bodies_list, "Mini Turbo", vehicle)
        vehicle_selection["Wheels"] = sort_wheels(wheels_list, "Mini Turbo")
        vehicle_selection["Glider"] = sort_gliders(gliders_list, "Acceleration")
        vehicle_selection["Characters"] = character_list["Light"]
    return vehicle_selection
def sort_body(list, key, vehicle):
    fastest_three = []
    sorted_body = sorted(list, key=itemgetter(key), reverse=True) 
    image_found = False
    global FASTEST_BODY_IMAGE
    FASTEST_BODY_IMAGE = sorted_body[0]["image"]
    for dict in sorted_body:
        if len(fastest_three) == 3:
            return fastest_three
        if(dict["Type"] == vehicle):
            if not image_found:
                FASTEST_BODY_IMAGE = dict["image"]
                image_found = True
            fastest_three.append(dict["Vehicle"])
def sort_gliders(list, key):
    fastest_three = []
    image_found = False
    global FASTEST_GLIDER_IMAGE
    for dict in list:
        if len(fastest_three) == 3:
            return fastest_three
        if dict["Type"] == key:
            if not image_found:
                FASTEST_GLIDER_IMAGE = dict["image"]
                image_found = True
            fastest_three.append(dict["Body"])
    return fastest_three
def sort_wheels(list, key):
    fastest_three = []
    global FASTEST_WHEEL_IMAGE
    if key == "Weight":
        sorted_wheels = sorted(list, key=itemgetter(key), reverse=False) 
    else:
        sorted_wheels = sorted(list, key=itemgetter(key), reverse=True) 
    FASTEST_WHEEL_IMAGE = sorted_wheels[0]["image"]
    for dict in sorted_wheels:
        if len(fastest_three) == 3:
            return fastest_three
        fastest_three.append(dict["Body"])
    return fastest_three


if __name__ == "__main__":
    app.run(debug=True)