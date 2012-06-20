What is this:
============

In the `scripts` directory you will find:

- `reformat-extracted-text.py` attempts to reformat either an
  actual SRT file or the output of `old/extract-text-from-srt`
  so that the way the transcript is broken into subtitles will
  make more sense for people who speak English. The result of
  the reformatting is sent to standard output.

The script might have bugs as it is still a new rewrite.
The realigned timings are estimates only and they can be off
but should not be too out of whack.
However, sometimes it will still break the transcript in a sub-optimal way
and sometimes it may fail to find suitable break points.
As I continue using it I expect there to be some improvements.

In the `old` subdirectory inside `scripts` you can find two more scripts.
These are no longer used for my own workflow,
but you might still find them useful:

- `extract-text-from-srt` strips out time codes and outputs the
  results to standard output. This is a sed script that has been
  written on MacOS X and which has never been tested it on any other system
  (not even Linux).

- `reformat-extracted-text` attempts to reformat the output of
  `extract-text-from-srt` so that the subtitles will make more
  sense for people who speak English; this is also sent to
  standard output.

The canonical way to run this set of two scripts
is to feed `extract-text-from-srt`
an SRT file that you got from Amara, then pipe this to
`reformat-extracted-text` and then redirect this to a text file.
Then you can proofread the text file, copy-and-paste it back to
Amara (restarting step 1), and then continue on to steps 2 through 4
to produce a timecoded set of subtitles.

Note that `reformat-extracted-text` is not a particularly
intelligent piece of software. You *will* need to review the
output it gives you; but in general what it gives you should
at least be better than stock stanford-bot (Cogi) output.

There is also a third:

Things to watch out for if you want to work on Coursera’s subtitles:
===================================================================

June 12, 2012:

As of June 12, 2012, subtitling support on Amara is not working.
After exiting the editor (whether through Save and Exit or
Submit Your Work) the system will disable the “Modify these
subtitles” link and erroneously mark your finished subtitles
as a draft. You will not be able to do anything about it
until the bot comes along and overwrite your finished work. This
has been reported to Amara but I am not sure when this can be
fixed.

The interim workaround is that after you have finished a draft
or a completed transcript, download the SRT file, and then
upload the *same* SRT file back onto Amara (i.e., mimic the bot’s
behaviour). This will reactivate the “Modify these subtitles”
link and allow you to continue with your subtitling.

(updated June 14, 2012)

If you have the time and have good ears and good editorial intuition,
come, join in and work on the subtitles!
A speech recognition system has left a big mess
that can confuse and mislead students,
sometimes to the point of telling them the exact opposite of what’s being said.
Your mission is to slay the dragon and return peace to the land of Coursera :-)

Anyway, if you do help out,
there are some finer points that you need to be aware of.
These are not obvious, and I found them out the hard way, If you
haven’t started yet, then it’d be better to know them before you
start.

1. A program called stanford-bot will attempt to automatically
   generate a transcript, using speech recognition
   technology.
   (Note that the fact that this is indeed a speech recognition system
   has been confirmed through official Amara and Coursera bug
   reporting channels.)
   This transcript is always generated.

2. A corollary of the above is that if there are no subtitles
   when you start working, and still no subtitles when you
   finish, then be prepared that stanford-bot will overwrite
   your work. When this happens just revert back to your version,
   but only if your version is complete, i.e., only if it covers
   100% of the video.

3. However, if stanford-bot’s transcript is already present before
   you start, then depending on how perfectionist you are, you
   might want to just throw away its transcript, or at least
   reformat it before using. The transcript that it generates have
   very strange formatting that is very hard to work with, and the
   subtitles are cut off at very illogical places which require
   a lot of work to fix. It can get so bad that it takes as long
   to try to fix it as to throw it away and start over.

4. Avoid Amara’ “upload transcript” function,
   and do not use it if *anyone* has uploaded a translation.
   Otherwise you will screw up the revision history and you
   will regret it afterwards.
   (Note that uploading an SRT of a *translation* is, however,
    apparently safe.)

5. The accuracy of the English transcript is paramount. It is
   in fact extremely important to get it right, because it will
   be used as the basis for non-English subtitles.

If you are a Coursera student, you can also find these notes
[on the Coursera wiki][2].

List of videos:
==============

Here are a collection of all the subtitles I have done or QA’d
for the Coursera classes I have taken:

(This list is not currently exactly needed;
but it was back when you have no way to get such a list on Amara’s interface)

Transcribed from scratch:

