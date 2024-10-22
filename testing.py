from polygon import RESTClient
import os
from dotenv import load_dotenv

load_dotenv()

client = RESTClient(os.getenv("POLYGON_API_KEY"))

aggs = client.get_aggs(
    "AAPL",
    1,
    "day",
    "2023-04-04",
    "2023-04-04",
)

# The aggregates get returned as Agg objects in a list -- here we only got one because that's what we specified
# (second parameter in the .get_aggs() method)

# Here's what it looks like

# aggs = [Agg(open=166.595, high=166.84, low=165.11, close=165.63, volume=46278295.0, 
#             vwap=165.9131, timestamp=1680580800000, transactions=456306, otc=None)]

# So, grab whichever aggregate you want and just use .open, .high ... to access whatever field you want
agg_obj = aggs[0]
print(agg_obj.open)

# Also, 2 years of historical data can be queried with the free version of Polygon, the database can be set up
# to store 2 years of info on whichever stocks are monitored if the data Polygon has is what is wanted
