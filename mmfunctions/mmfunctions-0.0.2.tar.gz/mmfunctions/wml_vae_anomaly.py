# VAE in Watson Machine Learning
import logging
import os
import sys
import numpy as np
import pandas as pd
from optparse import OptionParser

from iotfunctions import base
from iotfunctions import bif
from iotfunctions import entity
from iotfunctions import metadata
from iotfunctions.metadata import EntityType
from iotfunctions.db import Database
from iotfunctions.dbtables import FileModelStore
from iotfunctions.enginelog import EngineLogging
from iotfunctions import estimator
from mmfunctions.anomaly import VIAnomalyScore

# database front
class DatabaseDummy:
    tenant_id = '###_IBM_###'
    db_type = 'db2'
    model_store = FileModelStore()
    def _init(self):
        return


# get first argument - dataset name with entity name and timestamp as index columns
parser = OptionParser()

parser.add_option("-f", "--file", dest="filename",
                  default='AllOfArmstark.csv',
                  help="load data from FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
                  dest="verbose", default=True,
                  action="store_false",
                  help="don't print status messages to stdout")
parser.add_option("-d", "--delete",
                  dest="delete", default=True,
                  action="store_true",
                  help="delete old models")

(options, args) = parser.parse_args()

print("Loading data from " + str(options.filename))


# Load data
df_input = pd.read_csv(str(options.filename), parse_dates=['timestamp'], comment='#')
#df_input = df_input.asfreq('H')
df_input = df_input.sort_values(by='timestamp').set_index('timestamp').dropna().reset_index().set_index(['entity','timestamp'])

if df_input.size < 5:
    print('Dataset too small')
    exit

# pretend to open a database connection and set up the FileModelStore
db_schema=None
db = DatabaseDummy()


EngineLogging.configure_console_logging(logging.DEBUG)
jobsettings = { 'db': db,
               '_db_schema': 'public', 'save_trace_to_file' : True}

spsi = VIAnomalyScore(['Ap'], ['Vx'])
spsi.prior_sigma = 2.0
#et = spsi._build_entity_type(columns = [Column('MinTemp',Float())], **jobsettings)
et = spsi._build_entity_type(**jobsettings)
spsi._entity_type = et
df_input = spsi.execute(df=df_input)

print(type(spsi.Input))
for entity in df_input.index.levels[0]:
    print('Entity: ' + entity)
    print('    AP: ' + str(spsi.Input[entity]))
    print('    MU: ' + str(spsi.mu[entity]))
    print('    QU: ' + str(spsi.quantile095[entity]))


print(df_input.head(4))


EngineLogging.configure_console_logging(logging.INFO)

# save_path = saver.save(sess, model_path)
print("Model saved in files: %s" % spsi.models)

try:
    print(os.environ["RESULT_DIR"])
    os.system("(cd $RESULT_DIR;ls *VI*)")
    print(str(os.listdir(os.environ["RESULT_DIR"])))
except Exception as ee:
    print('Result Dir not found' + str(ee))

sys.stdout.flush()

