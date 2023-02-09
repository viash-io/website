This is the website repo for [viash.io](https://viash.io). It's built on top of [Quarto](https://quarto.org/).

## Requirements

1. Install [Quarto](https://quarto.org/docs/get-started/)
2. Install [Python 3.10](https://www.python.org/) or higher
3. Install [R 4.2](https://www.r-project.org/) or higher

## First setup

```sh
# clone the repo
git@github.com:viash-io/website.git
cd website

# Install R and Python dependency packages
Rscript -e 'renv::restore()'
```

## Local preview

```sh
source renv/python/virtualenvs/renv-python-3.10/bin/activate
quarto preview
```

Navigate to [http://localhost:8000](http://localhost:8000) in a web browser
