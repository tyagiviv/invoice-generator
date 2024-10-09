from setuptools import setup

APP = ['main.py']  # Main script for your application
DATA_FILES = [('resources', ['logo.png', 'invoice_number.json'])]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['reportlab', 'tkinter'],  # Add any other packages your app uses
    'includes': ['reportlab', 'tkinter'],
    'iconfile': 'logo.icns',
    'plist': {
        'CFBundleName': 'Invoice Generator',  # Name of  application
        'CFBundleVersion': '0.1',  # Version of  app
        'CFBundleShortVersionString': '0.1',  # Short version of  app
        'CFBundleIdentifier': 'com.vty.invoicegenerator',  # Unique identifier
    },
    'excludes': ['numpy', 'scipy'],  # Exclude any unnecessary packages to reduce size
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
