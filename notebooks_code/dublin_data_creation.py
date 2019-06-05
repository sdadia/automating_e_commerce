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
Segment = [10*['Grocery'], 
           40*['Technology'], 
           25*['Apparel'], 
           25*['Restaurants']]
Segment = list(itertools.chain(*Segment))


# product category
product_category = {'Grocery': [
                        40*['Leafy Veggies'], 
                        20*['Fruits'], 
                        5*['Food Grains'], 
                        5*['Spices'], 
                        30*['Meat']
                    ],
                    'Technology': [
                        48*['Cell Phones'], 
                        32*['Laptops'],
                        5*['Home Appliances'], 
                        15*['Office Equipment']
                    ],
                    'Apparel': [
                        26*['Men'], 
                        47*['Women'], 
                        27*['Kids and Babies']
                    ],
                    'Restaurants': [
                        48*["Indian"], 
                        21*["Chinese"], 
                        15*["Korean"],
                        5*["Japanese"], 
                        26*["Mexican"]
                    ]
                   }
for item in product_category:
    product_category[item] = list(itertools.chain(*product_category[item]))


# sale value
sale_values = {'Grocery': {
                        'Leafy Veggies':random.randint(1, 20), 
                        'Fruits':random.randint(3, 10), 
                        'Food Grains':random.randint(4, 10), 
                        'Spices':random.randint(8, 30),
                        'Meat':random.randint(2, 20),
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
                        'Men': random.normalvariate(80, 15), 
                        'Women':random.normalvariate(100, 30),
                        'Kids and Babies': random.normalvariate(15, 3), 
                    }
                }



# location
locations = pd.read_csv("../data/dublin_bike_stations.csv").values.tolist()
num_locations = len(locations)
loc_index = list(range(num_locations))
random.shuffle(loc_index)
location_type = {'Grocery': loc_index[: int(0.3*num_locations)],
                 'Apparel': loc_index[int(0.3*num_locations):int(0.55*num_locations)],
                 'Restaurants': loc_index[int(0.55*num_locations):int(0.80*num_locations)],
                 'Technology': loc_index[int(0.80*num_locations):],
                 
                }


# In[15]:


from faker import Faker

fake = Faker()

class StoreGenerator:
    def generate_data(self, time='realtime'):
        seg = random.choice(Segment)
        prd = random.choice(product_category[seg])
        sale = sale_values[seg][prd]
        lat, long = locations[random.choice(location_type[seg])]
        cash_or_card = random.choice(["cash", "card"])
        city="Dublin"
        
        if(time=='past'):
            timestamp = pd.Timestamp(fake.date_time_between(start_date="-20d", end_date="now", tzinfo=dublin_timezone))
        elif(time=='realtime'):
            timestamp = pd.Timestamp(datetime.datetime.now(), tz=dublin_timezone)
        
        return seg, prd, sale, lat, long, cash_or_card, timestamp, city
    
    def generate_data_json(self):
        seg, prd, sale, lat, long, cash_or_card, ts, city = self.generate_data()
        data = {
                     'segment': seg,
                     'product_category': prd,
                     'sale': sale,
                     'latitude': lat,
                     'longitude': long,
                     'cash_or_card' : cash_or_card,
                     'timestamp': str(ts),
                     'city': city
                }
        # json_data = json.dumps(data, sort_keys=True)
        
        return data