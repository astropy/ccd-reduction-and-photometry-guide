
import numpy as np

from astropy.modeling.models import Gaussian2D, MexicanHat2D, Const2D
from photutils.datasets import (make_random_gaussians_table,
                                make_gaussian_sources_image)
from photutils.aperture import EllipticalAperture


def read_noise(image, amount, gain=1):
    """
    Generate simulated read noise.

    Parameters
    ----------

    image: numpy array
        Image whose shape the noise array should match.
    amount : float
        Amount of read noise, in electrons.
    gain : float, optional
        Gain of the camera, in units of electrons/ADU.
    """
    shape = image.shape

    noise = np.random.normal(scale=amount / gain, size=shape)

    return noise


def bias(image, value, realistic=False):
    """
    Generate simulated bias image.

    Parameters
    ----------

    image: numpy array
        Image whose shape the bias array should match.
    value: float
        Bias level to add.
    realistic : bool, optional
        If ``True``, add some clomuns with somewhat higher bias value
        (a not uncommon thing)
    """
    # This is the whole thing: the bias is really suppose to be a constant
    # offset!
    bias_im = np.zeros_like(image) + value

    # If we want a more realistic bias we need to do a little more work.
    if realistic:
        shape = image.shape
        number_of_colums = 5

        # We want a random-looking variation in the bias, but unlike the
        # readnoise the bias should *not* change from image to image, so we
        # make sure to always generate the same "random" numbers.
        rng = np.random.RandomState(seed=8392)  # 20180520
        columns = rng.randint(0, shape[1], size=number_of_colums)
        # This adds a little random-looking noise into the data.
        col_pattern = rng.randint(0, int(0.1 * value), size=shape[0])

        # Make the chosen columns a little brighter than the rest...
        for c in columns:
            bias_im[:, c] = value + col_pattern

    return bias_im


def dark_current(image, current, exposure_time, gain=1.0, hot_pixels=False):
    """
    Simulate dark current in a CCD, optionally including hot pixels.

    Parameters
    ----------

    image : numpy array
        Image whose shape the cosmic array should match.
    current : float
        Dark current, in electrons/pixel/second, which is the way
        manufacturers typically report it.
    exposure_time : float
        Length of the simulated exposure, in seconds.
    gain : float, optional
        Gain of the camera, in units of electrons/ADU.
    hot_pixels : bool, optional
        If ``True``, add hot pixels to the image.

    Returns
    -------

    numpy array
        An array the same shape and dtype as the input containing dark counts
        in units of ADU.
    """

    # dark current for every pixel; we'll modify the current for some pixels if
    # the user wants hot pixels.
    base_current = current * exposure_time / gain

    # This random number generation should change on each call.
    dark_im = np.random.poisson(base_current, size=image.shape)

    if hot_pixels:
        # We'll set 0.01% of the pixels to be hot; that is probably too high
        # but should ensure they are visible.
        y_max, x_max = dark_im.shape

        n_hot = int(0.0001 * x_max * y_max)

        # Like with the bias image, we want the hot pixels to always be in the
        # same places (at least for the same image size) but also want them to
        # appear to be randomly distributed. So we set a random number seed to
        # ensure we always get the same thing.
        rng = np.random.RandomState(16201649)
        hot_x = rng.randint(0, x_max, size=n_hot)
        hot_y = rng.randint(0, y_max, size=n_hot)

        hot_current = 10000 * current

        dark_im[[hot_y, hot_x]] = hot_current * exposure_time / gain

    return dark_im


def sky_background(image, sky_counts, gain=1):
    """
    Generate sky background, optionally including a gradient across the
    image (because some times Moons happen).

    Parameters
    ----------

    image : numpy array
        Image whose shape the cosmic array should match.
    sky_counts : float
        The target value for the number of counts (as opposed to electrons or
        photons) from the sky.
    gain : float, optional
        Gain of the camera, in units of electrons/ADU.
    """
    sky_im = np.random.poisson(sky_counts * gain, size=image.shape) / gain

    return sky_im


def stars(image, number, max_counts=10000, gain=1):
    """
    Add some stars to the image.
    """
    # Most of the code below is a direct copy/paste from
    # https://photutils.readthedocs.io/en/stable/_modules/photutils/datasets/make.html#make_100gaussians_image

    flux_range = [max_counts / 10, max_counts]

    y_max, x_max = image.shape
    xmean_range = [0.1 * x_max, 0.9 * x_max]
    ymean_range = [0.1 * y_max, 0.9 * y_max]
    xstddev_range = [4, 4]
    ystddev_range = [4, 4]
    params = dict([('amplitude', flux_range),
                   ('x_mean', xmean_range),
                   ('y_mean', ymean_range),
                   ('x_stddev', xstddev_range),
                   ('y_stddev', ystddev_range),
                   ('theta', [0, 2 * np.pi])])

    sources = make_random_gaussians_table(number, params,
                                          random_state=12345)

    star_im = make_gaussian_sources_image(image.shape, sources)

    return star_im


