# Preface

# Understanding an astronomical CCD image

## Counts, photons and electrons
### Burp
## Not all counts are light
## Your detector is not ideal
## Construction of an artificial (but realistic) image
## Calibration overview
## Image combination
## Calibration choices you need to make

# Handling overscan, trimming, and bias subtraction

## Inspect your images and make a choice about next steps
## Subtract overscan, if desired
## Trim, if needed
## Combine bias images to make master

# Dark current and hot pixels

## The ideal case: your dark frames measure dark current, which scales linearly with time
## Reality: most of your dark frame is noise and not all of the time dependent artifacts are dark current
## Identifying hot pixels
## Make a choice about next steps for darks
## Subtract bias, if necessary

# Interlude: Image masking
## Identifying bad pixels
## Creating a mask
## incorporating the mask in reduction

# Flat corrections
## There are no perfect flats
## Make a choice about next steps for flats
## Calibrating the flats
### Subtract overscan and trim, if necessary
### Subtract bias, if necessary
### Subtract dark current, scaling if necessary (scale down when possible)
## Combining flats

# Reducing science images
## Initial reduction
### Subtract overscan and trim, if necessary
### Subtract bias, if necessary
### Subtract dark current, scaling if necessary (scale down when possible)
### Flat correct
## Cosmic ray removal

# Combining images
## Combine without aligning to create a sky flat
## Combination with alignment via WCS
## Combination with alignment based on star positions in the image


