import logging

from xml.etree import ElementTree

from src.objects import member


class Document(object):

  def __init__(self, xml_tree):
    if xml_tree is not None:
      assert(xml_tree.tag == 'document')
    for field in [
        'document_type', 'document_number', 'document_name',
        'document_title', 'document_short_title']:
      try:
        setattr(self, '_' + field, xml_tree.find(field).text)
      except AttributeError:
        setattr(self, '_' + field, '')

  @property
  def document_type(self):
    return self._document_type

  @document_type.setter
  def document_type(self, value):
    self._document_type = value

  @property
  def document_number(self):
    return self._document_number

  @document_number.setter
  def document_number(self, value):
    self._document_number = value

  @property
  def document_name(self):
    return self._document_name

  @document_name.setter
  def document_name(self, value):
    self._document_name = value

  @property
  def document_title(self):
    return self._document_title

  @document_title.setter
  def document_title(self, value):
    self._document_title = value

  @property
  def document_short_title(self):
    return self._document_short_title

  @document_short_title.setter
  def document_short_title(self, value):
    self._document_short_title = value


class Amendment(object):
  def __init__(self, xml_tree):
    if xml_tree is not None:
      assert(xml_tree.tag == 'amendment')
    for field in [
        'amendment_number', 'amendment_to_amendment_number',
        'amendment_to_document_number',
        'amendment_to_document_short_title',
        'amendment_purpose']:
      try:
        setattr(self, '_' + field, xml_tree.find(field).text)
      except AttributeError:
        setattr(self, '_' + field, '')

  @property
  def amendment_number(self):
    return self._amendment_number

  @amendment_number.setter
  def amendment_number(self, value):
    self._amendment_number = value, 

  @property
  def amendment_to_amendment_number(self):
    return self._amendment_to_amendment_number

  @amendment_to_amendment_number.setter
  def amendment_to_amendment_number(self, value):
    self._amendment_to_amendment_number = value, 

  @property
  def amendment_to_document_number(self):
    return self._amendment_to_document_number

  @amendment_to_document_number.setter
  def amendment_to_document_number(self, value):
    self._amendment_to_document_number = value, 

  @property
  def amendment_to_document_short_title(self):
    return self._amendment_to_document_short_title

  @amendment_to_document_short_title.setter
  def amendment_to_document_short_title(self, value):
    self._amendment_to_document_short_title = value, 

  @property
  def amendment_purpose(self):
    return self._amendment_purpose

  @amendment_purpose.setter
  def amendment_purpose(self, value):
    self._amendment_purpose = value


class Vote(object):

  def __init__(self, xml_tree):
    assert(xml_tree.tag == 'roll_call_vote')
    for field in [
        'congress', 'session', 'congress_year', 'vote_number', 'vote_date',
        'vote_title', 'vote_question_text', 'vote_document_text',
        'vote_result_text', 'question']:
      setattr(self, '_' + field, xml_tree.find(field).text)
    for field, cls in [
        ('document', Document),
        ('amendment', Amendment)]:
      setattr(self, '_' + field, cls(xml_tree.find(field)))
    self._members = [
        member.Member(child)
        for child in xml_tree.find('members').findall('member')]

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
  def vote_question_text(self):
    return self._vote_question_text

  @vote_question_text.setter
  def vote_question_text(self, value):
    self._vote_question_text = value

  @property
  def vote_document_text(self):
    return self._vote_document_text

  @vote_document_text.setter
  def vote_document_text(self, value):
    self._vote_document_text = value

  @property
  def vote_title(self):
    return self._vote_title

  @vote_title.setter
  def vote_title(self, value):
    self._vote_title = value

  @property
  def vote_result_text(self):
    return self._vote_result_text

  @vote_result_text.setter
  def vote_result_text(self, value):
    self._vote_result_text = value

  @property
  def question(self):
    return self._question

  @question.setter
  def question(self, value):
    self._question = value

  @property
  def document(self):
    return self._document

  @document.setter
  def document(self, value):
    self._document = value

  @property
  def amendment(self):
    return self._amendment

  @amendment.setter
  def amendment(self, value):
    self._amendment = value

  @property
  def members(self):
    return self._members

  @members.setter
  def members(self, value):
    self._members = value

  def __str__(self):
    return f'<Vote vote_number={self.vote_number}>'

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash((
        self.congress, self.session, self.vote_number, self.vote_date,
        self.question))

  def __eq__(self, other_vote):
    if not isinstance(other_vote, Vote):
      return NotImplemented
    # TODO: Obviously account for all members.
    for field in [
        'congress', 'session', 'congress_year', 'vote_number', 'vote_date',
        'vote_question_text', 'vote_document_text', 'vote_result_text',
        'question']:
      if getattr(self, field) != getattr(other_vote, field):
        return False
    return True

  @classmethod
  def from_file(cls, file_name):
    tree = ElementTree.ElementTree().parse(file_name)
    return cls(tree)
