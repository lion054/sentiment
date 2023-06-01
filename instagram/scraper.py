# Scraper for instagram 
# search for posts based on tags

import requests

def get_payload(url):
    r = requests.get(url=url)
    if r.status_code is not 200:
        raise Exception('Bad request. Error code: ' + r.status_code)
    return r.json()

# search instagram based on a tag and optionally a location
def search_tags(tag=""):
    captions = []
    if not tag:
        return captions

    data = get_payload('https://www.instagram.com/explore/tags/'+tag+'/?__a=1')
    try: 
        for media in data['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
            for caption in media['node']['edge_media_to_caption']['edges']:
                captions.append(caption['node']['text'])
    except Exception as e:
        print (e)
    return captions

# main scraper method for all social media platforms
def scraper(location="", topic="", limit=""):
    """
    Parameters:
    location : str
        filter by location
    topic : str
        filter by a topic/search term
    limit : int
        number of results to query
    """
    # currently can only filter by tags... 
    print(location + "||" + topic + "||")
    arr = search_tags(location)+ search_tags(topic)
    return arr
