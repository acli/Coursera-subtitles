What is this:
============

In the `scripts` directory you will find two scripts:

- `extract-text-from-srt` strips out time codes and outputs the
  results to standard output. This is a sed script that has been
  written on MacOS X and I haven’t tested it on other systems
  (not even Linux).

- `reformat-extracted-text` attempts to reformat the output of
  `extract-text-from-srt` so that the subtitles will make more
  sense for people who speak English; this is also sent to
  standard output.

The canonical way to run this is to feed `extract-text-from-srt`
an SRT file that you got from Amara, then pipe this to
`reformat-extracted-text` and then redirect this to a text file.
Then you can proofread the text file, copy-and-paste it back to
Amara (restarting step 1), and then continue on to steps 2 through 4.

Note that `reformat-extracted-text` is not a particularly
intelligent piece of software. You *will* need to review the
output it gives you; but in general what it gives you should
at least be better than stock stanford-bot (Cogi) output.

Things to watch out for if you want to work on Coursera’s subtitles:
===================================================================

June 12, 2012:

As of June 12, 2012, subtitling support on Amara is not working.
You have only one go to finish the whole transcript (i.e., Save
and Exit no longer works), but even if you manage to do that,
the system will still erroneously mark your finished subtitles
as a draft and you will not be able to do anything about it
until the bot comes along and overwrite your finished work. This
has been reported to Amara but I am not sure when this can be
fixed.

The interim workaround is that after you have finished a draft
or a completed transcript, download the SRT file, and then
upload the *same* SRT file back onto Amara. This will reactivate
the “Modify these subtitles” link and allow you to continue
with your subtitling.

(updated June 13, 2012)

These are not obvious, and I found them out the hard way, If you
haven’t started yet, then it’d be better to know them before you
start.

1. A program called stanford-bot will attempt to automatically
   generate a transcript, presumably with speech recognition
   technology. This transcript is always generated.

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

4. Avoid Universal Subtitles’ “upload transcript” function,
   and do not use it if *anyone* has uploaded a translation.
   Otherwise you will screw up the revision history and you
   will regret it afterwards.
   (Note that uploading an SRT of a *translation* is, however,
    apparently safe.)

5. The accuracy of the English transcript is paramount. It is
   in fact extremely important to get it right, because it will
   be used as the basis for non-English subtitles.

Note: A couple of scripts to faciliate step 3 can be found in
the scripts directory of this repo.

List of videos:
==============

(Needed back when Universal Subtitles didn’t provide a way to give
you a list of all videos you have done)

Here are a collection of all the subtitles I have done or QA’d
for the Coursera classes I have taken.  For some of my thoughts
on this whole exercise (of transcribing lectures), please head
over to http://w.gniw.ca/?p=735

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
- http://www.universalsubtitles.org/fr/videos/4e1VKeiCW3BD/en/325004/ (HCI 6.1)
- http://www.universalsubtitles.org/fr/videos/J4g1fGjMz6BN/en/325002/ (HCI 6.2)
- http://www.universalsubtitles.org/fr/videos/GMB76WUpPRAc/en/325001/ (HCI 6.3)

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

- To get all HCI videos properly transcribed, as I am nominally enrolled;
  though I have already given up on the studio track (primarily due to
  disillusionment and not due to workload).

- If time permits, to get at least the SaaS videos either transcribed
  (this would mean the instructor chats) or properly QA’d.

If you have the time and have good ears and good editorial intuition,
you are welcome to join in to fix this big mess created by the machine
transcription software “stanford-bot.” Machine transcription of lectures
really doesn’t work, especially when the transcripts are being used as
a basis for further translations — they simply contain too many errors,
sometimes to the point of saying the opposite of what’s actually said.

