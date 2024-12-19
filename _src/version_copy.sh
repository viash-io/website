mkdir _versioned/new
rsync -av --exclude 'versions.js' --exclude 'versions.json' --exclude 'versioned' _site/ _versioned/new/

echo "next rename the 'new' folder to the version number"
echo "then run 'tar -cJf new.tar.xz new'"