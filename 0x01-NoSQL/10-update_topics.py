#!/usr/bin/env python3
"""a Python function that changes all topics of a school document
based on the name
"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """Change school topics"""
    mongo_collection.update_many(
        {"name": name}, {"$set": {"topics": topics}}
    )
