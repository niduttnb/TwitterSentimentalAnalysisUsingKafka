import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer

consumer_key    = '8yFBpEhf7MiMktk2GNvthMNeM'
consumer_secret = 'VcYm394SGJIom1g0afKUuRQm8pR3kQqj0VRul7MLXkgXhu4v62'
access_token    = '2716416561-CxTXcX6a2J12WMbnUzRYCHpzM51QrWmhlEpvCTy'
access_token_secret   = 'WTPxMY3PijpM9sCZFp7VK3Pw9euJ0uDISlHaztfFI8cnv'


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
        self.producer.send(topic_name, value=data,partition=1)
        return True

    def on_error(self, error):
        print(error)

twitter_stream = Stream(auth, Producer(producer))
twitter_stream.filter(track=["Trump"])




                                                                                                                                                                                   