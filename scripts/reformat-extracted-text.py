#!/usr/bin/python
#
# THIS IS AN EXPERIMENTAL REWRITE - IT IS NOT WORKING YET!
#
# This script takes as standard input the extracted text from a
# stanford-bot-generated SRT file, and reformats it into something
# that is more sensible (in terms of line breaks) for use as subtitles.
#
# Apostrophes and quotation marks are left alone since I don't want to
# deal with them in a script at this moment.
#
# Notes:
#
# 1. This script assumes that its input has already been processed with
#    extract-text-from-srt. In other words it can't deal with a real
#    SRT file. The time codes must already have been removed.
#
# 2. The script will not produce something that's 100% correct. For
#    example it will treat all periods as end of segment markers,
#    even if it is the period in "Mr." or "No.". You need to pull out
#    vi and do some minimal post-processing before pasting the results
#    back into Universal Subtitles.
#

import sys
import nltk.data

def reformat_input(f):
  source = ' '.join(map(str.strip, f.readlines()))
  sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
  for s in sent_detector.tokenize(source):
    print "INPUT=%s\n" % s

def main(args):
  if len(args) == 0:
    reformat_input(sys.stdin)
  else:
    for file in args:
      reformat_input(file, 'r')

if __name__ == '__main__':
  args = sys.argv[1:]
  main(args)
