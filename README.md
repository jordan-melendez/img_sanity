# img_sanity
View and filter images based on their important attributes.

# Installation

Clone the directory and `cd` into it. Then, in a virtual environment, run
```
pip install .
```
or, since there are likely to be updates soon, `pip install -e .`, since that will keep the package up to date upon pulling new changes.

# Usage

In the python environment with `img_sanity` installed, run
```
python -m img_sanity.app --help
```
to see the command line arguments needed to run the app on any data set.
To run the included example from the `img_sanity` repo, use
```
python -m img_sanity.app example/figure_data.csv --img_path=example/figures
```
