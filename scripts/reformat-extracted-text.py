#!/usr/bin/python
# -*- coding: utf8 -*-
#
# This script takes as standard input either a Cogi-generated SRT file,
# or the extracted text from such a file; and reformats it into something
# that is more sensible (in terms of line breaks) for use as subtitles.
#
# Notes:
#
# 1. The realigned timings are only estimates. I use estimates such as
#    the estimated number of syllables in a word to help prevent the
#    timings from getting too out of whack, but perfect timings are
#    impossible. You still need to check the timings.
#
# 2. The script will not produce something that's 100% correct. It will
#    attempt to split at correct sentence boundaries using the NLTK
#    Punkt tokenizer; however, because stanford-bot's output sometimes
#    contains missing periods and other bugs, the tokenization does not
#    always produce correct results. Also, sentences can be extremely
#    long that we still need to find a way to split those. For these
#    reasons you will still need to do a manual review.
#

import time
import sys
import re
import pdb

import nltk.data
from nltk.tokenize import TreebankWordTokenizer

from nltk.corpus import treebank
from nltk import treetransforms
from nltk import induce_pcfg
from nltk.parse import pchart


class Timing:
  PAT_NARROW = re.compile(r"^(?:[\..:;!'1Iil]|‘|’)$")
  PAT_WIDE = re.compile(r'^(?:[A-Zmw]|—)$')

  PAT_ACRONYM = re.compile(r'^(?:[A-Z]+|[Oo]k)$')
  PAT_SHORT = re.compile(r'^(?:[",])$')
  PAT_LONG = re.compile(r'^(?:[-;:\.])$')
  PAT_ZERO = re.compile(r"^(?:'[ds]?|'[rv]e)$")

  PAT_NUMBER_RAW = r"(?:(?:\d+|\d{1,3}(?:,\d{3})*)(?:\.\d+)?)"
  PAT_MONETARY_RAW = r"(?:\$\s*%s)" % PAT_NUMBER_RAW
  PAT_MONETARY_CAPTURE = re.compile(r"(?:\$\s*(%s))" % PAT_NUMBER_RAW)
  PAT_NUMERIC = re.compile(r"^(?:%s|%s)$" % (PAT_NUMBER_RAW, PAT_MONETARY_RAW))

  PAT_DECIMAL_CAPTURE = re.compile(r'^(\d+)?\.(\d+)$')

  PAT_VOWEL_CLUSTER = re.compile(r'(?:ing|[aeiou]+|y$|y(?=[^aeiou]))')
  PAT_CONST_CLUSTER = re.compile(r'[bcdfghjklmnpqrstvxz]+')
  PAT_SEMI_CLUSTER = re.compile(r"(?:[wy]+|(?:n't|sm|thm)$)")
  PAT_W = re.compile(r'[Ww]')

  PAT_COMMA = re.compile(r',')

  # Possible fragment boundaries, in decreasing preference
  PAT_POSSIBLE_FRAGMENT_BOUNDARY = (
    re.compile(r'(?:(?:'\
      + r'(?<=, )(?:and|if|that|where|whereas|whether|which|who|why)\b'\
      + r')|(?:'\
      + r'\b(?:and again|and,? so),'\
      + r')|(?:'\
      + r'\b(?:and as'\
      + r'|and will'\
      + r'|because'\
      + r'|is that|is one|is to'\
      + r'|rather than'\
      + r'|so that'\
      + r'|that'\
      + r'|who)\b'\
      + r')|(?:'\
      + r'>> '\
      + r')|(?:'\
      + r'(?<=[,;] ).'\
      + r'))'),
    re.compile(r'(?:(?:'\
      + r'\b(?:above|at|and'\
      + r'|but'\
      + r'|depending on'\
      + r'|in'\
      + r'|of|on|or'\
      + r'|to'\
      + r'|unless|until|unto|upon)\b'\
      + r')|(?:'\
      + r'(?<=[,;] ).'\
      + r'))'),
  )

  THRES = 432 # about 108 characters

  Units = ('zero', 'one', 'two', 'three', 'four', 'five', 
      'six', 'seven', 'eight', 'nine', 'ten', 
      'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 
      'sixteen', 'seventeen', 'eighteen', 'nineteen')
  Tens = (None, None, 'twenty', 'thirty', 'forty', 'fifty', 
      'sixty', 'seventy', 'eighty', 'ninty')

  def __init__(self):
    self.MIN_DURATION = Timecode('00:00:01,500')

    self.raw = []
    self.tokens = []
    self.seq = 0
    self.ptr = 0

    self.sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    self.word_tokenizer = TreebankWordTokenizer()

