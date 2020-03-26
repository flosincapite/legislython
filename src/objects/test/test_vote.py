import os
import unittest
from xml.etree import ElementTree

from src.objects import vote


class VoteTest(unittest.TestCase):

  def setUp(self):
    super().setUp()
    fname = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      'data', 'test_vote.xml')
    self._node = vote.Vote.from_file(fname)

  def test_attributes(self):
    self.assertEqual('110', self._node.congress)
    print(self._node.votes[0].vote_number)
    print(self._node.votes[1].vote_number)


if __name__ == '__main__':
  unittest.main()
