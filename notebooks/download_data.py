from pathlib import Path
import tarfile

from astropy.utils.data import download_file

# Get single images
url = 'https://zenodo.org/record/3320113/files/combined_bias_100_images.fit.bz2?download=1'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('combined_bias_100_images.fit.bz2')

url = 'https://zenodo.org/record/3312535/files/dark-test-0002d1000.fit.bz2?download=1'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('dark-test-0002d1000.fit.bz2')

url = 'https://zenodo.org/record/5931364/files/single_bias_thermoelectric.fit.bz2?download=1'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('single_bias_thermoelectric.fit.bz2')

url = 'https://zenodo.org/record/3332818/files/combined_dark_300.000.fits.bz2?download=1'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('combined_dark_300.000.fits.bz2')

url = 'https://zenodo.org/record/4302262/files/combined_dark_exposure_1000.0.fit.bz2?download=1'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('combined_dark_exposure_1000.0.fit.bz2')

url = 'https://zenodo.org/records/10844909/files/TIC_125489084.01-S001-R055-C001-ip.fit.bz2?download=1'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('photometry/TIC_125489084.01-S001-R055-C001-ip.fit.bz2')

url = 'https://archive.stsci.edu/pub/hlsp/xdf/hlsp_xdf_hst_acswfc-60mas_hudf_f435w_v1_sci.fits'
download = download_file(url, show_progress=True)
p = Path(download)
p.rename('photometry/hlsp_xdf_hst_acswfc-60mas_hudf_f435w_v1_sci.fits')

# Get the tarball for the smaller example and extract it
url = 'https://zenodo.org/record/3254683/files/example-cryo-LFC.tar.bz2?download=1'
download = download_file(url, show_progress=True, cache=True)
tarball = tarfile.open(download)
tarball.extractall('.')

# Get the tarball for the bigger example and extract it
url = 'https://zenodo.org/record/3245296/files/example-thermo-electric.tar.bz2?download=1'
download = download_file(url, show_progress=True, cache=True)
tarball = tarfile.open(download)
tarball.extractall('.')
