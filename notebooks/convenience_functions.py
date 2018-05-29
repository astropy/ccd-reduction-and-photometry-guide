from astropy import visualization as aviz
from astropy.nddata.utils import block_reduce
from matplotlib import pyplot as plt

def show_image(image, percl=99, percu=None, figsize=(6, 10), cmap='viridis', log=False):
    """
    Show an image in matplotlib with some basic astronomically-appropriat stretching.
    
    Parameters
    ----------
    image
        The image to show 
    percl : number
        The percentile for the lower edge of the stretch (or both edges if ``percu`` is None)
    percu : number or None
        The percentile for the upper edge of the stretch (or None to use ``percl`` for both)
    figsize : 2-tuple
        The size of the matplotlib figure in inches
    """ 
    if percu is None:
        percu = percl
        percl = 100-percl
        
    if figsize is not None:
        # Rescale the fig size to match the image dimensions, roughly
        image_aspect_ratio = image.shape[0]/image.shape[1]
        figsize = (max(figsize) * image_aspect_ratio, max(figsize))
        
    fig, ax = plt.subplots(1,1, figsize=figsize)
    
    # To preserve details we should *really* downsample correctly and not rely on 
    # matplotlib to do it correctly for us (it won't).
    
    # So, calculate the size of the figure in pixels, block_reduce to roughly that,
    # and display the block reduced image.
    
    # Thanks, https://stackoverflow.com/questions/29702424/how-to-get-matplotlib-figure-size
    fig_size_pix = fig.get_size_inches() * fig.dpi
    
    ratio = (image.shape // fig_size_pix).max()
    
    if ratio < 1:
        ratio = 1
        
    # Divide by the square of the ratio to keep the flux the same in the reduced image
    reduced_data = block_reduce(image, ratio) / ratio**2

    # Of course, now that we have downsampled, the axis limits are changed to match
    # the smaller image size. Setting the extent will do the trick to change the axis display
    # back to showing the actual extent of the image.
    extent = [0, image.shape[1], 0, image.shape[0]]
    if log:
        stretch = aviz.LogStretch()
    else:
        stretch = aviz.LinearStretch()
    norm = aviz.ImageNormalize(reduced_data, interval=aviz.AsymmetricPercentileInterval(percl, percu), 
                                      stretch=stretch)

    plt.colorbar(ax.imshow(reduced_data, norm=norm, origin='lower', cmap=cmap, extent=extent))