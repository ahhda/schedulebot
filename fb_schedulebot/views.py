# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, requests, random, re
from pprint import pprint
from models import *
# Create your views here.

#access token for chatbot testing
#access_token = 'EAABvEGv4tasBAJWr2P6Do5m0AobAbYBl3ArirGSEfrSQlY30rIc5dfi8vqVfzOJI1JmKFtsnDv1tPxRC3nc53xrgy6Hb3GknwNOkq6xd6RC7CExQpZB52q99Ud7JTCb0BDfPCVrSZATzFsrJTMhItL4hl6me79h5h3JiqbLgZDZD'
#access token for ok correct
access_token = 'EAACEZCP91xugBAHIl5cZBqVIMb95Kgyw6IWQhsa3XCBa66pnJo5igKLpZCpZAGZA9Uh3nw4NMbAyv0aZC4s12tvv6a6BhLkhQbyVd2VAbStJkbhy3kUG2GEtjJDzda9qt7nXUx0f8Udnu9E5DrpKAnnlQjLgXOPh3QBN5mvZBFj5AZDZD'


questions = ["""Question 1: Which food don’t you like? Why don’t you like it?
Listen: http://okcorrect.com/free/q1.mp3"""]

first_message = """Hello! Antes de empezar, solo necesito saber la dirección de email que utilizaste
para inscribir. ¿Cual es?"""

def send_message_generic(fbid, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+access_token
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def send_welcome_message(fbid):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+access_token
    message1 = """Gracias. La prueba gratis empieza hoy.

Antes de empezar, lee estas reglas y consejos:
http://immersoes.weebly.com/reglasyconsejos.html

Abajo tienes la primera pregunta. Escribe tu respuesta en inglés y la corregiré dentro de 24 horas."""
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message1}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def send_question(fbid, day):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+access_token
    message1 = questions[day]
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message1}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def new_user_messages(fbid):
    send_message_generic(fbid, first_message)

def message_received(fbid, received_message):           
    # post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+access_token
    # response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
    # status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # pprint(status.json())
    if fb_user.objects.filter(fb_id=fbid).exists():
        print "USER ALREADY EXISTS"
        c = fb_user.objects.get(fb_id=fbid)
        if received_message == "test1":
            send_message_generic(fbid, "Test Working")
        elif received_message == "restart":
            c.current_day = 0
            c.first_message = 0
            c.save()
            new_user_messages(fbid)
        elif c.first_message == 0:
            c.first_message = 1
            c.save()
            send_welcome_message(fbid)
            send_question(fbid, 0)
        # send_welcome_message(fbid)
        # send_question(fbid, 0)
    else:
        pprint("NEW USER")
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
        user_details_params = {'fields':'first_name,last_name', 'access_token':access_token}
        user_details = requests.get(user_details_url, params=user_details_params).json()
        pprint(user_details)
        first_name = user_details['first_name']
        last_name = user_details['last_name']
        print first_name, last_name, fbid
        new_user = fb_user(fb_id=fbid, first_name=first_name, last_name=last_name)
        new_user.save()
        new_user_messages(fbid)
        # send_welcome_message(fbid)
        # send_question(fbid, 0)

class ScheduleBotView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            if self.request.GET['hub.verify_token'] == 'this_is_the_password':
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')
        except:
            return HttpResponse('Error, invalid request')

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        print "INCOMING MESSAGE"
        # print incoming_message
        pprint(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message and 'text' in message['message']:
                    # Print the message to the terminal
                    print "MESSAGE"
                    pprint(message)
                    message_received(message['sender']['id'], message['message']['text'])
                else:
                    print "STICKER"
        return HttpResponse()