#   sys.stderr.write('Reading tree bank data...')
#   t0 = time.time()
#   productions = []
#   S = nltk.Nonterminal('S')
#   for fileid in nltk.corpus.treebank.fileids():
#     for tree in nltk.corpus.treebank.parsed_sents(fileid):
#       productions += tree.productions()
#   sys.stderr.write(' %d trees read in %.2fs\n' \
#       % (len(productions), time.time() - t0))

#   sys.stderr.write('Training parser...')
#   t0 = time.time()
#   self.grammar = nltk.induce_pcfg(S, productions)
#   sys.stderr.write(' %d productions inducted in %.2fs\n' \
#       % (len(self.grammar.productions()), time.time() - t0))


  def decode_timecode(self, timecode):
    return map(Timecode, timecode.split(' --> '))


  def length_metric(self, s):
    """ A very simple length metric that assumes all characters have width 4
        except ', 1, I, i, l which have width 2
        and m, w and uppercase letters which have width 7
    """
    it = 0
    for c in s:
      if self.PAT_NARROW.search(c):
        it += 2
      elif self.PAT_WIDE.search(c):
        it += 7
      else:
        it += 4
    return it


  def remember(self, node):
    id = int(node[0])
    t_i, t_f = self.decode_timecode(node[1])
    self.raw.append([id, t_i, t_f, node[2:]])

    # Figure out the set of tokens comprising this input
    tokens = []
    for s in self.sent_tokenizer.tokenize(normalize_input(' '.join(node[2:]))):
      #sys.stderr.write('DEBUG: s=%s\n' % (s))
      tokens += self.word_tokenizer.tokenize(s)
      # Work around NLTK weirdness (, not separated into a token)
      if tokens[-1] != ',' and tokens[-1][-1] == ',':
        tokens.append(tokens[-1][-1])
        tokens[-2] = tokens[-2][0:-1]

    # Estimate relative timing for each token
    w = []
    for token in tokens:
      w.append(self.estimate_time_units(token))

    # Remember the estimate timing of each token
    dt = (t_f - t_i)/sum(w)
    t = t_i
    for i, token in enumerate(tokens):
      #sys.stderr.write('DEBUG: %s [%d]: %s\n' % (str(t), w[i], token))
      self.tokens.append([token, t])
      t += dt * w[i]


  def emit_segment(self, s):
    segments = []

    # Check for overlong sentences
    if self.length_metric(s) > self.THRES:
      #sys.stderr.write('Warning: Line %d too long: %s\n' % (self.seq + 1, s))
      tokens = self.word_tokenizer.tokenize(s)
      segments = self.break_into_fragments(s,
          map(lambda x: x[1], self.tokens[self.ptr:self.ptr + len(tokens)]))
    else:
      segments.append(s)

    for s in segments:
      self._emit_segment(s)


  def _emit_segment(self, s):
    tokens = self.word_tokenizer.tokenize(s)

    # Double-check that things look sane,
    sys.stderr.write('DEBUG: s=%s -> tokens=%s\n' % (s, tokens))
    n = 0
    for i, token in enumerate(tokens):
      chk = self.tokens[self.ptr + n][0]
      sys.stderr.write('DEBUG: emit=%s, mem=%s\n' % (token, chk))
      if token == '.' and chk != '.':
        sys.stderr.write('DEBUG: resync\n')
        continue
      if token != '.' and chk == '.':
        n += 1
        chk = self.tokens[self.ptr + n][0]
        sys.stderr.write('DEBUG: resync: mem=%s\n' % (chk))
      if token != chk:
        raise Exception("Near %s: Expecting \"%s\" but found \"%s\"" % (
                        str(self.tokens[self.ptr + n][1]),
                        str(token),
                        str(chk)))
      n += 1

    # Output the segment in SRT format
    t_i = self.tokens[self.ptr][1]
    t_f = self.tokens[self.ptr + n][1] if self.ptr + n < len(self.tokens) \
          else self.raw[-1][2]
    print "%d\r" % (self.seq + 1)
    print "%s --> %s\r" % (str(t_i), str(t_f))
    print "%s\r\n\r" % self.normalize_output(s)
    self.ptr += n
    self.seq += 1


  def break_into_fragments(self, s, timings):
    it = None
    for pat in self.PAT_POSSIBLE_FRAGMENT_BOUNDARY:
      it = self._break_into_fragments(s, timings, pat)
      if it:
        break
    if not it or None in it:
      raise Exception('Failed to find suitable break points: %s' % s)
    return it


  def _break_into_fragments(self, s, timings, pat):
    for n in range(2, 10):
      it = []
      candidate = [None] * n
      delta = len(s)/n
      for i in range(1, n):
        possible_start = delta * i
        for j in range(5, 1, -1):
          start = possible_start - delta/j
          end = possible_start + delta/j
          m = pat.search(s, start, end)
          if m:
            candidate[i] = m.start()
            #pdb.set_trace()
            break
        if candidate[i] is None:
          break
      if None not in candidate[1:n]:
        start = [0] + candidate[1:n]
        end = candidate[1:n] + [len(s)]
        for i in range(0, n):
          candidate = s[start[i]:end[i]]
          tokens = self.word_tokenizer.tokenize(candidate)
          width = self.length_metric(candidate)
          duration = sum(timings[0:len(tokens)])
          if width <= self.THRES and duration >= self.MIN_DURATION:
            it.append(candidate)
          else:
            it.append(None)
        if None not in it:
          break
    return it


  def estimate_time_units(self, s):
    """ Given a token s, estimate how many syllables (or equivalent) it has """
    if self.PAT_ACRONYM.search(s):
      it = len(s) + 2*len(self.PAT_W.findall(s)) # "W" is 3 syllables
    elif self.PAT_SHORT.search(s):
      it = 1
    elif self.PAT_LONG.search(s):
      it = 2
    elif self.PAT_ZERO.search(s):
      it = 0
    else:
      if self.PAT_NUMERIC.search(s):
        s = self.number_in_words(s)
      det = s.lower()
      vowels = len(self.PAT_VOWEL_CLUSTER.findall(det))
      semis = len(self.PAT_SEMI_CLUSTER.findall(det))
      it = vowels if vowels else vowels + semis
      if not it:
        it = len(self.PAT_CONST_CLUSTER.findall(det)) # FIXME
    return it


  def number_in_words(self, s):
    m = self.PAT_MONETARY_CAPTURE.search(s)
    if m:
      it = self.number_in_words(m.group(1))
      it += ' dollar' if it == 'one' else ' dollars'
    else:
      s = self.PAT_COMMA.sub('', s)
      m = self.PAT_DECIMAL_CAPTURE.search(s)
      if m:
        decimals = m.group(2)
        if m.group(1):
          it = self.number_in_words(m.group(1)) + ' point'
        else:
          it = 'point'
        for digit in decimals:
          it += ' '
          it += self.Units[int(digit)]
      else:
        x = int(s)
        if x < len(self.Units):
          it = self.Units[x]
        elif x < 100:
          tens = int(x/10)
          units = x%10
          it = self.Tens[tens]
          if units:
            it += ' ' + self.number_in_words(str(units))
        elif x < 1000:
          hundreds = int(x/100)
          remainder = x%100
          it = self.number_in_words(str(hundreds)) + ' hundred'
          if remainder:
            if remainder < 10:
              it += ' and'
            it += ' '
            it += self.number_in_words(str(remainder))
        elif x < 10000:
          thousands = int(x/1000)
          remainder = x%1000
          it = self.number_in_words(str(thousands)) + ' thousand'
          if remainder:
            if remainder < 10:
              it += ' and'
            it += ' '
            it += self.number_in_words(str(remainder))
        elif x < 1000000:
          thousands = int(x/1000)
          remainder = x%1000
          it = self.number_in_words(str(thousands)) + ' thousand'
          if remainder and remainder < 10:
            it += ' and'
          it += ' '
          it += self.number_in_words(str(remainder))
        elif x < 10000000:
          millions = int(x/1000000)
          remainder = x%1000000
          it = self.number_in_words(str(millions)) + ' million'
          if remainder:
            if remainder < 10:
              it += ' and'
            it += ' '
            it += self.number_in_words(str(remainder))
        elif x < 1000000000:
          millions = int(x/1000000)
          remainder = x%1000000
          it = self.number_in_words(str(millions)) + ' million'
          if remainder and remainder < 10:
            it += ' and'
          it += ' '
          it += self.number_in_words(str(remainder))
        elif x < 10000000000:
          billions = int(x/1000000000)
          remainder = x%1000000000
          it = self.number_in_words(str(billions)) + ' billion'
          if remainder:
            if remainder < 10:
              it += ' and'
            it += ' '
            it += self.number_in_words(str(remainder))
        elif x < 1000000000000:
          billions = int(x/1000000000)
          remainder = x%1000000000
          it = self.number_in_words(str(billions)) + ' billion'
          if remainder and remainder < 10:
            it += ' and'
          it += ' '
          it += self.number_in_words(str(remainder))
        else:
          it = s
    return it


  def normalize_output(self, s0):
    """ These are not movies. Remove [cough] or [sound] but not too early. """
    s = s0.encode('utf-8')
    s = re.sub(r'(\s*)\[(?:cough|sound)\](\s*)', r'\1\2', s)
    s = re.sub(r'\s+', r' ', s, re.DOTALL) # again

    #
    # There are other random formatting bugs that from my experience
    # are caused by training on PDF files. These are too numerous
    # to count and you really can't fix them all because you can't
    # predict them all :-(
    #
    # Ideally these should have been already normalized when we did
    # the input processing, unfortunately words sometimes actually got
    # broken off between subtitles (!)
    #
    s = re.sub(r'\b(info) (rmation)\b', r"\1\2", s)
    s = re.sub(r'\b(p) (arts)\b', r"\1\2", s)
    s = re.sub(r'\b(recog) (niz)', r"\1\2", s)
    s = re.sub(r'\b(softwa) (re)\b', r"\1\2", s)
    s = re.sub(r'(stru) (ctur)', r"\1\2", s)

    s = re.sub(r"'", ur'’', s)

    s = re.sub(r'(^|\s)(?:``|")', ur'\1“', s)
    s = re.sub(r'(^|\s)"', ur'\1“', s)
    s = re.sub(r'".', ur'.”', s)
    s = re.sub(r'(\S)"', ur'\1”', s)
    return s


