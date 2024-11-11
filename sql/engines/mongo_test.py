# # -*- coding: UTF-8 -*-
# import re, time
# import pymongo
# import logging
# import traceback
# import subprocess
# # import simplejson as json
# import datetime
# import tempfile
# from bson.son import SON
# from bson import json_util
# from pymongo.errors import OperationFailure
# from dateutil.parser import parse
# from bson.objectid import ObjectId
# from bson.int64 import Int64
#
# # from . import EngineBase
# # from .models import ResultSet, ReviewSet, ReviewResult
# # from common.config import SysConfig
#
# logger = logging.getLogger("default")
#
# # mongo客户端安装在本机的位置
# mongo = "mongo"
#
# # conn = pymongo.MongoClient(
# #     'clusterphrisk0-shard-00-00.ljy3k.mongodb.net',
# #     27017,
# #     authSource='ph_risk',
# #     connect=True,
# #     connectTimeoutMS=10000,
# # )
# # conn['ph_risk'].authenticate('prod_ph_risk', 'ctqmHBHh8UxNcQof', 'ph_risk')
# #
# #
#
#
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
#
# uri = "mongodb+srv://prod_ph_risk:ctqmHBHh8UxNcQof@clusterphrisk0.ljy3k.mongodb.net/ph_risk?retryWrites=true&w=majority&appName=ClusterPhRisk0"
#
# auth_db = 'ph_risk'
#
# # Create a new client and connect to the server
# client = MongoClient(uri,
#                      connect=True,
#                      connectTimeoutMS=10000)
#
# # Send a ping to confirm a successful connection
# try:
#     # client.admin.command('ping')
#     # client.ph_risk.command('ping')
#     client['ph_risk'].command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
