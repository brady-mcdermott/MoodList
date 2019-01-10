import urllib3
import facebook
import requests
import spotipy
import random
import os
import sys
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials

cid = "Enter Spotify Developer CID here"
secret = "Enter Spotify Developer Secret CID here"
username = "Enter Username here"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-library-read playlist-modify playlist-read-private'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

#Facebook stuff
facebookToken = 'Enter FacebookAPI Access Token here'
graph = facebook.GraphAPI(access_token=facebookToken, version = 2.12)
profile = graph.get_object(id='me', fields='id,name', limit=100)
posts = graph.get_connections(profile['id'], connection_name='posts', fields='caption,message,object_id')
recent_post = posts['data'][0]['message']

# Check if sentence is happy or sad

print("Most Recent FaceBook Post: " + recent_post)

newString = ''
happyList = ['absolutely', 'accepted', 'acclaimed', 'accomplish', 'accomplished', 'accomplishment', 'achievement', 'action', 'active', 'admire', 'adorable', 'adventure', 'affirmative', 'affluent', 'agree', 'agreeable', 'amazing', 'angelic', 'appealing', 'approve', 'aptitude', 'attractive', 'awesome', 'beaming', 'beautiful', 'believe', 'beneficial', 'bliss', 'bountiful', 'bounty', 'brave', 'bravo', 'brilliant', 'bubbly', 'calm', 'celebrated', 'certain', 'champ', 'champion', 'charming', 'cheery', 'choice', 'classic', 'classical', 'clean', 'commend', 'composed', 'congratulation', 'constant', 'cool', 'courageous', 'creative', 'cute', 'dazzling', 'delight', 'delightful', 'distinguished', 'divine', 'earnest', 'easy', 'ecstatic', 'effective', ' effervescent', 'efficient', 'effortless', 'electrifying', 'elegant', 'enchanting', 'encouraging', 'endorsed', 'energetic', 'energized', 'engaging', 'enthusiastic', 'essential', 'esteemed', 'ethical', 'excellent', 'exciting', 'exquisite', 'fabulous', 'fair', 'familiar', 'famous', 'fantastic', 'favorable', 'fetching', 'fine', 'fitting', 'flourishing', 'fortunate', 'free', 'fresh', 'friendly', 'fun', 'funny', 'generous', 'genius', 'genuine', 'giving', 'glamorous', 'glowing', 'good', 'gorgeous', 'graceful', 'great', 'green', 'grin', 'growing', 'handsome', 'happy', 'harmonious', 'healing', 'healthy', 'hearty', 'heavenly', 'honest', 'honorable', 'honored', 'hug', 'idea', 'ideal', 'imaginative', 'imagine', 'impressive', 'independent', 'innovate', 'innovative', 'instant', 'instantaneous', 'instinctive', 'intellectual', 'intelligent', 'intuitive', 'inventive', 'jovial', 'joy', 'jubilant', 'keen', 'kind', 'knowing', 'knowledgeable', 'laugh', 'learned', 'legendary', 'light', 'lively', 'lovely', 'lucid', 'lucky', 'luminous', 'marvelous', 'masterful', 'meaningful', 'merit', 'meritorious', 'miraculous', 'motivating', 'moving', 'natural', 'nice', 'novel', 'now', 'nurturing', 'nutritious', 'okay', 'one', 'one-hundred percent', 'open', 'optimistic', 'paradise', 'perfect', 'phenomenal', 'pleasant', 'pleasurable', 'plentiful', 'poised', 'polished', 'popular', 'positive', 'powerful', 'prepared', 'pretty', 'principled', 'productive', 'progress', 'prominent', 'protected', 'proud', 'quality', 'quick', 'quiet', 'ready', 'reassuring', 'refined', 'refreshing', 'rejoice', 'reliable', 'remarkable', 'resounding', 'respected', 'restored', 'reward', 'rewarding', 'right', 'robust', 'safe', 'satisfactory', 'secure', 'seemly', 'simple', 'skilled', 'skillful', 'smile', 'soulful', 'sparkling', 'special', 'spirited', 'spiritual', 'stirring', 'stunning', 'stupendous', 'success', 'successful', 'sunny', 'super', 'superb', 'supporting', 'surprising', 'terrific', 'thorough', 'thrilling', 'thriving', 'tops', 'tranquil', 'transformative', 'transforming', 'trusting', 'truthful', 'unreal', 'unwavering', 'up', 'upbeat', 'upright', 'upstanding', 'valued', 'vibrant', 'victorious', 'victory', 'vigorous', 'virtuous', 'vital', 'vivacious', 'wealthy', 'welcome', 'well', 'whole', 'wholesome', 'willing', 'wonderful', 'wondrous', 'worty', 'wow', 'yes', 'yummy', 'zeal', 'zealous']

