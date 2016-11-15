import json # python json package allows you to convert json objects to python dictionary format
import urllib
from collections import defaultdict

def customsearch(querry):
    results = []
    results_dict   = defaultdict(list)
    encoded = urllib.quote(querry)
    rawData = urllib.urlopen('https://www.googleapis.com/customsearch/v1?key=AIzaSyDthXFjwIaHm_SbjGjaqWthyVtvACbpxxY&cx=017576662512468239146:omuauf_lfve&q=' +encoded)
    data = json.load(rawData)

    length = len(data["items"])
    for i in range (5):

        results.append({
                        "title" : data["items"][i]["title"],
                        "url" : data["items"][i]["htmlFormattedUrl"]

        })

    return results
