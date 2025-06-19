from setuptools import setup

OPTIONS = {
    'plist': {
        'LSUIElement': True  # This hides the dock icon
    }
}

setup(
    app=['menu_timer.py'],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)