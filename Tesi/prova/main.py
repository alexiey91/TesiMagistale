try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
#twitter_stream = Twitter(auth=oauth)
#twitter_stream.search.tweets(result_type='recent', lang='en', count=10)

# Get a sample of the public data following through Twitter
#iterator = twitter_stream.statuses.sample()
iterator = twitter_stream.statuses.filter(track="#trump", language="en")
#iterator = twitter_stream.search.tweets(q='#trump',result_type='recent', lang='en')
#print json.dumps(iterator)
# Print each tweet in the stream to the screen
# Here we set it to stop after getting 1000 tweets.
# You don't have to set it to stop, but can continue running
# the Twitter API to collect data for days or even longer.
tweet_count = 100
for tweet in iterator:
    tweet_count -= 1
    #print tweet['statuses']
    # Twitter Python Tool wraps the data returned by Twitter
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print json.dumps(tweet)
      #file = json.loads(tweet.strip())
    if 'text' in tweet:  # only messages contains 'text' field is a tweet
         print tweet['id']  # This is the tweet's id
         print tweet['created_at']  # when the tweet posted
         print tweet['text']  # content of the tweet
    #
         print tweet['user']['id']  # id of the user who posted the tweet
         print tweet['user']['name']  # name of the user, e.g. "Wei Xu"
         print tweet['user']['screen_name']  # name of the user account, e.g. "cocoweixu"
    #
         hashtags = []
         for hashtag in tweet['entities']['hashtags']:
             hashtags.append(hashtag['text'])
         print hashtags

    print json.dumps(tweet, indent=4)

    if tweet_count <= 0:
        break