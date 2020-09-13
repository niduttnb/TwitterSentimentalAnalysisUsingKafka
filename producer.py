import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer

#Place your keys here
consumer_key    = ''
consumer_secret = ''
access_token    = ''
access_token_secret   = ''


producer = KafkaProducer(
bootstrap_servers='localhost:9092'
,value_serializer=lambda x: x.encode('utf-8')
) #Same port as your Kafka server


topic_name = "Twitter"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class Producer(StreamListener):

    def __init__(self, producer):
        self.producer = producer

    def on_data(self, data):
        self.producer.send(topic_name, value=data,partition=0)
        return True

    def on_error(self, error):
        print(error)

twitter_stream = Stream(auth, Producer(producer))
twitter_stream.filter(track=["Biden"])  #Stream tweets on Biden
 



                                                                                                                                                                                   