def make_cosmic_rays(image, number, strength=10000):
    """
    Generate an image with a few cosmic rays.

    Parameters
    ----------

    image numpy array
        Image whose shape the cosmic array should match.
    number: float
        Number of cosmic rays to add to the image.
    strength : float, optional
        Pixel count in the cosmic rays.
    """

    cr_image = np.zeros_like(image)

    # Yes, the order below is correct. The x axis is the column, which
    # is the second index.
    max_y, max_x = cr_image.shape

    # Get the smallest dimension to ensure the cosmic rays are within the image
    maximum_pos = np.min(cr_image.shape)
    # These will be center points of the cosmic rays, which we place away from
    # the edges to ensure they are visible.
    xy_cr = np.random.randint(0.1 * maximum_pos, 0.9 * maximum_pos,
                              size=[number, 2])

    cr_length = 5  # pixels, a little big
    cr_width = 2
    theta_cr = 2 * np.pi * np.random.rand()
    apertures = EllipticalAperture(xy_cr, cr_length, cr_width, theta_cr)
    masks = apertures.to_mask(method='center')
    for mask in masks:
        cr_image += strength * mask.to_image(shape=cr_image.shape)

    return cr_image


# Functions related to simulated flat images

def make_one_donut(center, diameter=10, amplitude=0.25):
    sigma = diameter / 2
    mh = MexicanHat2D(amplitude=amplitude,
                      x_0=center[0], y_0=center[1],
                      sigma=sigma)
    gauss = Gaussian2D(amplitude=amplitude,
                       x_mean=center[0], y_mean=center[1],
                       x_stddev=sigma, y_stddev=sigma)
    return Const2D(amplitude=1) + (mh - gauss)


def add_donuts(image, number=20):
    """
    Create a transfer function, i.e. matrix by which you multiply
    input counts to obtain actual counts.

    Parameters
    ----------


    image : numpy array
        Image whose shape the cosmic array should match.

    number : int, optional
        Number of dust donuts to add.
    """

    y, x = np.indices(image.shape)

    # The dust donuts should always be in the same place...
    rng = np.random.RandomState(43901)
    shape = np.array(image.shape)
    border_padding = 50

    # We'll make the dust specks range from 1% to 5% of the image size, but
    # only in a couple of sizes. The dust grains themselves are fairly uniform
    # in size (I think), and there are only a fwe elements on which dust can
    # settle. Size on the image is determined by size of the dust and how far
    # it is from the CCD chip.

    min_diam = int(0.02 * shape.max())
    max_diam = int(0.05 * shape.max())

    # Weight towards the smaller donuts because it looks more like real flats..
    diameters = rng.choice([min_diam, min_diam, min_diam, max_diam],
                           size=number)

    # Add a little variation in amplitude
    amplitudes = rng.normal(0.25, 0.05, size=number)
    center_x = rng.randint(border_padding,
                           high=shape[1] - border_padding, size=number)
    center_y = rng.randint(border_padding,
                           high=shape[0] - border_padding, size=number)
    centers = [[x, y] for x, y in zip(center_x, center_y)]

    donut_model = make_one_donut(centers[0], diameter=diameters[0],
                                 amplitude=amplitudes[0])
    donut_im = donut_model(x, y)
    idx = 1
    for center, diam, amplitude in zip(centers[1:],
                                       diameters[1:],
                                       amplitudes[1:]):
        idx += 1
        donut_model = make_one_donut(center, diameter=diam,
                                      amplitude=amplitude)
        donut_im += donut_model(x, y)

    donut_im /= number

    return donut_im


def sensitivity_variations(image, vignetting=True, dust=True):
    """
    Create a transfer function, i.e. matrix by which you multiply input
    counts to obtain actual counts.

    Parameters
    ----------


    image : numpy array
        Image whose shape the cosmic array should match.

    vignetting : bool, optional
        If ``True``, darken image near corners.

    dust : bool, optional
        If ``True``, add some plausible-looking dust.
    """

    sensitivity = np.zeros_like(image) + 1.0
    shape = np.array(sensitivity.shape)

    if dust or vignetting:
        # Yes, this should be y, x.
        y, x = np.indices(sensitivity.shape)

    if vignetting:
        # Generate very wide gaussian centered on the center of the image,
        # multiply the sensitivity by it.
        vign_model = Gaussian2D(amplitude=1,
                                x_mean=shape[0] / 2, y_mean=shape[1] / 2,
                                x_stddev=2 * shape.max(),
                                y_stddev=2 * shape.max())
        vign_im = vign_model(x, y)
        sensitivity *= vign_im

    if dust:
        dust_im = add_donuts(image, number=40)
        dust_im = dust_im / dust_im.max()
        sensitivity *= dust_im

    return sensitivity
