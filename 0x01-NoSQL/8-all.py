#!/usr/bin/env python3
"""a Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """Lists all docs in a collection"""
    return [doc for doc in mongo_collection.find()]
