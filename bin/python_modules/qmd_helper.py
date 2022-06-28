# Imports
import git, os

# Get root dir of repo
repo = git.Repo('.', search_parent_directories=True)
repo_root = repo.working_tree_dir

# Run `quarto pandoc --list-highlight-languages` for full list of supported languages
def print_file_contents(path, language = "default", folded = False):
    filepath = repo_root + path
    basename = os.path.basename(filepath)
    f = open(filepath)
    file_contents = f.read()

    if folded:
        print("<details>")
        print(f"<summary>Contents of {basename}</summary>")

    print(f"```{language}  ")
    print(file_contents)
    print("```  ")

    if folded:
        print("</details>")

def create_download_button(path):
    basename = os.path.basename(path)
    download_path = path
    print(f"<a href=\"{download_path}\" id=\"btn-download\" class=\"btn btn-info btn-md\" role=\"button\" download>Download {basename}</a>  ")