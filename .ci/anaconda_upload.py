"""
Pulled from https://github.com/rmcgibbo/python-appveyor-conda-example/blob/master/continuous-integration/binstar-push.py
"""
import os
import sys
import glob
import subprocess


def _main(*labels):
    token = os.environ['BINSTAR_TOKEN']
    packages = glob.glob('*.tar.bz2')

    if packages:
        print('Uploading {0}'.format(', '.join(packages)))
    else:
        raise RuntimeError('Upload Failed: No packages found.')

    cmd = [
        'anaconda',
        '-t', token,
        'upload',
        '--label', ' '.join(labels),
        '--force']
    cmd.extend(packages)

    error = None
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        error = 'binstar cmd failed: {0}'.format(e)
        error = error.replace(token, '*' * len(token))

    if error:
        raise RuntimeError(error)


if __name__ == '__main__':
    try:
        _labels = sys.argv[1:]
    except IndexError:
        exit(1)
    _main(*_labels)
