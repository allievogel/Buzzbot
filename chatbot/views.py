from django.shortcuts import render
from django.http import HttpResponse
import json, random
import requests
import datetime

friends = []
info = {"first_message": False,
        "your_name": ""}

def index(request):
    your_name("")
    return render (request, 'index.html')

# def chat(request):
#     user_message = request.POST.get('msg')
#     msg, animation = analyze_command(user_message)
#     return HttpResponse(json.dumps({"animation": animation, "msg": msg}), content_type="application/json")

def chat(request):
    user_message = request.POST.get('msg').lower()
    msg, animation = analyze_command(user_message)
    return HttpResponse(json.dumps({"animation": animation, "msg": msg}), content_type="application/json")




def get_weather(command):
    if "in" not in command:
        return "Please repeat the question, and mention the city!"
    city = command.split("in ")[1].split("?")[0]
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=40badce35dd91ee9ddb8bac02e3e6967".format(city)
    response = requests.get(url)
    data = response.json()
    print(data)
    return "Right now in {} I see...{}".format(city, data["weather"][0]["description"])


def curse(command):
    return "I'm a gentle robot! don't curse!"


def love_dogs(command):
    return "I love dogs so much! Please change the code and add a dog for me!"


def distracted(command):
    return "Oops, what did you ask me to do? I got too afraid when you talked about Dana!"


def how_much_money(command):
    return "I have 50 million shekels!"


def my_name(command):
    return "My name is boto, weren't you listening?"


def beam_up(command):
    return "I just can't do it Captain, I just don't have the power!"


def your_name(command):
    #ORIGINAL!
    # if "name is" in command or your_name == "":
    if "name is" in command:

        info['your_name'] = command.split("name is ")[1].split(" ")[0]
    else:
        info['your_name'] = command
    return "Nice to meet you, {}".format(info['your_name'])


def what_time(command):
    return 'The {} is {:%H:%M}.'.format("time", datetime.datetime.now())


def add_friends(command):
    friends.append(command.split("add ")[1].split(" ")[0])
    return "No problem, added new friend!"


def who_are_friends(command):
    friends_set = set(friends)
    if friends_set:
        if len(friends_set) > 1:
            return "Right now all my friends are {}".format(" and ".join(friends_set))
        else:
            return "Right now my only friend is {}".format(list(friends_set)[0])
    return "I don't have any friends!"




any_terms = [
    {
        "words": ["fuck", "shit", "hell", "bitch", "freaking"],
        "handler": curse,
        "animation": "no"

    },
    {
        "words": ["dana"],
        "handler": distracted,
        "animation": "afraid"
    },
    {
        "words": ["dog", "dogs"],
        "handler": love_dogs,
        "animation": "dog"
    },
]
all_terms = [
    {
        "words": ["much", "money"],
        "handler": how_much_money,
        "animation": "money"
    },
    {
        "words": ["my", "name", "is"],
        "handler": your_name,
        "animation": "inlove"
    },
    {
        "words": ["what", "your", "name"],
        "handler": my_name,
        "animation": "giggling"
    },
    {
        "words": ["what", "time"],
        "handler": what_time,
        "animation": "waiting"
    },
    {
        "words": ["add", "friends"],
        "handler": add_friends,
        "animation": "excited"
    },
    {
        "words": ["who", "friends"],
        "handler": who_are_friends,
        "animation": "laughing"
    },
    {
        "words": ["beam", "me","up"],
        "handler": beam_up,
        "animation": "no"
    },
    {
        "words": ["how", "weather"],
        "handler": get_weather,
        "animation": "ok"
    },
    {
        "words": ["what", "weather"],
        "handler": get_weather,
        "animation": "ok"
    },
]


def analyze_command(command):
    for term in any_terms:
        if any(x in command for x in term["words"]):
            return term["handler"](command), term["animation"]
    for term in all_terms:
        if all(x in command for x in term["words"]):
            return term["handler"](command), term["animation"]

    if info["your_name"] == "":
        info["first_message"] = True
        your_name(command)
        print(info['your_name'])



        return your_name(command), "dancing"

    return "Sorry, I'm not sure what you mean by that", "confused"
