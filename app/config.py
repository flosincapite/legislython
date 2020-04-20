import os
import tempfile


_tmp_dir = tempfile.mkdtemp()
_data_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data')
_roll_cache = os.path.join(_data_dir, 'rolls')
os.makedirs(_roll_cache, exist_ok=True)
_vote_cache = os.path.join(_data_dir, 'votes')
os.makedirs(_vote_cache, exist_ok=True)


class Config(object):

  SECRET_KEY = os.environ.get('SECRET_KEY', 'NOTHING')
  ROLL_CACHE = _roll_cache
  VOTE_CACHE = _vote_cache
  TEMP_DIR = _tmp_dir
