from pydantic import BaseModel
from pymongo import MongoClient

import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

client = MongoClient("mongodb+srv://ndongo:a9125844@cluster0.583znhe.mongodb.net/?retryWrites=true&w=majority")
db = client.Cluster0
collection = db.get_collection("users")
