#!/usr/bin/env python3
""" a python function that lists all documents in a collection"""
from pymongo import MongoClient


def list_all(mongo_collection):
    documents = list(mongo_collection.find())
    if len(documents) > 0:
        return documents
    else:
        return []
