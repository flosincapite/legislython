import re

from xml.etree import ElementTree


class RollVote(object):

  def __init__(self, xml_tree):
    assert(xml_tree.tag == 'vote')
    for field in [
        'vote_number', 'vote_date', 'issue', 'question', 'result', 'title']:
      node = xml_tree.find(field)
      if node is None:
        text = ''
      else:
        text = node.text
      setattr(self, '_' + field, text)
    tally_node = xml_tree.find('vote_tally')
    for field in ['yeas', 'nays']:
      text = ''
      if tally_node is not None:
        node = tally_node.find(field)
        if node is not None:
          text = node.text
      setattr(self, '_' + field, text)

    # Derived properties.
    self._vote_month = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }[re.search(r'\-(.*)', self._vote_date).groups()[0].lower()]
    self._vote_day = int(re.search(r'^\d*', self._vote_date).group())

  @property
  def vote_month(self):
    return self._vote_month

  @vote_month.setter
  def vote_month(self, value):
    self._vote_month = value

  @property
  def vote_day(self):
    return self._vote_day

  @vote_day.setter
  def vote_day(self, value):
    self._vote_day = value

  @property
  def vote_number(self):
    return self._vote_number

  @vote_number.setter
  def vote_number(self, value):
    self._vote_number = value

  @property
  def vote_date(self):
    return self._vote_date

  @vote_date.setter
  def vote_date(self, value):
    self._vote_date = value

  @property
  def issue(self):
    return self._issue

  @issue.setter
  def issue(self, value):
    self._issue = value

  @property
  def question(self):
    return self._question

  @question.setter
  def question(self, value):
    self._question = value

  @property
  def result(self):
    return self._result

  @result.setter
  def result(self, value):
    self._result = value

  @property
  def title(self):
    return self._title

  @title.setter
  def title(self, value):
    self._title = value

  @property
  def yeas(self):
    return self._yeas

  @yeas.setter
  def yeas(self, value):
    self._yeas = value

  @property
  def nays(self):
    return self._nays

  @nays.setter
  def nays(self, value):
    self._nays = value

  def __eq__(self, other_roll_vote):
    for attr in [
        'vote_number', 'vote_date', 'issue', 'question', 'result', 'title', 
        'yeas', 'nays']:
      if getattr(self, attr) != getattr(other_roll_vote, attr):
        return False
    return True

  def __hash__(self):
    return hash(([
        getattr(self, attr) for attr in [
            'vote_number', 'vote_date', 'issue', 'question', 'result', 'title', 
            'yeas', 'nays']]))


class Roll(object):

  def __init__(self, xml_tree):
    assert(xml_tree.tag == 'vote_summary')
    self._congress = xml_tree.find('congress').text
    self._session = xml_tree.find('session').text
    self._congress_year = xml_tree.find('congress_year').text
    self._votes = [
        RollVote(vote) for vote in xml_tree.find('votes').findall('vote')]

  @property
  def congress(self):
    return self._congress

  @congress.setter
  def congress(self, value):
    self._congress = value

  @property
  def session(self):
    return self._session

  @session.setter
  def session(self, value):
    self._session = value

  @property
  def congress_year(self):
    return self._congress_year

  @congress_year.setter
  def congress_year(self, value):
    self._congress_year = value

  @property
  def votes(self):
    return self._votes

  @votes.setter
  def votes(self, value):
    self._votes = value

  @classmethod
  def from_file(cls, file_name):
    tree = ElementTree.ElementTree().parse(file_name)
    return cls(tree)
