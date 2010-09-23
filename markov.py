import pymarksim

from optparse import OptionParser
from optparse import SUPPRESS_USAGE

import sqlite3

def run_main(options):
    pass







if __name__ == "__main__":
    parser = OptionParser(usage=SUPPRESS_USAGE)
    print "pymarksim v.%s\nBy %s\n" % (pymarksim.__version__,
                                       pymarksim.__author__)
    print "Type --help parameter for help.\n"

    parser.add_option("-d", "--db", dest="database",
                      help="Database file to use (sqlite) ex. database.db")

    parser.add_option("-i", "--input-text", dest="input_text",
                      help="Input text")

    parser.add_option("-n", "--model-name", dest="model_name",
                      help="The model name to update/use")

    parser.add_option("-m", "--mode", dest="mode",
                      help="Mode of operation: train, check")

    (options, args) = parser.parse_args()

    if not options.database:
        parser.error("You must specify a database (-d parameter) !")

    if not options.input_text:
        parser.error("You must specify an input text file to process (-i parameter) !")

    if not options.model_name:
        parser.error("You must specify a model name to use, this is the identification " +
                     "of the train/check (-n parameter) !")

    if not options.mode:
        parser.error("You must specify if you want to train or to check (-m parameter) !")

    run_main(options)
