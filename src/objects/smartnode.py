class SmartNode(object):
  # TODO: Use a metaclass for this? SIGH

  def __init__(self, xml_tree):
    for field in self.fields():
      pass
 
  @classmethod
  def root_name(cls):
    return NotImplemented

  @classmethod
  def fields(cls):
    return NotImplemented
