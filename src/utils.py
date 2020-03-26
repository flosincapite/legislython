import logging
import re
from urllib import request

from src import config
from src import congress


class GotRedirectedError(Exception):
  pass


class NoXmlError(Exception):
  pass


def _sneaky_get(url):
  agent = config.AGENT
  host = 'www.senate.gov'
  the_request = request.Request(
      url, headers={'User-Agent': agent, 'Host': host}, method='GET')
  response = request.urlopen(the_request)
  # Redirects to
  # https://www.senate.gov/pagelayout/general/one_item_and_teasers/file_not_found.htm
  if re.search(r'file_not_found', response.url):
      raise _NoXmlError(
          f'No XML available for {congress}.')

  # We didn't fool senate.gov into thinking we were a browser :(.
  if not response.url.endswith('.xml'):
      raise _GotRedirectedError('The Senate is on to us.')
      
  return response.read().decode('utf8')


def retrieve_roll(congress, session):
  congress = '{:0>3}'.format(congress)
  session = '{:0>1}'.format(session)
  url = (
      'https://senate.gov/legislative/LIS/roll_call_lists/vote_menu_'
      f'{congress}_{session}.xml')
  return _sneaky_get(url)


def retrieve_vote(congress, session, vote):
  congress = '{:0>3}'.format(congress)
  session = '{:0>1}'.format(session)
  vote = '{:0>5}'.format(vote)
  url = (
      'https://www.senate.gov/legislative/LIS/roll_call_votes/'
      f'vote{congress}{session}/vote_{congress}_{session}_{vote}.xml')
  return _sneaky_get(url)


def congress_for_year(year):
  assert(year >= 1989)
  diff = year - 1989
  congress_number = 101 + int(diff / 2)
  congress_session = (diff % 2) + 1
  return congress.Congress(congress_number, congress_session)
