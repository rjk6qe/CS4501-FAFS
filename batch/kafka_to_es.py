from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
from elasticsearch import Elasticsearch
import time
import json


es = Elasticsearch(['es'])
kafka_ready = False

# some_new_listing = {
#       "pk": 100,
#       "name":"Penguin",
#       "description":"forgive me.",
#       "category_id":"1",
#       "price":"40",
#       "owner_id":"1",
#       "time_posted":"2016-09-01T13:10:30+03:00",
#       "time_updated":"2016-09-19T13:20:30+03:00",
#       "pick_up":"canada",
#       "status":"N"
# }
#
#     index_status = es.index(index='listing_index', doc_type='listing', id=some_new_listing['pk'], body=some_new_listing)
#     es.indices.refresh(index="listing_index")

while not kafka_ready:
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        kafka_ready = True
    except NodeNotReadyError:
        time.sleep(5)
        # consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

while True:
    for message in consumer:
        kafka_object = json.loads((message.value).decode('utf-8'))
        index_status = es.index(index='listing_index', doc_type='listing', id=kafka_object['pk'], body=kafka_object)
        print(index_status)
        es.indices.refresh(index="listing_index")
