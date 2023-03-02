import git, subprocess, json, csv, re, yaml
from pathlib import Path

repo = git.Repo(".", search_parent_directories=True) # Get root dir of repo
repo_root = repo.working_tree_dir

json_export = "cli_schema_export.json"
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

cli_dir = Path(repo_root, "reference", "cli")
json_file = Path(repo_root, "reference", "cli_schema_export.json")
template_file = Path(repo_root, "_src" ,"automation", "template_cli_page.j2.qmd")

reference_dir = repo_root + "/reference/"

config_file = Path(repo_root, '_src', 'automation', 'config_pages_settings.yaml')

def generate_json():
	""" Calls viash in order to generate a cli export. """

	# Run bin/viash export cli_schema
	json = subprocess.check_output(["viash", "export", "cli_schema"]).decode('utf-8')
	with open(json_file, 'w') as outfile:
		outfile.write(json)

	print(f"Generated {json_file}")

def read_config_page_settings():
	""" Load the folder structure and keyword replacements file. """

	config_file = Path(repo_root, '_src', 'automation', 'config_pages_settings.yaml')
	with open(config_file, 'r') as infile:
			yaml_data = yaml.safe_load(infile)
	return yaml_data

def generate_pages():
	""" Load the generated JSON file and creates pages for every command entry. """

	with open(json_file, 'r') as infile:
		viash_json = json.load(infile)

	for entry in viash_json:
		create_page(entry["name"], entry)


def create_page(name, json_data):

	if "bannerCommand" in json_data: # Info is in top level command
		page_data = {'title': f'viash {name}', 'usesSubcommands': False, 'data': [json_data]}
	else:
		page_data = {'title': f'viash {name}', 'usesSubcommands': True, 'data': json_data['subcommands']}

	# TODO: description = replace_keywords(argument["descr"])

	render_jinja_page(cli_dir, name, page_data)

# TODO
# def qmd_code_paragraph(text) -> str:
# 	""" Returns text with newlines and code styling added. """
# 	qmd = ""
# 	splitted = text.split("\n")
# 	for part in splitted:
# 		qmd += "`" + part + "`\n\n"
# 	return qmd

def render_jinja_page(folder: str, filename: str, data: dict):
	""" Write data to yaml file and run jinja. """
	
	full_path = Path(folder, filename)
	base_dir = full_path.parent
	yaml_file = Path(base_dir, "_" + full_path.name).with_suffix('.yaml')
	qmd_file = full_path.with_suffix('.qmd')

	base_dir.mkdir(parents=True, exist_ok=True)	
	
	with open(yaml_file, 'w') as outfile:
		yaml.safe_dump(data, outfile, default_flow_style=False)

	qmd = subprocess.check_output(["j2", template_file, yaml_file]).decode('utf-8')
	with open(qmd_file, 'w') as outfile:
		outfile.write(qmd)

def replace_keywords(text: str) -> str:
	""" Finds all keywords in the format @[keyword](text) and returns the replacements based on the keywords settings. """

	# Find all keyword links
	matches = re.finditer(keyword_regex, text, re.MULTILINE)

	for matchNum, match in enumerate(matches, start=1):
		whole_match = match.group(0)
		keyword, keyword_text = match.groups()

		try:
			link = config_pages_settings['keywords'][keyword]
		except KeyError:
			link = "no-link"
			print(f"Could not find {keyword} in the cli pages settings keywords")

		# Replace match with hyperlink
		text = text.replace(whole_match, f"[{keyword_text}]({link})")

	return text

if __name__ == "__main__":
	generate_json()
	config_pages_settings = read_config_page_settings()
	generate_pages()
