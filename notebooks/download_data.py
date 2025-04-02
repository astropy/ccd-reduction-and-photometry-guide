from pathlib import Path
import shutil
import tarfile

from astropy.utils.data import download_file

def move(p : Path, dest : str):
    try:
        p.rename(dest)
    except OSError:
        shutil.move(p, dest)

    return Path(dest).exists()


def get_data(record : str, file_name : str, unzip=False):
    """
    Get a blob from Zenodo and either move it or unzip it.

    Parameters
    ----------
    record : str
        The Zenodo record number.

    file_name : str
        The file name to download.

    """
    url = f'https://zenodo.org/record/{record}/files/{file_name}?download=1'
    print(f"\nDownloading {file_name}")
    download = download_file(url, show_progress=True)
    p = Path(download)
    if p.exists():
        print(f"File {p} successfully downloaded.")
    else:
        raise RuntimeError(f"File {p} not downloaded.")

    if unzip:
        print(f"Unzipping {file_name}")
        tarball = tarfile.open(download)
        tarball.extractall('.')
        dir_name = file_name.split('.')[0]
        p = Path(dir_name)
        if p.exists():
            print(f"File {p} successfully unzipped.")
        else:
            raise RuntimeError(f"File {p} not unzipped.")
    else:
        moved = move(p, f'./{file_name}')
        if not moved:
            raise RuntimeError(f"File {file_name} not moved.")
        else:
            print(f"File {file_name} successfully moved.")


# Get single images
file_name = 'combined_bias_100_images.fit.bz2'
record = 3320113
get_data(record, file_name, unzip=False)

# raise RuntimeError("This is a test error to see if the notebook stops running.")

file_name = 'dark-test-0002d1000.fit.bz2'
record = 3312535
get_data(record, file_name, unzip=False)

file_name = "single_bias_thermoelectric.fit.bz2"
record = 5931364
get_data(record, file_name, unzip=False)

file_name = "combined_dark_300.000.fits.bz2"
record = 3332818
get_data(record, file_name, unzip=False)

file_name = "combined_dark_exposure_1000.0.fit.bz2"
record = 4302262
get_data(record, file_name, unzip=False)

# Get the tarball for the smaller example and extract it
file_name = "example-cryo-LFC.tar.bz2"
record = 3254683
get_data(record, file_name, unzip=True)


# Get the tarball for the bigger example and extract it
file_name = "example-thermo-electric.tar.bz2"
record = 3245296
get_data(record, file_name, unzip=True)
