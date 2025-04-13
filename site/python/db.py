import os
from pymongo import MongoClient
from test import mongodb


client = MongoClient(os.getenv(mongodb['str']))
cluster = client['Cluster0']
user = cluster['']