from kafka import KafkaConsumer
from kafka import TopicPartition
import json
from pymongo import MongoClient
import preprocessor as p



topic_name = 'Twitter'
client = MongoClient(port = 27017)
db = client.Twitter
table = db.TrumpvsBiden

def extract(message,partition):
    print(partition)
    if 'retweeted_status' in message:
        if 'extended_tweet' in message['retweeted_status']:

            try:
                tweetText=message['retweeted_status']['extended_tweet']['full_text']                

            except:
                try:
                    tweetText=message['retweeted_status']['text']
                    
                except:
                    print("Blank 1")
                    tweetText=''
    else:
        try:
            tweetText=message['extended_tweet']['full_text']
            
        except:
            try:
                tweetText=message['text']
                
            except:
                print("Blank 2")
                tweetText=''

    
    
    jsonText={}
    try:
        jsonText['text']=tweetText
    except:
        jsonText['text']=message['text']

    if partition ==0:
        jsonText['person']='B'
        
    else:
        jsonText['person']='T'
    
    try:
        x=table.insert_one(jsonText)

    except:
        print("Error while writing to mongoDB")

consumer = KafkaConsumer(
      topic_name,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='latest',
     enable_auto_commit=True,
     auto_commit_interval_ms =  5000,
     max_poll_records = 100,
     value_deserializer=lambda x: json.loads(x.decode('utf-8')))



for message in consumer:
    partition=message.partition
    message = message.value
    print(partition)
    extract(message,partition)
    

