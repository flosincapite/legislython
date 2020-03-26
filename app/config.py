import os
import tempfile


# _tmp_dir = tempfile.mkdtemp()
_tmp_dir = '/tmp/tmp7u2s0udc'
_roll_cache = os.path.join(_tmp_dir, 'rolls')
os.makedirs(_roll_cache, exist_ok=True)
_vote_cache = os.path.join(_tmp_dir, 'votes')
os.makedirs(_vote_cache, exist_ok=True)


class Config(object):

  SECRET_KEY = os.environ.get('SECRET_KEY', 'NOTHING')
  ROLL_CACHE = _roll_cache
  VOTE_CACHE = _vote_cache
