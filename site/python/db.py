import os
from pymongo import MongoClient
from test import mongodb


client = MongoClient(os.getenv(mongodb['str']))
cluster = client['Cluster0']
cpu = cluster['Cpu']
customerInfo = cluster['CustomerInfo']
gpu = cluster['Gpu']
mobo = cluster['Mobo']
orders = cluster['Orders']
ram = cluster['Ram']