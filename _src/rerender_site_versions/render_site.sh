#!/bin/bash -e

version=$1
folder=$2
target=$3

echo "version $version"
echo "folder $folder"
echo "target $target"

# get the website source
git clone --depth 1 --branch $version https://github.com/viash-io/website.git $folder

# inject version dropdown
docker run --rm -v "${PWD}":/workdir mikefarah/yq -i '.website.navbar.right = load("right.yml") + .website.navbar.right' $folder/_quarto.yml
cp --update=all js.html $folder

# copy file for website 0.8.1, and presumably also previous versions
if [ "$version" \< "0.8.2" ]; then
  cp --update=all _clone_template.qmd $folder/_includes
fi

# build
cd $folder
export VIASH_VERSION=$version
Rscript -e 'renv::restore()'
source renv/python/virtualenvs/renv-python-3.10/bin/activate
quarto render

# copy results
cp -r _site $target/_site/versioned/$folder
