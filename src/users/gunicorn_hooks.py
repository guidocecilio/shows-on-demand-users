# First think needs to be monkey patching, so avoiding other global imports
from gevent.monkey import patch_all
patch_all()


def on_starting(server):
    pass


def pre_fork(server, worker):
    pass


def post_fork(server, worker):
    pass
