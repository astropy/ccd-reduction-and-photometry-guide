---
note: The outline below is drawn from Massey 1997 guide to CCD Reductions
---

# Why your data needs work and what to do about it (not likely to redo exact details)

# Doing reduction

## Outline of reduction steps

I imagine this will be very similar except maybe for some terminology

## Examining frames to determine trim and bias

People should know they need to do this but they should also know to ask about the instrument they are using first.

## Setting things up: `setinstrument`, parameters of `ccdproc`, and ``ccdlist`

No clue what this is...

## Combining Bias Frames with `zerocombine`

Yeah, that is part of `ccdproc` and I don't think it needs that much emphasis?

## First pass through `ccdproc`

Need to read this...

## Constructing a bad pixel mask

## Dealing with The Darks

In my experience, and with electrically cooled CCDs (let alone ones in a cryo tank) the dark current is small *except* for some hot pixels. See the notebook I wrote looking at darks and how linear pixels are.

## Combining Flat-Field Exposures

Yikes....stay away from technique and hope we actually have some decent flats.

## Normalizing spectroscopic flats using `response`

That is likely beyond me.

## Flat-field division: `ccdproc` Pass 2

## Getting the Flat-Fielding Really RIght

### Combining the twilight/blank-sky flats

### Creating the Illumination Correction

## Finishing the flat-fielding

## Fixing bad pixels

# How many and what kind of calibratino frames do you need?

# INs and Outs of Combining Frames

Note there is a nice paper about image combination also that talks about clipping before combining.

# Summary of reduction steps

## Spectroscopic example
## Direct imaging example
