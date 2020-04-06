import os

from xml.etree import ElementTree

from src import congress
from src import utils
from src.objects import roll


def rolls_for_range(
    first_congress=None, last_congress=None, directory=None):
  """Generates Rolls within the provided date range.

  Rolls will be generated for all congresses in the closed interval
  [first_congress, last_congress].
  If directory is provided, this method will use it as a local cache to avoid
  making redundant HTTP requests for rolls.

  Args:
    first_congress: Congress object (src/congress.py)
    last_congress : Congress object
    roll_dir: local directory; rolls will be cached here if not None
    vote_dir: local directory; votes will be cached here if not None
  """
  if first_congress is None:
    first_congress = congress.Congress(101, 1)
  if last_congress is None:
    last_congress = congress.Congress()

  for the_congress in congress.congress_range(first_congress, last_congress):
    if directory is not None:
      fname = os.path.join(
          directory, f'{the_congress.congress}_{the_congress.session}.xml')
      if os.path.exists(fname):
        yield roll.Roll.from_file(fname)
        continue

    try:
      contents = utils.retrieve_roll(
          the_congress.congress, the_congress.session)

    except utils.NoXmlError:
      # No more .xml files after this point.
      break

    # TODO: Handle GotRedirectedError.
    except utils.GotRedirectedError:
      raise

    if directory is not None:
      with open(fname, 'w') as outp:
        outp.write(contents)

    yield roll.Roll(ElementTree.fromstring(contents))
