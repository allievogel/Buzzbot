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
brief1.append({"question":"Great to meet you! What is your email address?"})
brief1.append({"question":"We are excited to work with you. What is the name of the company you are working with?"})
brief1.append({"question":"Tell me a little bit about your project: What is the main objective?"})
brief1.append({"question":"Nice, I'm excited to get started. Now, who is your target audience?"})
brief1.append({"question":"We can target that audience. When are you looking to have this project completed by? Keep in mind that for most projects we need around a month to get it just right for you."})
brief1.append({"question":"Yes! We love working on these types of projects. What format are you looking to have this in?"})
brief1.append({"question":"Awesome. We are making note of that! Now let\'s get down to the details: can you describe your project\'s concept more in-depth?"})
# brief1.append({"question":"Noted! Is there anything specific you want to highlight?"})
brief1.append({"question":"Tell me about what you want your users to feel when they see your site?"})
# brief1.append({"question":"Voila! Which of these photos best resonates?"})
# brief1.append({"question":"Great. Now upload (by drag and dropping) any files you want to include for us?"})
brief1.append({"question":"We are really excited to speak with you! Now that we got know your needs a little better, let\'s schedule a time to discuss this brief. Please enter the date and time that works best for you?"})
brief1.append({"question":"We are all set to chat. You\'ll get an email confirmation for our appointment. Looking forward to it. Please click on the download button to the right to save your brief!"})

answerArr = ["objective","audience","timeline","format","concept","desc","feeling","schedule"]
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

    elif currentQuestion==3:
        print('updating answer table'+str(user_id))
        a=Answer(user_id=User.objects.get(pk=user_id),objective=msg)
        a.save()

    elif currentQuestion==4:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.audience = msg
        a.save()

    elif currentQuestion==5:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.timeline = msg
        a.save()
    elif currentQuestion==6:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.format= msg
        a.save()
    elif currentQuestion==7:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.concept=msg
        a.save()
        print('concept'+str(msg))

    elif currentQuestion == 8:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.desc = msg
        a.save()
        print('desc' + str(msg))

    elif currentQuestion == 9:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.feeling = msg
        a.save()
        print('feeling' + str(msg))
        print("current q:", currentQuestion)

    elif currentQuestion == 10:
        a = Answer.objects.get(user_id=User.objects.get(pk=user_id))
        a.schedule = msg
        a.save()
        print('schedule' + str(msg))


    print("current q:",currentQuestion)
    return HttpResponse(json.dumps({"msg": brief1[currentQuestion]["question"], "user_id":user_id}), content_type="application/json")



def your_name(command):
    #ORIGINAL!
    # if "name is" in command or your_name == "":
    if "name is" in command:

        info['your_name'] = command.split("name is ")[1].split(" ")[0]
    else:
        info['your_name'] = command
    return "Great to meet you, {}. Are you ready to get started? ".format(info['your_name'])


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

def brief(request):

    print("this is working")
    user_id = request.POST.get('user_id')
    print(user_id)
    # answers=Answer.objects.filter(user_id=User.objects.get(pk=user_id))
    answers=Answer.objects.filter(user_id=User.objects.get(pk=user_id)).values()[0]
    print("ans",answers)
    print("bre",brief1)

    return HttpResponse(json.dumps({'answers': answers},{'questions': brief1}), content_type="application/json")

    # return render(request,'index.html',{'answers':answers},{'questions':brief1})