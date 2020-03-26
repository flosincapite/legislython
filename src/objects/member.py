from xml.etree import ElementTree


class Member(object):

  def __init__(self, xml_tree):
    assert(xml_tree.tag == 'member')
    self._member_full = xml_tree.find('member_full').text
    self._last_name = xml_tree.find('last_name').text
    self._first_name = xml_tree.find('first_name').text
    self._party = xml_tree.find('party').text
    self._state = xml_tree.find('state').text
    self._vote_cast = xml_tree.find('vote_cast').text
    self._lis_member_id = xml_tree.find('lis_member_id').text

  @property
  def member_full(self):
    return self._member_full

  @member_full.setter
  def member_full(self, value):
    self._member_full = value

  @property
  def last_name(self):
    return self._last_name

  @last_name.setter
  def last_name(self, value):
    self._last_name = value

  @property
  def first_name(self):
    return self._first_name

  @first_name.setter
  def first_name(self, value):
    self._first_name = value

  @property
  def party(self):
    return self._party

  @party.setter
  def party(self, value):
    self._party = value

  @property
  def state(self):
    return self._state

  @state.setter
  def state(self, value):
    self._state = value

  @property
  def vote_cast(self):
    return self._vote_cast

  @vote_cast.setter
  def vote_cast(self, value):
    self._vote_cast = value

  @property
  def lis_member_id(self):
    return self._lis_member_id

  @lis_member_id.setter
  def lis_member_id(self, value):
    self._lis_member_id = value

  @property
  def _key_tuple(self):
    return (self.last_name, self.first_name, self.party, self.state)

  def __hash__(self):
    return hash(self._key_tuple)

  def __eq__(self, other_vote):
    if not isinstance(other_vote, Vote):
      return NotImplemented
    return self._key_tuple == other_vote._key_tuple
