import requests
from Music import search_and_play
from speak import speech_play
from capture import get_base64
from api_keys import api_keys_rapid

def websearch(query):
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query":query,"limit":"3","related_keywords":"true"}
    headers = {
        "x-rapidapi-key": api_keys_rapid[0],
        "x-rapidapi-host": "google-search74.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

tools = [
    {
        "type": "function",
        "function": {
            "name": "websearch",
            "description": "Search the top 3 results from Google for a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to use for the web search."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_and_play",
            "description": "Searches for a song (e.g., on YouTube Music) and plays it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "The name of the song to search for and play. Including the artist can improve results."
                    }
                },
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "speech_play",
            "description": "Converts a given text into speech and plays it out loud. Use this to communicate responses or information to the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to be converted to speech. Should be plain text for best results."
                    }
                },
                "required": ["text"]
            }
        }
    },{
        "type":"function",
        "function":{
            "name":"capture_photo",
            "description":"opens camera and captures the photo",
            "parameters":{
                "type":"object",
                "properties":{
                    "text":{
                        
                    }
                }
            }
            
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_base64",
            "description": "Reads and returns a base64 encoded string of the last captured image from the file 'image.txt'. Returns None if the file does not exist.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

TOOL_MAPPING = {
    "websearch": websearch,
    "search_and_play": search_and_play,
    "speech_play": speech_play,
    "get_base64": get_base64
}