var ChatBot = {};

//The server path will be used when sending the chat message to the server.
//todo replace with your server path if needed
ChatBot.DEFAULT_ANIMATION = "waiting";
//The animation timeout is used to cut the current running animations when a new animations starts
ChatBot.animationTimeout;
//Holds the speech synthesis configuration like language, pich and rate
ChatBot.speechConfig;
//Will be set to false automatically whan the browser does not support speech synthesis
//Or when the user clicks the mute button
ChatBot.speechEnabled = false;

ChatBot.currentQuestion = 0;
ChatBot.briefLength = 10;

//TODO: remove for production
ChatBot.debugMode = true;

//This function is called in the end of this file
ChatBot.start = function () {
    $(document).ready(function () {
        ChatBot.debugPrint("Document is ready");
        ChatBot.bindErrorHandlers();
        ChatBot.initSpeechConfig();
        ChatBot.bindUserActions();
        ChatBot.userId;
        ChatBot.write("Hello there! I’d love to chat with you about your creative brief. Let’s start with an introduction: My name is Buzz, what is your name?", "Buzzbot");
    });
};

//Handle Ajax Error, animation error and speech support
ChatBot.bindErrorHandlers = function () {
    //Handle ajax error, if the server is not found or experienced an error
    $(document).ajaxError(function (event, jqxhr, settings, thrownError) {
        ChatBot.handleServerError(thrownError);
    });

    //Making sure that we don't receive an animation that does not exist
    $("#emoji").error(function () {
        ChatBot.debugPrint("Failed to load animation: " + $("#emoji").attr("src"));
        ChatBot.setAnimation(ChatBot.DEFAULT_ANIMATION);
    });

    //Checking speech synthesis support
    if (typeof SpeechSynthesisUtterance == "undefined") {
        ChatBot.debugPrint("No speech synthesis support");
        ChatBot.speechEnabled = false;
        $("#mute-btn").hide();
    }
};

ChatBot.bindUserActions = function () {
    //Both the "Enter" key and clicking the "Send" button will send the user's message
    $('.chat-input').keypress(function (event) {
        if (event.keyCode == 13) {
            ChatBot.sendMessage();
        }
    });

    $(".send-button").unbind("click").bind("click", function (e) {
        ChatBot.sendMessage();
    });

    $("#downloadNow").bind("click", function (e) {
        console.log(ChatBot.userId)
        $.post("/brief", {"user_id":ChatBot.userId}, function (result) {
            console.log(result.answers);
            console.log(result.answers.objective);
            // $('#name').text(result.answers.user_name);
            // $('#email').text(result.answers.email);
            // $('#companyname').text(result.answers.company_name);
            $('#objective').text(result.answers.objective);
            $('#audience').text(result.answers.audience);
            $('#timeline').text(result.answers.timeline);
            $('#format').text(result.answers.format);
            $('#concept').text(result.answers.concept);
            $('#feeling').text(result.answers.feeling);
            $('#schedule').text(result.answers.schedule);


            audience=result.audience;
            concept=result.concept;

        })

    });
};


//Moving the progress bar forward with each question answered
ChatBot.move = function () {
    var elem = $("#myBar");
    var width = 1;
    var counter=0;
    var id = setInterval(frame, 10);

    function frame() {
        if (width >= 100) {
            clearInterval(id);
             // $('#percent').innerHTML=0;

        } else {
            width++;
            elem.style.width = width + '%';
            counter++;
        }
    }
};

//Moving percentage with animation

//  ChatBot.percentageCalc = function () {
//     var count = 0
//
//     $('#test').onclick = function perCent(){
//     var inp = document.getElementById("text").value;
//
//     if( inp === ""){
//     alert("You need some text");
//     return
//
// }
//     document.getElementById("percent").innerHTML ='';
//     count += 10;
//     document.getElementById("percent").innerHTML = count + "%";
//
//     if(count > 100)
//     document.getElementById("percent").innerHTML = 100 + "%";
// }
//  };

//  // getting percentage to move
//  ChatBot.modify_qty = function (val) {
//     var qty = $('#qty').value;
//     var new_qty = parseInt(qty,10) + val;
//
//     if (new_qty < 0) {
//         new_qty = 0;
//     }
//
//     $('#qty').value = new_qty;
//     return new_qty;
// };

//Initializeing HTML5 speech synthesis config
ChatBot.initSpeechConfig = function () {
    if (ChatBot.speechEnabled) {
        ChatBot.speechConfig = new SpeechSynthesisUtterance();
        ChatBot.speechConfig.lang = 'en-US';
        ChatBot.speechConfig.rate = 1.6;
        ChatBot.speechConfig.pitch = 5;
        ChatBot.speechConfig.onend = function (event) {
            $("#speak-indicator").addClass("hidden");
        }
    }
};