sadList = ['abysmal', 'adverse', 'alarming', 'angry', 'annoy', 'anxious', 'apathy', 'appalling', 'atrocious', 'awful', 'bad', 'banal', 'barbed', 'belligerent', 'bemoan', 'beneath', 'boring', 'broken', 'callous', 'can\'t', 'clumsy', 'coarse', 'cold', 'cold-hearted', 'collapse', 'confused', 'contradictory', 'contrary', 'corrosive', 'corrupt', 'crazy', 'creepy', 'criminal', 'cruel', 'cry', 'cutting', 'damage', 'damaging', 'dastardly', 'dead', 'decaying', 'deformed', 'deny', 'deplorable', 'depressed', 'deprived', 'despicable', 'detrimental', 'dirty', 'disease', 'disgusting', 'disheveled', 'dishonest','dishonorable', 'dismay', 'dismal', 'distress', 'don\'t', 'dreadful', 'dreary', 'enraged', 'eroding', 'evil', 'fail', 'faulty', 'fear', 'feeble', 'fight', 'filthy', 'foul', 'frighten', 'frightful', 'gawky', 'ghastly', 'grave', 'greed', 'grim', 'grimace', 'gross', 'grotesque', 'gruesome', 'guilty', 'haggard', 'hard', 'hard-hearted', 'harmful', 'hate', 'hideous', 'homely', 'horrendous', 'horrible', 'hostile', 'hurt', 'hurtful', 'icky', 'ignorant', 'ignore', 'ill', 'immature', 'imperfect', 'impossible', 'inane', 'inelegant', 'infernal', 'injure', 'injurious', 'insane', 'insidious', 'insipid', 'jealous', 'junky', 'lose', 'lousy', 'lumpy', 'malicious', 'mean', 'menacing', 'messy', 'misshapen', 'missing', 'misunderstood', 'moan', 'moldy', 'monstrous', 'naive', 'nasty', 'naughty', 'negate', 'negative', 'never', 'no', 'nobody', 'nondescript', 'nonsense', 'not', 'noxious', 'objectionable', 'odious', 'offensive', 'old', 'oppressive', 'pain', 'perturb', 'pessimistic', 'petty', 'plain', 'poor', 'prejudice', 'questionable', 'quirky', 'quit', 'reject', 'renege', 'repellant', 'reptilian', 'repugnant', 'repulsive', 'revenge', 'revolting', 'rocky', 'rotten', 'rude', 'ruthless', 'sad', 'savage', 'scare', 'scary', 'scream', 'severe', 'shocking', 'shoddy', 'sick', 'sickening', 'sinister', 'slimy', 'smelly', 'sobbing', 'sorry', 'spiteful', 'sticky', 'stinky', 'stormy', 'stressful', 'stuck', 'stupid', 'substandard', 'suspect', 'suspicious', 'tired', 'tense', 'terrible', 'terrifying', 'threatening', 'ugly', 'undermine', 'unfair', 'unfavorable', 'unhappy', 'unhealthy', 'unjust', 'unlucky', 'unpleasant', 'unsatisfactory', 'unsightly', 'untoward', 'unwanted', 'unwelcome', 'unwholesome', 'unwieldy', 'unwise', 'upset', 'vice', 'vicious', 'vile', 'villainous', 'vindictive', 'wary', 'weary', 'woeful', 'worthless', 'wound', 'yell', 'yucky', 'zero', 'depressing']
BLANK = ' '
i = 0
j = 0
happyScore = 0
sadScore = 0
l = list(recent_post)
while(i < len(l)):
    if(not l[i].isalpha() and not l[i] == BLANK):
        del l[i]
        newString += BLANK
    else:
        newString += l[i]
    i += 1
newString = newString.lower()
i = 0
if(not newString[len(newString) - 1] == ' '):
    newString += ' '
while(i < len(newString)):
    word = newString[i : newString.find(BLANK)]
#    print(newString)
#    print(word)
    newString = newString[newString.find(BLANK) + 1 : len(newString)]
    while(j < len(happyList)):
        if(word == happyList[j]):
            happyScore += 1
        j += 1
    j = 0
    while(j < len(sadList)):
        if(word == sadList[j]):
            sadScore += 1
        j += 1
    j = 0


#Weather data
api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=***Enter City that you live in here***'

url = api_address

json_data = requests.get(url).json()
formatted_data = json_data['weather'] [0] ['description']
print()
print ("The weather right now is: " + formatted_data)

if(formatted_data == "clear sky" or "few clouds"):
    happyScore+=1
    print("Seems like good weather!")

if(formatted_data == "light rain"):
    sadScore+=1
    print("No one likes a rainy day :(")

print()
print("Happy Score: " + str(happyScore))
print("Sad Score: " + str(sadScore))

# Add songs from Happy Playlist to Today's playlist

if(happyScore > sadScore):
    sourcePlaylist = sp.user_playlist(username, "spotify:user:casey727:playlist:6M4ZbVjkSE6P3IhbeYbnhc") #Happy playlist
    tracks = sourcePlaylist["tracks"]
    songs = tracks["items"]
    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks["items"]:
            songs.append(item)
        ids = []
#    print(len(songs))
#    print(songs[0]['track']['id'])

    i = random.randint(0,len(songs))
    sp.user_playlist_add_tracks(username, "Enter Personal Spotify Playlist CID here", [songs[i]["track"]["id"]]) #today's playlist

## Add songs from Sad playlist to Today's Playlist

if(sadScore > happyScore):
    sourcePlaylist = sp.user_playlist(username, "spotify:user:httpblue_:playlist:7po73ySk4MLa832Lqmmyjf") #sad playlist
    tracks = sourcePlaylist["tracks"]
    songs = tracks["items"]
    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks["items"]:
            songs.append(item)
        ids = []
#    print(len(songs))
#    print(songs[0]['track']['id'])

    i = random.randint(0,len(songs))
    sp.user_playlist_add_tracks(username, "Enter Personal Spotify Playlist CID here", [songs[i]["track"]["id"]]) #todays playlist

    print()
    print("Enjoy your songs for today!")
