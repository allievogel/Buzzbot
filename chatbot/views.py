from django.shortcuts import render
from django.http import HttpResponse
import json, random
import requests
import datetime
from .models import User, Answer

friends = []
info = {"first_message": False,
        "your_name": ""}

counter = 0
current_user = ""
name = ""
answer3 = ""

brief1 = []
brief1.append({"question":"Great! What is your email address?"})
brief1.append({"question":"Great! We are excited to work with you. What is the name of the company you are working with?"})
brief1.append({"question":"Tell me a little bit about your project: What is the main objective?"})
brief1.append({"question":"Nice, I'm excited to get started. Now, who is your target audience?"})
brief1.append({"question":"When are you looking to have this project completed by? Keep in mind that for most projects we need around a month to get it just right for you."})
brief1.append({"question":"Cool. Can\'t wait to work together. Let\'s speak about your project type:"})
brief1.append({"question":"Yes! We love working on ... What format are you looking to have this in?"})
brief1.append({"question":"Awesome. We are making note of that! Now let\'s get down to the details: can you describe your project\'s concept more in-depth?"})
brief1.append({"question":"Noted! Is there anything specific you want to highlight?"})
brief1.append({"question":"Tell me about what you want your users to feel when they see your site?"})
brief1.append({"question":"Voila! Which of these photos best resonates?"})
brief1.append({"question":"Great. Now upload (by drag and dropping) any files you want to include for us?"})
brief1.append({"question":"We are really excited to speak with you! Now that we got know your needs a little better, let\'s schedule a time to discuss this brief."})
brief1.append({"question":"We are all set to chat. You\'ll get an email confirmation for our appointment to connect at ... Looking forward to it."})

def index(request):
    your_name("")
    return render (request, 'index.html')



def chat (request):
    msg = request.POST.get('msg').lower()
    user_id=request.POST.get('user_id')
    currentQuestion = int(request.POST.get('question_num'))
    if currentQuestion == 0:
        u = User(user_name=msg)
        u.save()
        user_id = u.id
        print("firsttime"+str(user_id))
    elif currentQuestion == 1:
        print("second time"+str(user_id))
        u=User.objects.get(pk=user_id)
        u.email=msg
        u.save()

    elif currentQuestion == 2:
        u = User.objects.get(pk=user_id)
        u.company_name=msg
        u.save()

    return HttpResponse(json.dumps({"msg": brief1[currentQuestion]["question"], "user_id":user_id}), content_type="application/json")

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

def get_email(command):
    return "Yallah, let's go. What's your email address?"

def respond_email(command):
    return "Great! We are excited to work with you. What is the name of the company you are working with?"

def your_name(command):
    #ORIGINAL!
    # if "name is" in command or your_name == "":
    if "name is" in command:

        info['your_name'] = command.split("name is ")[1].split(" ")[0]
    else:
        info['your_name'] = command
    return "Great to meet you, {}. Are you ready to get started? ".format(info['your_name'])



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

    {
        "words": ["yes", "ready", "yallah"],
        "handler": get_email,
        "animation": "ok"
    },

    {
        "words": ["@"],
        "handler": respond_email,
        "animation": "ok"
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

    return "Hmmm, I'm not that smart of a robot yet. Let's try again!", "confused"
