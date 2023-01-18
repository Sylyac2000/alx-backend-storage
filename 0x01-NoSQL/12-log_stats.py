#!/usr/bin/env python3
"""
a Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_log_stats():
    """Change school topics"""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    # Count all documents
    total_logs = collection.count_documents({})
    print(str(total_logs) + " logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod " + method + ": " + str(count))
    # Count status check
    count_status = collection.count_documents({"method": "GET",
                                              "path": "/status"})
    print(str(count_status) + " status check")


if __name__ == "__main__":
    nginx_log_stats()
