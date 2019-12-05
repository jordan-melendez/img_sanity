from distutils.core import setup

setup(
    name='img_sanity',
    packages=['img_sanity'],
    version='0.1',
    author='Jordan Melendez',
    author_email='jmelendez1992@gmail.com',
    install_requires=[
        'dash>=1.7.0',
        'pandas',
        'plotly>=4.3.0',
    ]
)
