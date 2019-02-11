from setuptools import setup

APP = ['SkeleType.py']
DATA_FILES = ['blockdefinitions.py','rubik.py']
OPTIONS = {
     'argv_emulation': True,
     'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)