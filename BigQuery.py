import os
import json
from google.cloud import bigquery
from pathlib import Path

class BigQuery :
  __table_id = ''
  __client = None

  def __init__ (self) :
    with open('./config/config.json') as json_string:
      config = json.load(json_string)
    self.__table_id = config['google']['bigquery']['tableId']

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(Path('./config/google_auth.json'))

  def auth (self) :
    self.__client = bigquery.Client()

  # https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.insert_rows_json
  def insert (self, data) :
    errors = self.__client.insert_rows_json(self.__table_id, data, row_ids=[None] * len(data))
    if errors == []:
      print('New rows have been added.')
    else:
      print('Encountered errors while inserting rows: {}'.format(errors))

  def getDF (self) :
    sql = """
      SELECT *
      FROM `{}`
    """.format(self.__table_id)

    df = self.__client.query(sql).to_dataframe()
    return df
