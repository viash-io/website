# viash.io

This is the website repo for [viash.io](https://viash.io).

## Requirements

[Quarto](https://quarto.org/docs/get-started/), R 4.2 and Python 3.10.

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

## How the renv was created

```r
install.packages("renv")
renv::init()
renv::use_python()
```

```sh
source renv/python/virtualenvs/renv-python-3.10/bin/activate
```

```r
install.packages(c("reticulate", "languageserver", "rmarkdown"))
reticulate::py_install(c("pandas", "GitPython", "jupyter", "nbformat"))
renv::snapshot()
```