- http://www.universalsubtitles.org/en/videos/vz9OvM97buqT/info/ (SaaS 5.8)
- http://www.universalsubtitles.org/fr/videos/RqPMqHtxcsbA/en/325911/ (HCI 1.2)
- http://www.universalsubtitles.org/fr/videos/hZbYw3S5emvp/en/325638/ (HCI 1.3)
- http://www.universalsubtitles.org/fr/videos/tJCi1dIa5lBJ/en/326521/ (HCI 1.4)
- http://www.universalsubtitles.org/fr/videos/xOoOaLfas4Mz/en/327172/ (HCI 2.3)
- http://www.universalsubtitles.org/fr/videos/Ccd5NxCIzc3v/en/328862/ (HCI 3.1)
- http://www.universalsubtitles.org/fr/videos/x1HgL7TWQEkw/en/329248/ (HCI 3.2)
- http://www.universalsubtitles.org/fr/videos/KK3G5CfxEMkK/en/330023/ (HCI 4.1)
- http://www.universalsubtitles.org/fr/videos/N3TqLfUnlrAg/en/330224/ (HCI 4.2)
- http://www.universalsubtitles.org/fr/videos/cCinMZkk8IfM/en/335507/ (HCI 7.2)
- http://www.universalsubtitles.org/fr/videos/bMF01JVrNxmV/en/337489/ (HCI 8.1)
- http://www.universalsubtitles.org/fr/videos/WBCHIQgmVtYu/en/337942/ (HCI 8.2)


Reformatting and QA of stanford-bot’s transcripts:

- http://www.universalsubtitles.org/en/videos/ayR3VR8BXJdL/info/ (models 9-2)
- http://www.universalsubtitles.org/fr/videos/4rCunfbLShfw/info/ (PGM 1-1)
- http://www.universalsubtitles.org/fr/videos/KUprgjyoAjfq/en/303905/ (NLP 17-3)
- http://www.universalsubtitles.org/fr/videos/vPfFsyG2H2w1/en/321441/ (NLP chat II)
- http://www.universalsubtitles.org/fr/videos/8qWn2qbDGOHI/en/325003/ (HCI 2.2)
- http://www.universalsubtitles.org/fr/videos/FZdagnyVGlGX/en/329585/ (HCI 3.3)
- http://www.universalsubtitles.org/fr/videos/wB9UdDAP8a5X/en/329502/ (HCI 3.4)
- http://www.universalsubtitles.org/fr/videos/P4C1NvtfhveB/en/335002/ (HCI 5.1)
- http://www.universalsubtitles.org/fr/videos/Nq8BVvfcrJMI/en/334621/ (HCI 5.2)
- http://www.universalsubtitles.org/fr/videos/DdShqs9hOPZk/en/334563/ (HCI 5.3)
- http://www.universalsubtitles.org/fr/videos/4e1VKeiCW3BD/en/325004/ (HCI 6.1)
- http://www.universalsubtitles.org/fr/videos/J4g1fGjMz6BN/en/325002/ (HCI 6.2)
- http://www.universalsubtitles.org/fr/videos/GMB76WUpPRAc/en/325001/ (HCI 6.3)
- http://www.universalsubtitles.org/fr/videos/rlfgSzTcqzTQ/en/336161/ (HCI 7.1)
- http://www.universalsubtitles.org/fr/videos/iNKD8Lv04vAM/en/336567/ (Soc 1-5)

QA of other transcriptionist’s work:

- http://www.universalsubtitles.org/fr/videos/ZEW0CIMyUoft/en/324971/ (HCI 1.1)

Minor revisions to transcripts already revised by other students:

- http://www.universalsubtitles.org/fr/videos/ZVF6pWv6LSlo/info/ (PGM) (2-8)
- http://www.universalsubtitles.org/fr/videos/JfejIomQXOV9/info/ (PGM)
- http://www.universalsubtitles.org/en/videos/tThIgKFLeJ7w/info/ (models)

TO DO:

- http://www.universalsubtitles.org/fr/videos/VbaciFSlgnqW/en/227447/ (NLP) (5-1)
- http://www.universalsubtitles.org/fr/videos/MQpvCWmjNXXC/en/226619/ (NLP) (4-8)

Current focus:
=============

- To get all HCI videos properly transcribed.

- If time permits, to get at least the SaaS videos either transcribed
  (this would mean the instructor chats) or properly QA’d.

See also:
========

1.  The [Video Subtitles][1] article on the Coursera wiki, where I wrote the whole [Finer Points][2] section.

2.  [Some thoughts on transcribing Coursera lectures][3] on my blog.

3.  [Some comments about Amara’s speech recognizer][4] on my blog.

[1]: https://share.coursera.org/wiki/index.php/Video_Subtitles
[2]: https://share.coursera.org/wiki/index.php/Video_Subtitles#Finer_Points
[3]: http://w.gniw.ca/?p=735
[4]: http://w.gniw.ca/?p=937
