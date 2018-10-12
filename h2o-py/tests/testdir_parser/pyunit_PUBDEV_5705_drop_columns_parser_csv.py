from __future__ import print_function
import sys
sys.path.insert(1,"../../")
import h2o
from tests import pyunit_utils
import os

def import_folder():
  # generate a big frame with all datatypes and save it to csv.  Load it back with different skipped_columns settings
  nrow = 1000
  ncol = 1000
  seed=12345
  frac1 = 0.16
  frac2 = 0.2
  f1 = h2o.create_frame(rows=nrow, cols=ncol, real_fraction=frac1, categorical_fraction=frac1, integer_fraction=frac1,
                        binary_fraction=frac1, time_fraction=frac1, string_fraction=frac2, missing_fraction=0.1,
                        has_response=False, seed=seed)
  tmpdir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath('__file__')), "..", "results"))
  if not(os.path.isdir(tmpdir)):
    os.mkdir(tmpdir)
  savefilenamewithpath = os.path.join(tmpdir, 'in.csv')
  h2o.download_csv(f1, savefilenamewithpath)

  # load in whole dataset
  wholeFrame = h2o.import_file(savefilenamewithpath, skipped_columns = [0,1,2])
  skip_all = list(range(wholeFrame.ncol))
  skip_even = list(range(wholeFrame.ncol, 0, -2))
  skip_odd = list(range(wholeFrame.ncol, 1, -2))
  skip_start_end = [wholeFrame.ncol-1, 0]

  try:
    loadFileSkipAll = h2o.import_file(savefilenamewithpath, skipped_columns = skip_all)
    sys.exit(1) # should have failed here
  except:
    pass

  # skip even columns
  loadFileSkipEven = h2o.upload_file(savefilenamewithpath, skipped_columns = skip_even)

  # skip odd columns


  # skip the very beginning and the very end.


def checkCorrectSkips(completeFrame, csvfile, skipped_columns):
  skippedFrame = h2o.upload_file(csvfile, skipped_columns=skipped_columns)

  # remove columns from completeFrame



if __name__ == "__main__":
  pyunit_utils.standalone_test(import_folder)
else:
  import_folder()
