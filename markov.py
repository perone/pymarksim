import pymarksim

from optparse import OptionParser
from optparse import SUPPRESS_USAGE
import cPickle
import gzip

from nltk import word_tokenize

class MarkovItem(object):
    def __init__(self, item, probability):
        self.item = item
        self.probability = probability    

    def __repr__(self):
        return "<MarkovItem '%s':%.2f>" % (self.item, self.probability)

    def __eq__(self, other):
        return self.item == other.item

def run_train(tokenized, options):

    markov_dict = {}

    try:
        file_handle = gzip.open(options.dump_file, "rb",
                                compresslevel=options.compress_level)
        print "File %s found, loading..." % options.dump_file
        markov_dict = cPickle.load(file_handle)
        file_handle.close()
    except Exception:
        print "File %s not found, creating a new one..." % options.dump_file

    print "Updating..."
    for i in xrange(0, len(tokenized)-2):
        key = (tokenized[i], tokenized[i+1])
        value = tokenized[i+2]
        new_transition = MarkovItem(value, 1.0)

        # If the key is already present in the markov dict
        if key in markov_dict:
            # If we still don't have that transition
            if new_transition not in markov_dict[key]:
                markov_dict[key].append(new_transition)
            else:
                # if we have that transition
                pass                
        else:
            markov_dict[key] = [new_transition]


    file_handle = gzip.open(options.dump_file, "w+b",
                            compresslevel=options.compress_level)
    cPickle.dump(markov_dict, file_handle)
    file_handle.close()

    # Show the chain
    #for k,v in markov_dict.items():
    #   print k,v

    print "Done !"

def run_check(tokenized, options):
    file_handle = gzip.open(options.dump_file, "rb",
                            compresslevel=options.compress_level)
    print "File %s found, loading..." % options.dump_file
    markov_dict = cPickle.load(file_handle)
    file_handle.close()

    accept_rate = 0.0

    print "Checking..."

    for i in xrange(0, len(tokenized)-2):
        key = (tokenized[i], tokenized[i+1])
        value = MarkovItem(tokenized[i+2], 1.0)

        if value in markov_dict.get(key, []):
            accept_rate += 1.0
    
    tokenized_len = float(len(tokenized)-2)
    print "Match %.2f %%" % ((accept_rate/tokenized_len)*100.0)

def run_main(options):
    file_handle = open(options.input_text, "r")
    mem_buffer = file_handle.read()
    file_handle.close()

    tokenized = word_tokenize(mem_buffer)

    globals()["run_%s" % options.mode](tokenized, options)

if __name__ == "__main__":
    parser = OptionParser(usage=SUPPRESS_USAGE)
    print "pymarksim v.%s\nBy %s\n%s\n" % (pymarksim.__version__,
                                           pymarksim.__author__,
                                           pymarksim.__home__)
    print "Type --help parameter for help.\n"

    parser.add_option("-d", "--df", dest="dump_file",
                      help="Pickle object file ex. pickle.db")

    parser.add_option("-i", "--input-text", dest="input_text",
                      help="Input text")

    parser.add_option("-m", "--mode", dest="mode",
                      help="Mode of operation: train, check")

    parser.add_option("-c", "--compress-level", dest="compress_level", default=9, type="int",
                      help="The gzip compression level, default is 9 (max).")

    (options, args) = parser.parse_args()

    if not options.dump_file:
        parser.error("You must specify a pickle object to dump data (-d parameter) !")

    if not options.input_text:
        parser.error("You must specify an input text file to process (-i parameter) !")

    if not options.mode:
        parser.error("You must specify if you want to train or to check (-m parameter) !")

    run_main(options)




