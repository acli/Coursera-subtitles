#!/usr/bin/python
# -*- coding: utf8 -*-
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
# 2. The script will not produce something that's 100% correct. It will
#    attempt to split at correct sentence boundaries using the NLTK
#    Punkt tokenizer; however, because stanford-bot's output sometimes
#    contains missing periods and other bugs, the tokenization does not
#    always produce correct results and so you will still need to review
#    it.
#

import sys
import re
import nltk.data

def reformat_input(f):
  sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

  source = ' '.join(map(str.strip, f.readlines()))
  source = re.sub(r'\s+', r' ', source)
  source = re.sub(r"'", r'’', source)
  source = re.sub(r'\bcuz\b', r'’cause', source)
  source = re.sub(r'\bgonna\b', r'going to', source)
  source = re.sub(r'\bwanna\b', r'want to', source)

  #
  # stanford-bot's output contains numerous formatting bugs,
  # including missing periods at the end of sentences.
  # Try to make some guesses in an attempt to fix *that*.
  #
  source = re.sub(r'([^\.]) (And|But|Or)\b', r'\1. \2', source)

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
