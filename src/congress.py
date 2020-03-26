def congress_range(congress_1, congress_2):
  while congress_1 < congress_2:
    print(congress_1)
    yield congress_1
    congress_1 = congress_1 + 1


class Congress(object):
  def __init__(self, congress=None, session=None):
    assert((congress is None) + (session is None) in {0, 2})
    if session is not None:
      assert(session in {1, 2})
    self._congress = congress
    self._session = session

  @property
  def congress(self):
    return self._congress

  @property
  def session(self):
    return self._session

  def __eq__(self, other_congress):
    if not isinstance(other_congress, Congress):
      return other_congress == self
    return (
        self.congress == other_congress.congress and
        self.session == other_congress.session)
    
  def __lt__(self, other_congress):
    if not isinstance(other_congress, Congress):
      return other_congress >= self
    if other_congress.congress is None:
      return self.congress is not None
    if self.congress > other_congress.congress:
      return False
    return (
        self.congress < other_congress.congress or
        self.session < other_congress.session)

  def __add__(self, increment):
    sess = self.session
    cong = self.congress
    for _ in range(increment):
      if sess == 1:
        sess = 2
      else:
        cong += 1
        sess = 1
    return Congress(cong, sess)

  def __iadd__(self, increment):
    print('Called iadd')
    for _ in range(increment):
      print('iadd iterating')
      if self.session == 1:
        self._session = 2
      else:
        self._congress += 1
        self._session = 1
    return self

  def __str__(self):
    return f'<Congress congress={self.congress} session={self.session}>'

  def __repr__(self):
    return str(self)
