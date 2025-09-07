import discord, os, json, random, math
from datetime import datetime

def calculate_countdown(date):
    d = datetime.strptime(date, "%m/%d/%Y").timestamp()
    return math.floor(d)

def get_json():
    with open(os.getenv('JSON')) as json_data:
        d = json.load(json_data)
        return d

def get_member(index):
    response = ''
    for usernameSection in get_json()['memberList']['members'][index-1]['username']:
        response = response + usernameSection
    return response

def split_username(username):
    return list(filter(None, username.split("&")))

def random_color():
    colors = [discord.Colour.from_rgb(171, 171, 171), discord.Colour.from_rgb(138, 108, 196), discord.Colour.from_rgb(59, 118, 194)]
    return random.choice(colors)

