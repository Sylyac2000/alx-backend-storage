#!/usr/bin/env python3
"""
a Python script that improve 12-log_stats.py
by adding the top 10 of the most present IPs in the collection nginx
of the database logs
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

    # Count top IPs
    print("IPs:")
    top_ips = collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in top_ips:
        count = ip.get("count")
        ip_address = ip.get("ip")
        print("\t{}: {}".format(ip_address, count))


if __name__ == "__main__":
    nginx_log_stats()
