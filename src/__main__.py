import csv
import datetime

from src import config
from src import generate_csv


def _get_datetime(date_expression, default_date):
  if date_expression is None:
    return default_date
  if isinstance(date_expression, int):
    date_expression = str(date_expression)
  if isinstance(date_expression, str):
    try:
      return datetime.datetime.strptime(date_expression, '%Y%m%d')
    except ValueError:
      raise ValueError('Date expressions should be like YYYYMMDD.')
  return date_expression


class SenateComponent(object):
  
  def populate_csv(
      self, output_csv, first_date=None, last_date=None, cache_rolls=True,
      cache_votes=True):

    first_date = _get_datetime(
        first_date, datetime.datetime(year=1989, month=1, day=1))
    last_date = _get_datetime(
        last_date, datetime.datetime.now() + datetime.timedelta(days=1))

    with open(output_csv, 'w') as outp:
      writer = csv.writer(outp)
      for row in generate_csv.csv_rows(
          first_date, last_date,
          config.ROLL_XML_DIR if cache_rolls else None,
          config.VOTE_XML_DIR if cache_votes else None):
        writer.writerow(row)


if __name__ == '__main__':
  import fire
  fire.Fire(SenateComponent)
