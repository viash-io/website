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
config_pages_settings = ''
with open(config_file, 'r') as infile:
		config_pages_settings = yaml.safe_load(infile)

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
	json_file = open(reference_dir + json_export, "r")
	viash_json = json.load(json_file)
	json_file.close()

	for key in viash_json:
		create_page(key["name"], key)


def create_page(name, json_entry):
	qmd = ""
	qmd += qmd_header(f"viash {name}")

	if "bannerCommand" in json_entry:  # Info is in top level command
		qmd += qmd_add_command(command_json=json_entry, is_subcommand=False)
	else:  # Info is in subcommands
		for subcommand_json in json_entry["subcommands"]:
			qmd += qmd_add_command(command_json=subcommand_json, is_subcommand=True)

	write_qmd_file("cli", name, qmd)

def qmd_add_command(command_json, is_subcommand) -> str:
	""" Returns the information about the command in markdown form. """
	qmd = ""
	
	if is_subcommand: # This is a subcommand, so add a H2 with its name
		qmd += qmd_h2(command_json["bannerCommand"])

	qmd += command_json["bannerDescription"] + "\n\n"
	qmd += qmd_bold_paragraph("Usage:")
	qmd += qmd_code_paragraph(command_json["bannerUsage"])
	qmd += qmd_create_arguments_table(command_json["opts"])

	return qmd

def qmd_header(title) -> str:
	""" Returns the page metadata markdown that belongs at the top of a qmd file, with the title filled in. """
	qmd = "---\n"
	qmd += f"title: {title}\n"
	qmd += "search: true\n"
	qmd += "execute:\n"
	qmd += "  echo: false\n"
	qmd += "  output: asis\n"
	qmd += "---\n\n"
	return qmd

def qmd_code_paragraph(text) -> str:
	""" Returns text with newlines and code styling added. """
	qmd = ""
	splitted = text.split("\n")
	for part in splitted:
		qmd += "`" + part + "`\n\n"
	return qmd

def qmd_bold_paragraph(text) -> str:
	""" Returns text with newlines and bold styling added. """
	return "**" + text + "**\n\n"

def qmd_h2(text) -> str:
	""" Returns text with H2 markdown and newlines. """
	return "## " + text + "\n\n"

def qmd_create_arguments_table(arguments_list) -> str:
	""" Creates a table of arguments found in the given arguments_list """
	qmd = ""
	qmd += "| Argument | Description | Type |\n"
	qmd += "|-|:----|-:\n"

	sorted_arguments = sorted(arguments_list, key=lambda x: x["name"], reverse=False)

	for argument in sorted_arguments:
		if argument['name'] == "config":
			argument_name = f"`{argument['name']}`"
		else:
			argument_name = f"`--{argument['name']}`"

		if "short" in argument:
			argument_name += f", `-{argument['short']}`"

		description = replace_keywords(argument["descr"])
		description = description.replace(
			"$", "\$"
		)  # Prevents dollar sign being detected as LaTeX start

		if argument["required"]:
			description += " **This is a required argument.**"

		qmd += f"| {argument_name} | {description} | `{argument['type']}` |\n"

	# Always add --help
	qmd += f"| `--help`, `-h` | Show help message |  |\n"

	qmd += "\n\n"
	return qmd

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

def write_qmd_file(dir_in_reference, file_name, content):
	Path(reference_dir + f"{dir_in_reference}/").mkdir(parents=True, exist_ok=True)
	qmd_file = open(reference_dir + f"{dir_in_reference}/{file_name}.qmd", "w")
	qmd_file.write(content)
	qmd_file.close()

if __name__ == "__main__":
	generate_json()
	config_pages_settings = read_config_page_settings()
	generate_pages()
