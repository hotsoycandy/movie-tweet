# external modules
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import tweepy

# internal modules
from Tweepy import Tweepy
from BigQuery import BigQuery

# load modules
bq = BigQuery()
bq.auth()
tw = Tweepy()
tw.auth()

def insert_tweet () :
  results = tw.search_as_pages('왓챠 OR 넷플릭스 OR 영화 OR 드라마', 5000)

  data = []
  for tweet in results.next() :
    data.append({
      'id': tweet.id,
      'text': tweet.text,
      'truncated': tweet.truncated,
      'source': tweet.source,
      'created_at': tweet.created_at.strftime("%Y-%m-%dT%H:%M:%S")
    })
    print(tweet.id)
    print(tweet.created_at)

  bq.insert(data)
  data = []

def tweet_to_wordcloud () :
  results = tw.search('왓챠 OR 넷플릭스 OR 영화 OR 드라마', 10)
  texts = []
  for tweets in results :
    for tweet in tweets :
      texts = texts + tweet.text.split()

  keywords = Counter(texts).most_common(50)
  keywords_dict = { }
  for keyword, freq in keywords :
    keywords_dict[keyword] = freq

  cloud = WordCloud(font_path='NanumGothic.ttf', width=600, height=600)
  image = cloud.generate_from_frequencies(keywords_dict).to_array()

  plt.figure()
  plt.imshow(image, interpolation='bilinear')
  plt.axis('off')
  plt.show()

def pickle_to_wordcloud () :
  df = pd.read_pickle("./tweets.pkl")
  keywords = Counter(" ".join(df["text"]).split()).most_common()
  print(keywords)
  keywords_dict = { }
  for keyword, freq in keywords :
    keywords_dict[keyword] = freq

  cloud = WordCloud(font_path='NanumGothic.ttf', width=1200, height=1200)
  image = cloud.generate_from_frequencies(keywords_dict).to_array()

  plt.figure()
  plt.imshow(image, interpolation='bilinear')
  plt.axis('off')
  plt.show()

def bigquery_save_as_pickle () :
  df = bq.getDF()
  df.to_pickle("./tweets.pkl")

def pickle_to_pie_chart () :
  df = pd.read_pickle("./tweets.pkl")

  source = df.groupby('source').size()
  source = pd.DataFrame({
    'size': source.values,
    'label': source.index.values
  })
  source.loc[source['size'] < 1000, ['label']] = 'etc'
  source = source.groupby('label').sum().sort_values(by='size', ascending=False)

  plt.pie(source['size'].values, startangle=90)
  plt.legend(
    labels=['%s, %1.1f %%' % (l, (s / source.sum() * 100)) for l, s in zip(source.index.values, source['size'].values)],
    loc="upper right"
  )
  plt.axis('equal')
  plt.title('Device chart', fontsize=20)
  plt.tight_layout()
  plt.show()

def pickle_analyze () :
  df = pd.read_pickle("./tweets.pkl")
  size = df.groupby('source').size()
  for index, value in size.iteritems() :
    print(index, value)
  print(size)
