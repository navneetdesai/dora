from geopy import distance
from geopy.geocoders import Nominatim


class Geopy:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="dora")
        self.locators = {}

    def get_geocode(self, location) -> tuple[float, float]:
        return self.geolocator.geocode(location)

    def get_distance(self, loc1, loc2):
        loc1, loc2 = self.locators[loc1], self.locators[loc2]
        return distance.distance(loc1, loc2).km
