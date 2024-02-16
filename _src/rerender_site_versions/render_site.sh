#!/bin/bash -e

version=$1
folder="_src/rerender_site_versions/$2"

echo "version $version"
echo "folder $folder"

# get the website source
git clone --depth 1 --branch $version https://github.com/viash-io/website.git $folder

# inject version dropdown
docker run --rm -v "${PWD}":/workdir mikefarah/yq -i '.website.navbar.right = load("_src/rerender_site_versions/right.yml") + .website.navbar.right' $folder/_quarto.yml
cp --update=all js.html $folder

# copy file for website 0.8.1, and presumably also previous versions
if [ "$version" \< "0.8.2" ]; then
  cp --update=all _src/rerender_site_versions/_clone_template.qmd $folder/_includes
fi

# build
pushd $folder
export VIASH_VERSION=$version
Rscript -e 'renv::restore()'
source renv/python/virtualenvs/renv-python-3.10/bin/activate
quarto render
popd

# copy results
cp -r $folder/_site _site/versioned/$2
