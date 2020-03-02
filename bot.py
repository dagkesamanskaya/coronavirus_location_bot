from geopy.distance import geodesic
from datetime import date
import pandas as pd
from geopy.distance import geodesic
from telegram.ext import Updater, MessageHandler, Filters
from telegram import InputLocationMessageContent
from telegram import Location

today = date.today()
updater = Updater(token='1009750191:AAH7nqI4_6sDuPLAQvROeXFlV7VPeJeTTfw', use_context=True)

dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!\n\nSend me your location to find the closest coronavirus spot on "+str(today))

def closest (coordinates, set_of_coordinates):
    curr = set_of_coordinates[0]
    for index in range (len (set_of_coordinates)):
        if geodesic(coordinates, set_of_coordinates[index]).kilometers < geodesic(coordinates, curr).kilometers:
            curr = set_of_coordinates[index]
    return curr, geodesic(coordinates,curr).kilometers

def get_location(day, month, year, user_location_lat, user_location_long):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    df = pd.read_csv(url, error_bad_lines=False)
    coordinates = df[['Lat','Long']]
    tuples = [tuple(x) for x in coordinates.to_numpy()]
    closest_dot = closest((user_location_lat, user_location_long), tuples)
    place = df.loc[(df['Lat'] == 53.7098) & (df['Long'] == 27.9534)]
    country = place['Country/Region'].to_numpy()[0]
    return country, int(closest_dot[1])

def location(update, context):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)
    country_distance = get_location(today.day, today.month,today.year, message.location.latitude, message.location.longitude)
    context.bot.send_message(chat_id=update.effective_chat.id, text='The closest infected spot of coronavirus is\n\n in '+country_distance[0]+' '+str(country_distance[1])+' kilometers away')

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(location_handler)
updater.start_polling()