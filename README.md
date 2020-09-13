# TwitterSentimentalAnalysisUsingKafka
I used Kafka to stream twitter data and see who is leading the Twitter Battle between Trump and Biden on Twitter using Sentimental Analysis

Tools needed:
(i) Apache/Confluent Kafka
(ii) Python
(iii) Twitter Account
(iv) MongoDB

Setup to be done before you run the code
(i) Create a developer account on Twitter and get consumer_key ,consumer_secret_key,access_token ,access_token_secret
(ii) Download Apache/Confluent Kafka and create a topic named 'Twitter' with 2 partition.
(iii) Setup a mongoDB replica set with one primary and one seconday node (This is needed as MongoDB Change Stream works only on a replica set): https://www.youtube.com/watch?time_continue=3&v=bJo7nr9xdrQ&feature=emb_logo
(iv) Download these python packages primarily: Flair, Tweepy, Pytorch ,Pymongo, Matplotlib and preprocessor

Steps:
1) Start the mongoDB replica set server with atleast 2 nodes- one primary and one seconday
2) Run the Kafka Server
3) Run the following python code in this order:
  (i) producer.py : This will start streaming tweets from twitter on Biden and produce it in Partition 0 of Kafka Topic - 'Twitter'
  (ii) producer2.py : This will start streaming tweets from twitter on Trump and produce it in Partition 1 of Kafka Topic - 'Twitter'
  (iii) consumer.py : Here the consumer will listen to inserts in both the partitions and will extract the entire tweet (extended_tweet) if the tweet size>140 characters. Later the consumer will push the tweet  along with the label -'B' or 'T' to indicate who is the tweet about to a MongoDB collection
  (iv) StreanMongoDB.ipyn: This will create a change Stream that will listen to all the new documents(tweets) being created in the collection. Then it will perform sentimental analysis on each tweet using Flair(DistilledBERT) and then see is the tweet in favor of Trump, Biden or is neutral. Later on it will plot a pie chart to depict the result with each incoming tweet
