import pymarksim

from optparse import OptionParser
from optparse import SUPPRESS_USAGE

import cPickle
import gzip

import nltk

def run_train(tokenized, options):

    markov_dict = {}

    try:
        file_handle = gzip.open(options.dump_file, "rb")
        markov_dict = cPickle.load(file_handle)
        file_handle.close()
    except Exception:
        pass

    for i in xrange(0, len(tokenized)-2):
        key = (tokenized[i], tokenized[i+1])
        value = tokenized[i+2]

        if key in markov_dict:
            if value not in markov_dict[key]:
                markov_dict[key].append(value)
        else:
            markov_dict[key] = [value]

    file_handle = gzip.open(options.dump_file, "w+b")
    cPickle.dump(markov_dict, file_handle)
    file_handle.close()

    print "Done !"

def run_check(tokenized, options):
    file_handle = gzip.open(options.dump_file, "rb")
    markov_dict = cPickle.load(file_handle)
    file_handle.close()

    accept_rate = 0.0

    for i in xrange(0, len(tokenized)-2):
        key = (tokenized[i], tokenized[i+1])
        value = tokenized[i+2]

        if key in markov_dict:
            if value in markov_dict[key]:
                accept_rate += 1.0

    tokenized_len = float(len(tokenized)-2)
    print "Match %.3f %%" % (accept_rate/tokenized_len)

def run_main(options):
    file_handle = open(options.input_text, "r")
    mem_buffer = file_handle.read()
    file_handle.close()

    tokenized = nltk.word_tokenize(mem_buffer)
        
    if options.mode == "train":
        run_train(tokenized, options)
    
    if options.mode == "check":
        run_check(tokenized, options)

if __name__ == "__main__":
    parser = OptionParser(usage=SUPPRESS_USAGE)
    print "pymarksim v.%s\nBy %s\n" % (pymarksim.__version__,
                                       pymarksim.__author__)
    print "Type --help parameter for help.\n"

    parser.add_option("-d", "--df", dest="dump_file",
                      help="Pickle object file ex. pickle.db")

    parser.add_option("-i", "--input-text", dest="input_text",
                      help="Input text")

    parser.add_option("-m", "--mode", dest="mode",
                      help="Mode of operation: train, check")

    (options, args) = parser.parse_args()

    if not options.dump_file:
        parser.error("You must specify a pickle object to dump data (-d parameter) !")

    if not options.input_text:
        parser.error("You must specify an input text file to process (-i parameter) !")

    if not options.mode:
        parser.error("You must specify if you want to train or to check (-m parameter) !")

    run_main(options)




