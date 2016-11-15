import json # python json package allows you to convert json objects to python dictionary format
import urllib
from collections import defaultdict

def customsearch(querry):
    results_dict   = defaultdict(list)
    encoded = urllib.quote(querry)
    rawData = urllib.open('https://www.googleapis.com/customsearch/v1?key=AIzaSyDthXFjwIaHm_SbjGjaqWthyVtvACbpxxY&cx=017576662512468239146:omuauf_lfve&q=' +encoded)
    data = json.load(rawData)

    length = len(data["items"])
    for i in range (length):
        results_dict[i].append(data["items"][i]["title"])
        results_dict[i].append(data["items"][i]["htmlFormattedUrl"])

    return results_dict
        
