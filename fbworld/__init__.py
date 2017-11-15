import os

DATA_DIR = "%s/../data" % os.path.dirname(os.path.realpath(__file__))
ACCESS_TOKEN = os.environ.get('INDV_ACCESS_TOKEN', None)
