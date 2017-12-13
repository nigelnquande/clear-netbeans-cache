from distutils.core import setup
from glob import glob
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options={'py2exe': {'bundle_files': 2, 'compressed': True, "optimize": 2, "dist_dir": "bin"}},
    console=[{'script': "clear_nb_cache.py", "dest_base": "clear_nb_cache", "icon_resources": [(1, "imgs/clear_nb.ico")],}],
    zipfile=None,
    data_files = [('imgs', ['./imgs/clear_nb.ico'])],
)