//The core function of the app, sends the user's line to the server and handling the response
ChatBot.sendMessage = function () {
    var sendBtn = $(".send-button");
    //Do not allow sending a new message while another is being processed
    if (!sendBtn.is(".loading")) {
        var chatInput = $(".chat-input");
        //Only if the user entered a value
        if (chatInput.val()) {
            sendBtn.addClass("loading");
            ChatBot.write(chatInput.val(), "me");
            //Sending the user line to the server using the POST method
            console.log('before post'+ChatBot.userId);
            $.post("/chat", {"msg": chatInput.val(),"question_num":ChatBot.currentQuestion,"user_id":ChatBot.userId}, function (result) {
                console.log(result);
                if (typeof result != "undefined" && "msg" in result) {
                    ChatBot.setAnimation(result.animation);
                    ChatBot.write(result.msg, "Buzzbot");
                    ChatBot.userId=result.user_id;
                    console.log('callback post'+ChatBot.userId)
                } else {
                    //The server did not erred but we got an empty result (handling as error)
                    ChatBot.handleServerError("No result");
                }
                ChatBot.currentQuestion++;
                console.log((parseFloat(ChatBot.currentQuestion) / parseFloat(ChatBot.briefLength) * 100) + "%")
                $("#myBar").width((parseFloat(ChatBot.currentQuestion) / parseFloat(ChatBot.briefLength) * 100) + "%")

                sendBtn.removeClass("loading");
            });
            chatInput.val("")
        }
    }
};



ChatBot.write = function (message, sender) {
    //Only boto's messages should be heard
    if (ChatBot.speechEnabled) {
        ChatBot.speak(message);
    }
    var image;
    if (sender == "Buzzbot"){
        image = '<div class = "buzzIcon"><img src="./static/images/buzzicon.png" height="64px" width="64px"></div>'
        var chatScreen = $(".chat-screen");
        chatScreen.scrollTop = chatScreen.scrollHeight;
        sender = $("<span />").addClass("sender").addClass(sender).html(image);
        var msgContent = $("<span />").addClass("msg").text(message);
        var newLine = $("<div />").addClass("msg-row Buzzbot").css({"background-color": "#74C8F3", "margin-bottom": "20px"});
        chatScreen.append(newLine);
        newLine.before(sender).append(msgContent);
    }else{
        image = '<div class = "allieIcon"></div><img src="./static/images/allieicon.png" height="64px" width="64px"></div>'
        var chatScreen = $(".chat-screen");
        sender = $("<span />").addClass("sender").addClass(sender).html(image);
        var msgContent = $("<span />").addClass("msg").text(message);
        var newLine = $("<div />").addClass("msg-row me").css({"background-color": "#ADDEF4", "margin-top": "15px"});
        chatScreen.append(newLine);
        newLine.before(sender).append(msgContent);
    }
};

//Setting boto's current animation according to the server response
ChatBot.setAnimation = function (animation) {
    $("#emoji").attr("src", "static/images/boto/" + animation + ".gif");
    //Cut the current running animations when a new animations starts
    clearTimeout(ChatBot.animationTimeout);
    //Each animation plays for 4.5 seconds
    ChatBot.animationTimeout = setTimeout(function () {
        $("#emoji").attr("src", "static/images/boto/" + ChatBot.DEFAULT_ANIMATION + ".gif")
    }, 4500);
};

ChatBot.speak = function (msg) {
    $("#speak-indicator").removeClass("hidden");
    try {
        ChatBot.speechConfig.text = msg;
        speechSynthesis.speak(ChatBot.speechConfig);
    } catch (e) {
        $("#speak-indicator").addClass("hidden");
    }
};

ChatBot.handleServerError = function (errorThrown) {
    ChatBot.debugPrint("Server Error: " + errorThrown);
    var actualError = "";
    if (ChatBot.debugMode) {
        actualError = " ( " + errorThrown + " ) ";
    }
    ChatBot.write("Sorry, there seems to be an error on the server. Let's talk later. " + actualError, "Buzzbot");
    ChatBot.setAnimation("giggling");
    $(".send-button").removeClass("loading");
};

ChatBot.debugPrint = function (msg) {
    if (ChatBot.debugMode) {
        console.log("CHATBOT DEBUG: " + msg)
    }
};

// trying to bring data from backend to frontend

// def brief (request):
//     user_id = request.POST.get('user_id')
//     # answers=Answer.objects.filter(user_id=User.objects.get(pk=user_id))
//     answers=Answer.objects.filter(user_id=user_id)
//
//     print(answers.values())
//
//     return render(request,'index.html',{'answers':answers},{'questions':brief1})

ChatBot.start();

//csrf cookie
//Ajax CSRF.

$(function() {

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


});



