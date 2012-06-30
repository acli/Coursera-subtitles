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
Turns out that the killer difference that decreased conversion
was adding a box for the coupon code,
because many people, when they see a coupon code,
will then search on the web [and] try to find coupons for that.
A lot of those folks will not return
to buy what they were just about to [buy] a moment ago.

Here’s an article reporting how Expedia ran into a similar problem
where, by simply adding a field with “company name,”
that had a dramatic decrease in the conversions on their website.

And these changes may seem trivial;
but, again, at scale, they can have a dramatic impact.

And then these underscore the point that small distractions —
like extra fields — can have a big impact of your site’s performance;
and, conversely, if you get the small things right,
you can have a dramatic *positive* impact.
Here’s a nice example from Ron Kohavi again.

These are two versions of Feedback from Microsoft Office.
The difference between the two is that
the first one shows both the qualitative and quantitative on the same screen —
stars and reason —;
the second one, subtlely but importantly, separates them in time,
so that what you first see is just a number of stars,
and you next see is the qualitative feedback.
And shifting to this two-staged feedback doubles the response rate.

But Microsoft designers weren’t done yet.
They wondered whether they can increase things even more.
So here’s a version — we’ll call this version C —
and what it does is,
as opposed to having five stars, we have three buttons,
“Yes,” “No,” and “I don’t know.”
And then we have the same two-stage feedback strategy as before
except the prompt, in this case, is customized to the button that you clicked.
So, we have simplified the number of options for the feedback,
and we’ve customized the prompt.
Making these small changes
increases the rate of feedback by a three-and-a-half-fold.

This feedback example illustrates two important points:
The first of them is a psychological principle called “commitment escalation,”
that, if you are [to] get somebody to do a bit
and then add a little bit more later on,
they’re much more likely than if you made the big ask up front.
And interfaces that get this right can reap the rewards.

The second that we’re seeing is that
phenomena like commitment escalation are subtle,
and fine-tuning it to exactly your circumstances will take some work.
And so what we’re seeing is that
by combining iterative design and controlled experimentation,
you can dial in these phenomena
to make your site work most effectively.
By now I bet you’re really excited
about the opportunity for running experiments online.
And so, in the next video,
we’ll talk about general techniques for being able to do this effect[ively].

(1031 words in 6:18)
