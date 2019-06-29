import tweepy
import traceback
import time

owner = ""

def login():

    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def upload(text):
    api = login()
    try:
        output = text
        api.update_status(status=output)
    except:
        error_msg = traceback.format_exc().split("\n", 1)[1][-130:]
        api.send_direct_message(screen_name = owner, text = error_msg + " " + time.strftime("%H:%M:%S"))
