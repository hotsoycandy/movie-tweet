import json
import tweepy

class Tweepy :
  # check real tweet url
  # https://twitter.com/twitter/status/1234903157580296192

  # tweet object document
  # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

  __consumer_key = ''
  __consumer_secret = ''
  __access_token = ''
  __access_token_secret = ''
  __api = None

  def __init__ (self) :
    with open('./config/config.json') as json_string:
      config = json.load(json_string)

    self.__consumer_key = config['tweepy']['consumer_key']
    self.__consumer_secret = config['tweepy']['consumer_secret']
    self.__access_token = config['tweepy']['access_token']
    self.__access_token_secret = config['tweepy']['access_token_secret']

  def auth (self) :
    auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret)
    auth.set_access_token(self.__access_token, self.__access_token_secret)
    self.__api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

  # https://docs.tweepy.org/en/latest/api.html#API.search
  def search (self, searchQuery, count) :
    public_tweets = self.__api.search(q=searchQuery, count=count, lang='ko')
    return public_tweets

  def search_as_pages (self, searchQuery, count) :
    public_tweets = tweepy.Cursor(
      self.__api.search,
      q=searchQuery,
      count=100,
      lang='ko',
      result_type='recent',
      max_id='1352800928957534207'
    ).pages(count)

    return public_tweets