class Timecode:
  PAT_TIMECODE_CAPTURE = re.compile(r'^(\d\d):(\d\d):(\d\d),(\d\d\d)$')

  def __init__(self, timecode):
    if isinstance(timecode, int) or isinstance(timecode, float):
      self.milliseconds = timecode
    else:
      m = self.PAT_TIMECODE_CAPTURE.search(timecode)
      if m:
        self.milliseconds = 3600000*int(m.group(1)) + 60000*int(m.group(2)) \
                                    + 1000*int(m.group(3)) + int(m.group(4))
      else:
        raise ValueError('Malformed timecode "%s"' % timecode)

  def __str__(self):
    t = self.milliseconds
    return "%02d:%02d:%02d,%03d" % (int(t/3600000), int(t/60000)%60, \
                                            int(t/1000)%60, t%1000)

  def __add__(self, other):
    return Timecode(self.milliseconds + (other.milliseconds \
                            if isinstance(other, Timecode) else float(other)))

  def __radd__(self, other): # needed for sum()
    return Timecode(self.milliseconds + (other.milliseconds \
                            if isinstance(other, Timecode) else float(other)))

  def __sub__(self, other):
    return Timecode(self.milliseconds - (other.milliseconds \
                            if isinstance(other, Timecode) else float(other)))

  def __mul__(self, other):
    return Timecode(self.milliseconds * other)

  def __div__(self, other):
    return Timecode(self.milliseconds / other)

  def __truediv__(self, other):
    return Timecode(self.milliseconds / float(other))

  def __lt__(self, other):
    return self.milliseconds < other.milliseconds

  def __le__(self, other):
    return self.milliseconds <= other.milliseconds

  def __eq__(self, other):
    return self.milliseconds == other.milliseconds

  def __nq__(self, other):
    return self.milliseconds != other.milliseconds

  def __ge__(self, other):
    return self.milliseconds >= other.milliseconds

  def __gt__(self, other):
    return self.milliseconds > other.milliseconds


