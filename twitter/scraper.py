import tweepy
import json
import os
import re 
import geocoder

# https://developer.twitter.com/en/docs.html
# can use bounding box for location filtering 
# - POSTED from the webpage? 

def sign_in():
    """
    returns a reference to the authenticated api
    """
    auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
    auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_SECRET"))
    api = tweepy.API(auth)
    return api

def clean_text(text):
    patterns = [
        "((http(s)?(\:\/\/))+(www\.)?([\w\-\.\/])*(\.[a-zA-Z]{2,3}\/?))[^\s\b\n|]*[^.,;:\?\!\@\^\$ -]"
        , "#"
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)
    return text

def scrape(location="", topic="", limit=100):
    """
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    """
    # API.search(q[, geocode][, lang][, locale][, result_type][, count][, until][, since_id][, max_id][, include_entities])
    tweets = []
    if not location and not topic:
        return tweets
    api = sign_in()
    query       = topic
    osm_geocode = geocoder.osm(location).json
    geocode = str(osm_geocode["lat"]) + "," +str(osm_geocode["lng"]) + "," + "500km"
    lang        = "EN"
    locale      = ""
    count       = limit
    
    search_results = api.search(topic,lang=lang,count=count,geocode=geocode)
    for tweet in search_results:
        text = clean_text(tweet.text)
        if len(text)>0:
            print(text)
            tweets.append(text)
    return tweets

