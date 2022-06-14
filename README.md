## Viewing

You can look at the latest version of the  work-in-progress website here: https://viash-io.github.io/new_website/
Alternatively, you can pull the repo and execute this command for a local preview:

```
quarto preview
```

You'll probably need some R and Python prerequisite for the command above to work.

## Updating

The main .qmd files live in the **documentation** folder, while the **docs** folder contains the files to display the website in a web browser like HTML, JS and CSS.
To create a new version of the website, make your changes, then execute this from the root of the project:

```
quarto render
```

This will generate html files in the **docs** directory. Next, push the changes to the main branch.
After pushing the changes to main, the website will be rebuilt and published via gh pages. After a few minutes the changes should be visible on https://viash-io.github.io/new_website/.

