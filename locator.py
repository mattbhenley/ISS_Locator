#!/bin/python3

import datetime
import json
import threading
import time
import turtle
import sys

from urllib import request
from collections import namedtuple



class ISS():

    def __init__(self):
        self.is_instance = True
        self._astronauts_url = 'http://api.open-notify.org/astros.json'
        self._location_url = 'http://api.open-notify.org/iss-now.json'
        self._location_tuple = namedtuple(
            'Location', ['latitude', 'longitude'])
        self._location()

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        self.is_instance = False

    def __repr__(self):
        return (f'{self.__class__.__name__}:\n\tTimestamp:{self._update_timestamp}\n\tLocation:{self.location}\n\tPeople: {self.people_in_space}')

    def _get_page(self, url):
        response = request.urlopen(url)
        result = json.loads(response.read())
        return result

    def _location(self):
        result = self._get_page(self._location_url)
        self.location = self._location_tuple(result['iss_position']['latitude'],
                                             result['iss_position']['longitude'])
        self._update_timestamp = result['timestamp']

    @property
    def people_in_space(self):
        result = self._get_page(self._astronauts_url)
        return [people['name'] for people in result['people']]


class Tracker(ISS):

    def __init__(self):
        super().__init__()
        self._bgpic = 'images/map.gif'
        self._shape = 'images/iss2.gif'

        self._screen = turtle.Screen()
        self._screen.title('Python ISS Tracker')
        self._screen.setup(width=720, height=360)
        self._screen.setworldcoordinates(-180, -90, 180, 90)
        self._screen.bgpic(self._bgpic)
        self._screen.register_shape(self._shape)
        self._screen.onscreenclick(self.update_turtle_location, btn=1)

        self._tracker = turtle.Turtle()
        self._tracker.shape(self._shape)
        self._tracker.setheading(90)

    def update_turtle_location(self, *args):
        self._location()
        self._tracker.penup()
        self._tracker.goto(float(self.location[0]), float(self.location[1]))
        # Debug
        print(self.__repr__())


if __name__ == '__main__':

    try:
        with Tracker() as iss:
            iss.update_turtle_location()
        turtle.mainloop()

    except KeyboardInterrupt:
        sys.exit(0)



# # http://open-notify.org/Open-Notify-API/
# url = 'http://api.open-notify.org/astros.json'
# response = urllib.request.urlopen(url)
# result = json.loads(response.read())

# print('People in Space: ', result['number'])

# people = result['people']

# for p in people:
#   print(p['name'], ' in ', p['craft'])


# url = 'http://api.open-notify.org/iss-now.json'
# response = urllib.request.urlopen(url)
# result = json.loads(response.read())

# location = result['iss_position']
# lat = float(location['latitude'])
# lon = float(location['longitude'])
# print('Latitude: ', lat)
# print('Longitude: ', lon)

# screen = turtle.Screen()
# screen.setup(720, 360)
# screen.setworldcoordinates(-180, -90, 180, 90)
# screen.bgpic('map.gif')


# screen = turtle.Screen()
# screen.setup(720, 360)
# screen.setworldcoordinates(-180, -90, 180, 90)
# # image source:
# # map.jpg: http://visibleearth.nasa.gov/view.php?id=57752 Credit: NASA
# screen.bgpic('map.gif')

# screen.register_shape('iss2.gif')
# iss = turtle.Turtle()
# iss.shape('iss2.gif')
# iss.setheading(90)

# iss.penup()
# iss.goto(lon, lat)

# # When Does ISS next pass over me?
# #london
# #lat = 51.5072
# #lon = 0.1275

# # Tokyo
# #lat = 35.689487
# #lon = 139.691706

# # Space Center, Houston
# lat = 29.5502
# lon = -95.097

# location = turtle.Turtle()
# location.penup()
# location.color('yellow')
# location.goto(lon, lat)
# location.dot(5)
# location.hideturtle()

# url = 'http://api.open-notify.org/iss-pass.json?lat=' + \
#     str(lat) + '&lon=' + str(lon)
# response = urllib.request.urlopen(url)
# result = json.loads(response.read())

# #print result
# over = result['response'][1]['risetime']
# location.write(time.ctime(over))
