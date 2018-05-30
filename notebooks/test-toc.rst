`Preface <00.00-Preface.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`1. Understanding an astronomical CCD image <01.00-Understanding-an-astronomical-CCD-image.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Construction of an artificial (but realistic)
   image <01.04-Construction-of-an-artificial-(but-realistic)-image.ipynb>`__
-  `Calibration overview <01.05-Calibration-overview.ipynb>`__
-  `Image combination <01.06-Image-combination.ipynb>`__
-  `Calibration choices you need to
   make <01.07-Calibration-choices-you-need-to-make.ipynb>`__
-  `Reading images <01.08-reading-images.ipynb>`__

`2. Handling overscan, trimming, and bias subtraction <02.00-Handling-overscan,-trimming,-and-bias-subtraction.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Inspect your images and make a choice about next
   steps <02.01-Inspect-your-images-and-make-a-choice-about-next-steps.ipynb>`__
-  `Subtract overscan, if
   desired <02.02-Subtract-overscan,-if-desired.ipynb>`__
-  `Trim, if needed <02.03-Trim,-if-needed.ipynb>`__
-  `Combine bias images to make
   master <02.04-Combine-bias-images-to-make-master.ipynb>`__

`3. Dark current and hot pixels <03.00-Dark-current-and-hot-pixels.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `The ideal case: your dark frames measure dark current, which scales
   linearly with
   time <03.01-The-ideal-case:-your-dark-frames-measure-dark-current,-which-scales-linearly-with-time.ipynb>`__
-  `Reality: most of your dark frame is noise and not all of the time
   dependent artifacts are dark
   current <03.02-Reality:-most-of-your-dark-frame-is-noise-and-not-all-of-the-time-dependent-artifacts-are-dark-current.ipynb>`__
-  `Identifying hot pixels <03.03-Identifying-hot-pixels.ipynb>`__
-  `Make a choice about next steps for
   darks <03.04-Make-a-choice-about-next-steps-for-darks.ipynb>`__
-  `Subtract bias, if
   necessary <03.05-Subtract-bias,-if-necessary.ipynb>`__

`4. Interlude: Image masking <04.00-Interlude:-Image-masking.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Identifying bad pixels <04.01-Identifying-bad-pixels.ipynb>`__
-  `Creating a mask <04.02-Creating-a-mask.ipynb>`__
-  `incorporating the mask in
   reduction <04.03-incorporating-the-mask-in-reduction.ipynb>`__

`5. Flat corrections <05.00-Flat-corrections.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `There are no perfect
   flats <05.01-There-are-no-perfect-flats.ipynb>`__
-  `Make a choice about next steps for
   flats <05.02-Make-a-choice-about-next-steps-for-flats.ipynb>`__
-  `Calibrating the flats <05.03-Calibrating-the-flats.ipynb>`__
-  `Combining flats <05.04-Combining-flats.ipynb>`__

`Reducing science images <06.00-Reducing-science-images.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Initial reduction <06.01-Initial-reduction.ipynb>`__
-  `Cosmic ray removal <06.02-Cosmic-ray-removal.ipynb>`__

`7. Combining images <07.00-Combining-images.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Combine without aligning to create a sky
   flat <07.01-Combine-without-aligning-to-create-a-sky-flat.ipynb>`__
-  `Combination with alignment via
   WCS <07.02-Combination-with-alignment-via-WCS.ipynb>`__
-  `Combination with alignment based on star positions in the
   image <07.03-Combination-with-alignment-based-on-star-positions-in-the-image.ipynb>`__

######################################################################

`Preface <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/00.00-Preface.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`1. Understanding an astronomical CCD image <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.00-Understanding-an-astronomical-CCD-image.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Construction of an artificial (but realistic)
   image <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.04-Construction-of-an-artificial-(but-realistic)-image.ipynb>`__
-  `Calibration
   overview <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.05-Calibration-overview.ipynb>`__
-  `Image
   combination <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.06-Image-combination.ipynb>`__
-  `Calibration choices you need to
   make <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.07-Calibration-choices-you-need-to-make.ipynb>`__
-  `Reading
   images <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.08-reading-images.ipynb>`__

`2. Handling overscan, trimming, and bias subtraction <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/02.00-Handling-overscan,-trimming,-and-bias-subtraction.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Inspect your images and make a choice about next
   steps <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/02.01-Inspect-your-images-and-make-a-choice-about-next-steps.ipynb>`__
-  `Subtract overscan, if
   desired <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/02.02-Subtract-overscan,-if-desired.ipynb>`__
-  `Trim, if
   needed <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/02.03-Trim,-if-needed.ipynb>`__
-  `Combine bias images to make
   master <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/02.04-Combine-bias-images-to-make-master.ipynb>`__

`3. Dark current and hot pixels <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/03.00-Dark-current-and-hot-pixels.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `The ideal case: your dark frames measure dark current, which scales
   linearly with
   time <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/03.01-The-ideal-case:-your-dark-frames-measure-dark-current,-which-scales-linearly-with-time.ipynb>`__
-  `Reality: most of your dark frame is noise and not all of the time
   dependent artifacts are dark
   current <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/03.02-Reality:-most-of-your-dark-frame-is-noise-and-not-all-of-the-time-dependent-artifacts-are-dark-current.ipynb>`__
-  `Identifying hot
   pixels <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/03.03-Identifying-hot-pixels.ipynb>`__
-  `Make a choice about next steps for
   darks <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/03.04-Make-a-choice-about-next-steps-for-darks.ipynb>`__
-  `Subtract bias, if
   necessary <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/03.05-Subtract-bias,-if-necessary.ipynb>`__

`4. Interlude: Image masking <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/04.00-Interlude:-Image-masking.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Identifying bad
   pixels <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/04.01-Identifying-bad-pixels.ipynb>`__
-  `Creating a
   mask <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/04.02-Creating-a-mask.ipynb>`__
-  `incorporating the mask in
   reduction <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/04.03-incorporating-the-mask-in-reduction.ipynb>`__

`5. Flat corrections <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.00-Flat-corrections.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `There are no perfect
   flats <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.01-There-are-no-perfect-flats.ipynb>`__
-  `Make a choice about next steps for
   flats <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.02-Make-a-choice-about-next-steps-for-flats.ipynb>`__
-  `Calibrating the
   flats <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.03-Calibrating-the-flats.ipynb>`__
-  `Combining
   flats <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/05.04-Combining-flats.ipynb>`__

`Reducing science images <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/06.00-Reducing-science-images.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Initial
   reduction <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/06.01-Initial-reduction.ipynb>`__
-  `Cosmic ray
   removal <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/06.02-Cosmic-ray-removal.ipynb>`__

`7. Combining images <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/07.00-Combining-images.ipynb>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Combine without aligning to create a sky
   flat <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/07.01-Combine-without-aligning-to-create-a-sky-flat.ipynb>`__
-  `Combination with alignment via
   WCS <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/07.02-Combination-with-alignment-via-WCS.ipynb>`__
-  `Combination with alignment based on star positions in the
   image <http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/07.03-Combination-with-alignment-based-on-star-positions-in-the-image.ipynb>`__
