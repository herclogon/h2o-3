from __future__ import print_function
import sys
sys.path.insert(1,"../../")
import h2o
from tests import pyunit_utils
import os
import pandas as pd
import random

def import_folder():
  # generate a big frame with all datatypes and save it to csv.  Load it back with different skipped_columns settings
  nrow = 1000
  ncol = 1000
  nrow = 100
  ncol = 7
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
  outputfile = os.path.join(tmpdir, 'out.csv')
  h2o.download_csv(f1, savefilenamewithpath)

  # load in whole dataset
  skip_all = list(range(f1.ncol))
  skip_even = list(range(0, f1.ncol, 2))
  skip_odd = list(range(1, f1.ncol, 2))
  skip_start_end = [0, f1.ncol-1]
  skip_except_last = list(range(0, f1.ncol-2))
  skip_except_first = list(range(1, f1.ncol))
  temp = list(range(0, f1.ncol))
  random.shuffle(temp)
  skip_random = []
  for index in range(0, f1.ncol/2):
    skip_random.append(temp[index])
  skip_random.sort()

  skippedFrameUF = h2o.import_file(savefilenamewithpath, skipped_columns=skip_even)

  try:
    loadFileSkipAll = h2o.upload_file(savefilenamewithpath, skipped_columns = skip_all)
    sys.exit(1) # should have failed here
  except:
    pass

  try:
    importFileSkipAll = h2o.import_file(savefilenamewithpath, skipped_columns = skip_all)
    sys.exit(1) # should have failed here
  except:
    pass

  # skip even columns
  checkCorrectSkips(outputfile, savefilenamewithpath, skip_even)

  # skip odd columns
  checkCorrectSkips(outputfile, savefilenamewithpath, skip_odd)

  # skip the very beginning and the very end.
  checkCorrectSkips(outputfile, savefilenamewithpath, skip_start_end)

  # skip all except the last column
  checkCorrectSkips(outputfile, savefilenamewithpath, skip_except_last)

  # skip all except the very first column
  checkCorrectSkips(outputfile, savefilenamewithpath, skip_except_first)

  # randomly skipped half the columns
  checkCorrectSkips(outputfile, savefilenamewithpath, skip_random)


def checkCorrectSkips(outputfile, csvfile, skipped_columns):
  skippedFrameUF = h2o.upload_file(csvfile, skipped_columns=skipped_columns)
  skippedFrameIF = h2o.import_file(csvfile, skipped_columns=skipped_columns) # this two frames should be the same
  pyunit_utils.compare_frames_local(skippedFrameUF, skippedFrameIF, prob=1.0)

  # download frame with skipped columns to csv file
  h2o.download_csv(skippedFrameIF, outputfile)

  # compare the two csv files to make sure they are agree except in the skipped columns
  with (open(csvfile), open(outputfile)) as (ffull, fskip):
    for (linef, lines) in (ffull, fskip):
      listf = linef.split(',')
      lists = lines.split(',')  # contain fewer columns
      skippedCounter = 0;
      for cindex in range(len(listf)):
        if (cindex not in skipped_columns):
          assert listf[cindex]==lists[skippedCounter], "contents of skipped file {0} does not match correct parsing value {1}.".format(lists[skippedCounter], listf[cindex])
          skippedCounter=skippedCounter+1




if __name__ == "__main__":
  pyunit_utils.standalone_test(import_folder)
else:
  import_folder()
