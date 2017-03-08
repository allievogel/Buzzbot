from django.shortcuts import render
import json, random

def index(request):

    return render (request, 'index.html')

def test(request):
    msg = request.POST.get('msg')
    return json.dumps(msg)


def chat(request):
    user_message = request.POST.get('msg')
    response_message, boto_animation = message_key(user_message)[0], message_key(user_message)[1]
    return json.dumps({"animation": boto_animation, "msg": response_message})

def message_key(message):
        lowercase_message = message.lower()
        positive_greeting = ['happy', 'great', 'excited', 'good', 'nice', 'ok', 'amazing', 'best']
        bad_word = ['fuck', 'shit', 'bitch', 'hate', 'slut']
        negative_greeting = ['sad', 'tired', 'exhausted', 'sleepy', 'bad', 'angry', 'upset']
        hello_greeting = ['welcome', 'meet', 'salut', 'hi', 'hello' 'good morning', 'good evening', 'good night',
                          'greetings']
        people_name = ['allie', 'Allie', 'nathalie', 'Nathalie', 'giddeon', 'Giddeon', 'olivia', 'Olivia', 'arie',
                       'Arie', 'david', 'David']
        questions = {'how old are you': 'it is one of the grand mysteries of life',
                     'how are you': 'you know, I have been better. Thanks for your concern',
                     'where is': 'i suggest you ask that you check a map. I am no cartographer',
                     'language do you speak': 'i speak english, some french, and little Hebrew. But you can speak to me in English. And you?',
                     'your name': 'my name is boto, the best chatbot in the world'}

        for word in lowercase_message.split():

            if word in bad_word:
                return bad_word_response()

            elif word in positive_greeting:
                return positive_greeting_response()


            elif word in negative_greeting:
                return negative_greeting_response()

            elif word in hello_greeting:
                return hello_user()

            elif word in people_name:
                return people_name_response()

        if lowercase_message in questions:
            return (questions[lowercase_message], "dancing")
        return ('I did not understand the question, can you ask it again', "no")

def bad_word_response():
    return ("Get those bad words out of here", 'laughing')

def positive_greeting_response():
    return ("I am so happy to hear that. Ask me any questions...", 'dancing')

def negative_greeting_response():
    return ("Sorry to hear you are in a bad mood", 'crying')

def hello_user():
    greeting_chatbot = ['Excited to speak with you, I am here to answer questions','Hey you! Ask any question you like','Hey. Excited to get to know you. Please, ask a question!']
    chatbot_response = random.choice(greeting_chatbot)
    return (chatbot_response, 'dancing')

def people_name_response():
    return ("Great to hear from you. How are you feeling today?", 'excited')