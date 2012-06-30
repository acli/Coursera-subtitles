I really like this example
because it illustrates the kind of experiments
that you can easily do on your own.
And it also shows how, in this case,
by making the imperative vocabulary stronger —
“Follow me,” or even “You should follow me” —
we see an increase in clickthrough rate:
The clearer you make what users ought to do,
the more users click through.

Ron Kohavi has been a leading expert
for controlled experimentation for a number of years,
and I’d like to share with you a couple of examples from his research.
He’s currently at Microsoft,
and here’s a simple example from search results
that shows how imperceptible changes to an individual
can aggregate to yield phenomena that you can measure.

Here you can see two versions of search results,
one which is slightly typographically crisper than the other one —
you may not even notice the difference at all.
However, this difference, which is below your conscious level,
increases the number of query per user by 0.9%
and the number of ad clicks per user increases 3%.
At the scale that Microsoft and the other large search [carriers] operate,
this is a *huge* change.
And I think this is a nice example of how, in general,
the giant scale of experiments that you can conduct on the web
makes small but consequential differences detectable —
things which we’d never see in the lab
you can now investigate.
Also, it’s an example of how changes
which are too small to matter for a couple of people —
If you are building search results for 10 users,
a 0.9% change might not be something you’d worry about;
however, the impact of these changes accumulates
when the number of users increases to the scale of the web.

It *is* worth mentioning that some of the changes that you may see
might in fact be anomalies rather than real changes.
For example, aggregating results on a month-by-month basis
may make February or shorter months seem like down months —
in reality they just have fewer days.
Or, the day that you switched to daylight-savings time,
[you] may see a dip in March;
the day that you switched *from* daylight-savings time —
which has an extra hour —, you may see an increase.
So be careful about these variations
which may just be an artefact of your measuring tool.
It’s another reason why it’s important to run real manipulations.
Correlations can of course tell you a lot,
but the manipulations help you avoid many of these data anomalies.

All of the examples we’ve seen so far
show a case where the designer *intended* to create a new variation
and then measured the impact.
And then this is: That’s great.
It’s also important to pay attention to your measurements
even for design changes that you’d think *won’t* have any impact.

Here’s an example of a shopping cart from Greg Linden’s blog,
where, on the left, we have a page that yielded a large number of conversions;
on the right, what was intended to be a routine change
dropped the number of conversions precipitously.
Why?
I’ll give you a moment to think about it.

Since a number of variables changed at once,
it took a little bit of work to figure out
which of these five design changes
was the one which actually made the difference.