PAT_ID = re.compile(r'^\d+$')
PAT_TIMECODE = re.compile(r'^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d$')

STATE_INIT = 0
STATE_TEXT = 1
STATE_ID_FOUND = 2
STATE_TIMECODE_FOUND = 3


def normalize_input(source):
  source = re.sub(r'\s+', r' ', source, re.DOTALL)

  #
  # NLTK gets very confused by a sequence of ."
  # so we normalize that to ". early
  # in order to avoid other problems.
  #
  source = re.sub(r'(\.)(")', r'\2\1', source) # scandalous!

  #
  # stanford-bot favours extremely colloquial forms;
  # this is decidedly inappropriate for lectures.
  #
  source = re.sub(r'\bcuz\b', r"'cause", source)
  source = re.sub(r'\bgonna\b', r'going to', source)
  source = re.sub(r'\boutta\b', r'out of', source)
  source = re.sub(r'\bwanna\b', r'want to', source)

  #
  # easy terminology fixes
  # (even in Canada we don't write "dialogue box" with the "ue")
  #
  source = re.sub(r'\b(dialog)ue (box)', r'\1 \2', source)

  #
  # stanford-bot's output contains numerous formatting bugs,
  # including missing periods at the end of sentences.
  # Try to make some guesses in an attempt to fix *that*.
  #
  source = re.sub(r'([^\.]) (Also|And|Because|By contrast|But|'+\
                  r'Filling out|Here|Or)\b', \
                  r'\1. \2', source)
  source = re.sub(r'\b([Ii]t|[Tt]here)\?([ds])\b', r"\1'\2", source)

  #
  # If it's a period followed by a double quote,
  # theoretically we shouldn't need to do anything.
  # But NLTK gets confused (?!) so we still have to add a period...
  #
  source = re.sub(r'([\.!\?]")(\s)', r'\1.\2', source)

  return source


def reformat_input(f):
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

  for s in timing.sent_tokenizer.tokenize(source):
    s = re.sub(r'([\.!\?]"?)\.', r'\1', s)
    if state == STATE_TIMECODE_FOUND:
      timing.emit_segment(s)
    else:
      print s


def main(args):
  # FIXME - Stupid unicode workaround, thanks to Anne Lambert
  # https://class.coursera.org/nlp/forum/thread?thread_id=1849
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')

  if len(args) == 0:
    reformat_input(sys.stdin)
  else:
    for file in args:
      reformat_input(open(file, 'r'))

if __name__ == '__main__':
  args = sys.argv[1:]
  main(args)
