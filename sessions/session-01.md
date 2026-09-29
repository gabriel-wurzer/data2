# Session 1: What a machine means when it says it learns

259.075 Data-integrated Algorithmic Design Processes II
Friday, 9 October 2026, 09:00 to 11:00, EDV-Labor PC5

Take a building in Vienna, say a corner house in the seventh district, and ask what it needs
for heating. The usual way to answer takes an afternoon: you enter the geometry, the wall
build-ups, the windows, you run a simulation, you get a number. Do that for a hundred design
variants and you have spent a month.

> A model is a fast answer to a question that used to be slow.

We will spend the term building something that answers in a millisecond instead, well enough
to be useful while you are still drawing. Today we build the smallest such thing there is:
one number in, one number out, and a rule in between that the machine finds by itself.

A word on the data before we start. The buildings are from the open data of the City of
Vienna, layer `GEBAEUDETYPOGD`, one polygon per building with its construction period. The
heating demand is not. No open dataset in Vienna gives measured consumption per building, so
the target value in our table comes from a formula that combines the wall U-value of the
construction period with the shape of the footprint. This matters more than it sounds, and
we come back to it at the end of the session.

## Guessing first

Open `01_neuron.ipynb` and run the first two cells. You get a scatter plot: one point per
building, compactness on the horizontal axis, heating demand on the vertical.

Compactness is the perimeter of the footprint divided by the square root of its area. A round
building sits at 3.5, a long slab is far above that. Hover over a few points and look at what
kind of houses they are.

> Compactness: perimeter divided by the square root of area. Dimensionless, so a small shed
> and a large block can be compared.

Now put a line through that cloud by hand. The next cell gives you a slider for the slope
`w`; the intercept `b` stays fixed for the moment. The line moves with the slider and the
title shows one number, the mean squared error, which is the average of the squared vertical
distances between your line and the points. Find the smallest value you can and write it
down. We will need it in twenty minutes.

You have just done, with your hand and your eye, what the rest of this session automates.

## The neuron

The line you were moving is

    hwb = w · compactness + b

and in the language of the field this is a *neuron*: inputs, one weight per input, a bias
term, an output. Nothing more. Every network you will meet later, including the ones that
draw pictures, is built from this.

The error you were minimising has a name too. Squaring the distances punishes a few large
mistakes more than many small ones, which is a choice, not a law; other choices exist and we
will meet one in session 6.

## Downhill in the dark

Move the slider two steps to the right and watch the error. If it grows, you went the wrong
way; if it falls, keep going. That rule is enough to find the minimum, and it does not
require you to know anything about the shape of the error landscape. You only need to know
whether it goes up or down from where you stand.

> The slope of the error at your current position has a name: the gradient. It tells you
> which way is downhill, nothing else.

The notebook plots that landscape for you, first as a curve over `w`, then as a surface over
`w` and `b`. Turn it until you see the valley from the side. It is narrow and it lies at an
angle, and that will cost us dearly in a minute.

The derivation of the gradient for this model is in the notebook as a collapsible cell. Open
it if you want it; it is not examined. What you need is the line of code, and it is given.

## Your part

The loop is yours. The scaffold is there, the gradient is there, and two lines are missing:
one step against the gradient for `w`, one for `b`. The step length is called the *learning
rate*.

Run it. The error falls, slowly, and after three thousand steps you land at `w = 8.5` and
`b = 111`. Then set the learning rate to 0.04 and run it again. The error explodes, and the
loss curve, plotted logarithmically, shoots off the top of the plot. Both runs go into your
submission.

> If the loss curve rises, your learning rate is too large. This is the most common failure
> in the whole field.

Three thousand steps for a straight line is embarrassing, and the reason is the narrow
valley you turned around earlier. Those of you who finish early: compute the exact solution
by least squares, compare it with what the loop found, and think about why the loop took so
long. We deal with it properly in session 2.

## What the model actually learned

The error stops at 23.7 and no amount of patience brings it lower. That is not the fault of
the loop. A building has more to it than the shape of its footprint, and the one thing that
matters most here, the U-value of the wall, is in the data but not in the model. Session 2
hands it to the model and the error collapses.

There is a second, less comfortable point. Look at the last map in the notebook, coloured by
residual: red where the model overestimates, blue where it underestimates. You will find a
pattern by construction period, and you should, because the target value was computed from
the construction period in the first place.

> Our model is learning a calculation rule that someone wrote down, not the behaviour of a
> house. Everything in this course stands or falls on the difference.

This is deliberate. A rule has no measurement error, so everything we do in the first weeks
can be checked exactly. From session 3 on we add noise, and from there the difference between
signal and accident is the whole problem.

## Before Friday

Log in to the hub once and run `00_check.ipynb`. It tests that the environment, the data and
the test runner are in place, nothing else. If it fails, send the error message; we fix it
before the session, not during it. Whoever still cannot log in on Friday works in pairs at
one machine.

## Submission, due Thursday 23:59

The notebook, with the two missing lines filled in, one stable and one divergent run, and
five sentences on what the fitted parameters mean in building terms. The grading criteria are
in the assignment sheet: order of magnitude, sign and physical plausibility, units, limits of
validity, one named source of error, one design consequence. One point each, and the code is
worth four.

The tests are not hidden. They are in the notebook, they are the same ones the grader uses,
and you can call the grading run before the deadline. See `kursregeln.md` for what happens if
you get stuck: the solution to the two lines is released after ten minutes, without asking
and without penalty.
