from pprint import pprint
from sqlalchemy import create_engine
import folium
import itertools
import json
import numpy as np
import pandas as pd
import random
import datetime
import pytz
dublin_timezone = pytz.timezone('Europe/Dublin')

# segment
Segment = [30*['Grocery'], 
           10*['Technology'], 
           15*['Apparel'], 
           45*['Restaurants']]
Segment = list(itertools.chain(*Segment))


# product category
product_category = {'Grocery': [
                        25*['Leafy Veggies'], 
                        10*['Fruits'], 
                        4*['Food Grains'], 
                        1*['Spices'], 
                        60*['Meat']
                    ],
                    'Technology': [
                        15*['Cell Phones'], 
                        27*['Laptops'],
                        40*['Home Appliances'], 
                        18*['Office Equipment']
                    ],
                    'Apparel': [
                        40*['Men'], 
                        40*['Women'], 
                        20*['Kids and Babies']
                    ],
                    'Restaurants': [
                        7*["Indian"], 
                        30*["Chinese"], 
                        20*["Korean"],
                        22*["Japanese"], 
                        10*["Mexican"]
                    ]
                   }
for item in product_category:
    product_category[item] = list(itertools.chain(*product_category[item]))


# sale value
sale_values = {'Grocery': {
                        'Leafy Veggies':random.randint(1, 13), 
                        'Fruits':random.randint(3, 10), 
                        'Food Grains':random.randint(1, 5), 
                        'Spices':random.randint(8, 30),
                        'Meat':random.randint(2, 20),
                        'Dairy':random.randint(5, 40),
                     },
                    'Technology': {
                        'Cell Phones':random.randint(150, 1200),
                        'Laptops':random.randint(450, 2000),
                        'Home Appliances':random.randint(10, 200),
                        'Office Equipment':random.randint(20, 1000),
                    },
                    'Restaurants': {
                        "Indian":random.randint(10, 40),
                        "Chinese":random.randint(8, 35),
                        "Korean":random.randint(12, 40),
                        "Japanese":random.randint(10, 50),
                        "Thai":random.randint(15, 50),
                        "Italian":random.randint(10, 30),
                        "Mexican":random.randint(8, 25),
                    },
                    'Apparel': {
                        'Men': random.normalvariate(40, 15), 
                        'Women':random.normalvariate(45, 30),
                        'Kids and Babies': random.normalvariate(30, 3), 
                    }
                }



# location
locations = pd.read_csv("../data/cork_locations.csv").sample(n=500).values.tolist()
print(locations[:10])
num_locations = len(locations)
loc_index = list(range(num_locations))
random.shuffle(loc_index)
location_type = {'Grocery': loc_index[: int(0.6*num_locations)],
                 'Apparel': loc_index[int(0.6*num_locations):int(0.65*num_locations)],
                 'Restaurants': loc_index[int(0.65*num_locations):int(0.80*num_locations)],
                 'Technology': loc_index[int(0.80*num_locations):],
                 
                }

# locations = pd.read_csv("../data/dublin_bike_stations.csv").values.tolist()
# num_locations = len(locations)
# loc_index = list(range(num_locations))
# random.shuffle(loc_index)
# location_type = {'Grocery': loc_index[: int(0.3*num_locations)],
#                  'Apparel': loc_index[int(0.3*num_locations):int(0.55*num_locations)],
#                  'Restaurants': loc_index[int(0.55*num_locations):int(0.80*num_locations)],
#                  'Technology': loc_index[int(0.80*num_locations):],
                 
#                 }


from faker import Faker
fake = Faker()
class StoreGenerator:
    def generate_data(self, time='realtime'):
        seg = random.choice(Segment)
        prd = random.choice(product_category[seg])
        sale = sale_values[seg][prd]
        lat, long = locations[random.choice(location_type[seg])]
        cash_or_card = random.choice(["cash", "card"])
        city="cork"
        
        if(time=='past'):
            timestamp = pd.Timestamp(fake.date_time_between(start_date="-45d", end_date="now", tzinfo=dublin_timezone))
        elif(time=='realtime'):
            timestamp = pd.Timestamp(datetime.datetime.now(), tz=dublin_timezone)
        

        
        return seg, prd, sale, lat, long, cash_or_card, timestamp, city
    
    def generate_data_json(self, time='past'):
        seg, prd, sale, lat, lon, cash_or_card, ts, city = self.generate_data(time)
        data = {
                     'segment': seg,
                     'product_category': prd,
                     'sale': sale,
                     'latitude': lat,
                     'longitude': lon,
                     'cash_or_card' : cash_or_card,
                     'timestamp': str(ts),
                     'city':city
                }
        # json_data = json.dumps(data, sort_keys=True)
        
        return data