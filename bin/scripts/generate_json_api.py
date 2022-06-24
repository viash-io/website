import git, subprocess

# Get root dir of repo
repo = git.Repo('.', search_parent_directories=True)
repo_root = repo.working_tree_dir
# Get bin directory path
bin = repo_root + "/bin/"
reference_dir = repo_root + "/documentation/reference"

json = subprocess.run([bin + "viash", "--cli_export"], stdout=subprocess.PIPE).stdout.decode('utf-8')
f = open(repo_root + "/documentation/reference/" + "viash_ref.json", "w")
f.write(json)
f.close()

print("Generated cli_export json")