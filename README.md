This is the website repo for [viash.io](https://viash.io). It's built on top of [Quarto](https://quarto.org/).

## Local preview

Follow the steps below to start a local preview:

1. Install [Quarto](https://quarto.org/docs/get-started/)
2. Install [Python 3.10](https://www.python.org/) or higher
3. Install [R 4.1](https://www.r-project.org/) or higher
4. Pull the repo and use it as your working directory
5. Execute `Rscript -e 'renv::restore()'` to install most of the R and Python dependencies
6. Install some missing R dependencies: `Rscript -e 'install.packages(c("readr", "rmarkdown"))'`
7. Install the missing Python dependencies: `source renv/python/virtualenvs/renv-python-3.8/bin/activate && pip install pandas nbformat jupyter`
8. Run `quarto preview`
9. Navigate to [http://localhost:8000](http://localhost:8000) in a web browser