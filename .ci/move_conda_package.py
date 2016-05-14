"""
Pulled from https://github.com/rmcgibbo/python-appveyor-conda-example/blob/master/continuous-integration/move-conda-package.py
"""
import sys
import os
import yaml
import glob
import shutil
from conda_build.config import config


def _main(recipe_dir):
    recipe_meta = os.path.join(recipe_dir, 'meta.yaml')
    with open(recipe_meta) as rm:
        package_name = yaml.load(rm)['package']['name']

    binary_package_glob = '{0}*.tar.bz2'.format(package_name)
    binary_package_glob = os.path.join(config.bldpkgs_dir, binary_package_glob)

    binary_package = glob.glob(binary_package_glob)[0]

    shutil.move(binary_package, '.')


if __name__ == '__main__':
    _recipe_dir = sys.argv[1]

    _main(_recipe_dir)
