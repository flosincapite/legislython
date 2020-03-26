import datetime
import os
from xml.etree import ElementTree

from src import config
from src import roll_getter
from src import utils
from src.objects import vote


def _votes_for_roll(
    first_date, last_date, roll, cache_directory=None):
  for the_vote in roll.votes:
    vote_date = datetime.datetime(
        year=int(roll.congress_year), month=the_vote.vote_month,
        day=the_vote.vote_day)
    if vote_date < first_date or vote_date >= last_date:
      continue

    if cache_directory is not None:
      fname = os.path.join(
          cache_directory,
          f'vote_{roll.congress_year}_{the_vote.vote_number}.xml')
      if not os.path.exists(fname):
        try:
          contents = utils.retrieve_vote(
              roll.congress, roll.session, the_vote.vote_number)

        # TODO: Handle GotRedirectedError.
        except utils.GotRedirectedError:
          raise
        with open(fname, 'w') as outp:
          outp.write(contents)

      yield vote.Vote.from_file(fname)

    else:
      contents = utils.retrieve_vote(
          roll.congress, roll.session, the_vote.vote_number)
      node = ElementTree.fromstring(contents)
      yield vote.Vote(node)


def get_votes(
    first_date, last_date, roll_dir=None, vote_dir=None):
  assert(first_date < last_date)

  # Determines congresses for the relevant years.
  first_congress = utils.congress_for_year(first_date.year)
  last_congress = utils.congress_for_year(last_date.year + 1)

  # Retrieves votes.
  for roll in roll_getter.get_rolls(first_congress, last_congress, roll_dir):
    for vote in _votes_for_roll(first_date, last_date, roll, vote_dir):
      yield vote
