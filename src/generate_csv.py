import datetime

from src import vote_getter


def _normalize_vote(vote):
  try:
    return {
      'yea': 'y',
      'nay': 'n',
      'not voting': 'a',
      'not guilty': 'ng',
      'guilty': 'g',
      'present': 'p',
      'present, giving live pair': 'pglp',
      'a': 'a'}[vote.strip().lower()]
  except KeyError:
    logging.warn('Unexpected vote value: ', vote)
    return vote


def csv_rows(first_date, last_date, roll_dir=None, vote_dir=None):

  d = {}
  votes = set()
  for vote in vote_getter.get_votes(
      first_date, last_date, roll_dir, vote_dir):
    vote_tuple = (
        vote.congress, vote.session, vote.vote_number,
        datetime.datetime.strptime(vote.vote_date, '%B %d, %Y,  %I:%M %p'),
        f'{vote.question}: {vote.vote_title}')
    votes.add(vote_tuple)
    for member in vote.members:
      member_tuple = (
          member.last_name, member.first_name, member.party, member.state)
      d.setdefault(member_tuple, {})[vote_tuple] = _normalize_vote(
          member.vote_cast)

  num_cols = (
      5 +  # Names, party affiliation, etc.
      3 * len(votes))
  votes = sorted(votes, key=lambda tup: tup[3])

  top_row = [''] * 5
  question_row = [''] * 5
  member_row = [''] * 5
  for _, _, _, date, question in votes:
    top_row.extend(['', datetime.datetime.strftime(date, '%m/%d/%y')])
    question_row.extend(['', question, ''])
    member_row.extend(
        ['y/n', 'Voted with party?', 'Voted with opposition?'])
  yield top_row
  yield question_row

  for _ in range(10):
    yield [''] * num_cols

  yield member_row

  for member_tuple, vote_dict in sorted(
      d.items(), key=lambda item: item[0][0]):
    last, first, party, state = member_tuple
    row = ['', '', state, f'{last}, {first}', party]
    for vote in votes:
      row.extend([vote_dict.get(vote, 'a'), '', ''])
    yield row
