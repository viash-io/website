## Viewing

You can look at the latest version of the  work-in-progress website here: https://viash-io.github.io/new_website/
Alternatively, you can pull the repo and execute this command for a local preview:

```
quarto preview
```

You'll probably need some R and Python prerequisite for the command above to work.

## Updating

The main .qmd files live in the **documentation** folder.
To create a new version of the website, make your changes and push them to the `main` branch. This will start up a Github action that will build the website to the `gh-pages` branch.
After about 15 minutes the changes should be visible on https://viash-io.github.io/new_website/.
