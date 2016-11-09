from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
from elasticsearch import Elasticsearch
import time

kafka_ready = False

while not kafka_ready:
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        kafka_ready = True
    except NodeNotReadyError:
        time.sleep(5)

for message in consumer:
    kafka_object = json.loads((message.value).decode('utf-8'))
    index_status = es.index(index='listing_index', doc_type='listing', id=kakfa_object['pk'], body=kakfa_object)
    es.indices.refresh(index="listing_index")
