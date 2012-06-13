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
#    always produce correct results and so you will still need to do a
#    manual review.
#

import sys
import re
import nltk.data


class Timing:
  PAT_TIMECODE_CAPTURE = re.compile(r'^(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)$')

  def __init__(self):
    self.raw = []
    self.tokens = []
    self.seq = 0
    self.ptr = 0

  def decode_timecode(self, timecode):
    t_i, t_f = None, None
    m = self.PAT_TIMECODE_CAPTURE.search(timecode)
    if m:
      t_i = 3600000*int(m.group(1)) + 60000*int(m.group(2)) \
		  + 1000*int(m.group(3)) + int(m.group(4))
      t_f = 3600000*int(m.group(5)) + 60000*int(m.group(6)) \
		  + 1000*int(m.group(7)) + int(m.group(8))
    return t_i, t_f

  def time_str(self, t):
    return "%02d:%02d:%02d,%03d" % (int(t/3600000), int(t/60000)%60, \
					    int(t/1000)%60, t%1000)

  def remember(self, node):
    id = int(node[0])
    t_i, t_f = self.decode_timecode(node[1])
    self.raw.append([id, t_i, t_f, node[2:]])

    tokens = (' '.join(node[2:])).split(' ')
    dt = (t_f - t_i)/len(tokens)
    for i, token in enumerate(tokens):
      self.tokens.append([token, t_i + dt*i])

  def emit_segment(self, s):
    tokens = s.split(' ')
    n = len(tokens)
    t_i = self.tokens[self.ptr][1]
    t_f = self.tokens[self.ptr + n][1] if self.ptr + n < len(self.tokens) else self.raw[-1][2]

    for i, token in enumerate(tokens):
      chk = self.tokens[self.ptr + i][0]
      if token.strip('.') != chk.strip('.'):
	raise Exception("Near %s: looking for %s but found %s" % (
			self.time_str(self.tokens[self.ptr + i][1]),
			str(token),
			str(chk)))

    print "%d" % (self.seq + 1)
    print "%s --> %s" % (self.time_str(t_i), self.time_str(t_f))
    print "%s\n" % s
    self.ptr += n
    self.seq += 1


PAT_ID = re.compile(r'^\d+$')
PAT_TIMECODE = re.compile(r'^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d$')

STATE_INIT = 0
STATE_TEXT = 1
STATE_ID_FOUND = 2
STATE_TIMECODE_FOUND = 3


def normalize_input(source):
  source = re.sub(r'\s+', r' ', source, re.DOTALL)
  source = re.sub(r"'", r'’', source)

  #
  # stanford-bot favours extremely colloquial forms;
  # this is decidedly inappropriate for lectures.
  #
  source = re.sub(r'\bcuz\b', r'’cause', source)
  source = re.sub(r'\bgonna\b', r'going to', source)
  source = re.sub(r'\bwanna\b', r'want to', source)

  #
  # stanford-bot's output contains numerous formatting bugs,
  # including missing periods at the end of sentences.
  # Try to make some guesses in an attempt to fix *that*.
  #
  # If it's a period followed by a double quote,
  # theoretically we shouldn't need to do anything.
  # But NLTK gets confused (?!) so we still have to add a period...
  #
  source = re.sub(r'([^\.]) (Also|And|Because|But|Here|Or)\b', \
		  r'\1. \2', source)

  #
  # This is for NLTK. Hard to believe. But true :P
  #
  source = re.sub(r'([\.!\?]")(\s)', r'\1.\2', source)

  return source


def reformat_input(f):
  sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
  source = ''
  memory = []
  timing = Timing()
  state = STATE_INIT

  id = None
  timecode = None

  for s in map(str.strip, f.readlines()):
    if state == STATE_INIT:
      if PAT_ID.search(s):
	memory = [s]
	state = STATE_ID_FOUND
      else:
	source = ' '.join(memory)
	state = STATE_TEXT
    elif state == STATE_ID_FOUND:
      if PAT_TIMECODE.search(s):
	memory.append(s)
	state = STATE_TIMECODE_FOUND
      else:
	source = ' '.join(memory)
	state = STATE_TEXT
    elif state == STATE_TIMECODE_FOUND and PAT_ID.search(s):
      memory = [s]
    elif state == STATE_TIMECODE_FOUND and PAT_TIMECODE.search(s):
      memory.append(s)
    elif state == STATE_TIMECODE_FOUND and len(s) == 0:
      timing.remember(memory)
      memory = None
    else:
      if state == STATE_TIMECODE_FOUND:
	memory.append(normalize_input(s))
      if source:
	source += ' '
      source += s

  if state == STATE_TIMECODE_FOUND and memory is not None:
    timing.remember(memory)

  source = normalize_input(source)

  for s in sent_detector.tokenize(source):
    s = re.sub(r'([\.!\?]"?)\.', r'\1', s)
    if state == STATE_TIMECODE_FOUND:
      timing.emit_segment(s)
    else:
      print s


def main(args):
  if len(args) == 0:
    reformat_input(sys.stdin)
  else:
    for file in args:
      reformat_input(file, 'r')

if __name__ == '__main__':
  args = sys.argv[1:]
  main(args)
