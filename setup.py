from setuptools import setup  # Need this to handle modules

setup(
    name='spoonacular_script',
    version='0.0.1',
    packages=['core', 'tests'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.text').read(),
    entry_points={
        'console_scripts': [
            'spoonacular_script = app:main'
        ]
    }
)
