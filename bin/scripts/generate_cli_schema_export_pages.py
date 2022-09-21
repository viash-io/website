import git, subprocess, json, csv, re
from pathlib import Path

repo = git.Repo(".", search_parent_directories=True) # Get root dir of repo
repo_root = repo.working_tree_dir

json_export = "cli_schema_export.json"
keyword_replace_csv = repo_root + "/bin-data/keyword_links.csv"
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

reference_dir = repo_root + "/documentation/reference/"

def generate_json():
	""" Calls viash in order to generate a cli export. """

	# Run bin/viash export cli_schema
	# bin = repo_root + "/bin/"
	# json = subprocess.run([bin + "viash", "export", "cli_schema"], stdout=subprocess.PIPE).stdout.decode('utf-8')
	# f = open(reference_dir + json_export, "w")
	# f.write(json)
	# f.close()

	print(f"Generated {reference_dir}/{json_export}")


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

	write_qmd_file("viash", name, qmd)

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
	qmd = ""
	qmd += f"---\ntitle: {title}\n"
	qmd += "search: true\n"
	qmd += "execute:\n"
	qmd += "  echo: false\n"
	qmd += "  output: asis\n"
	qmd += "---\n\n"
	return qmd

def qmd_code_paragraph(text) -> str:
	""" Returns text with newlines and code styling added. """
	return "`" + text + "`\n\n"

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


def replace_keywords(text: str) -> str:
	""" Finds all keywords in the format @[keyword](text) and returns the replacements based on the keywords CSV. """
	# Find all keyword links
	matches = re.finditer(keyword_regex, text, re.MULTILINE)

	for matchNum, match in enumerate(matches, start=1):
		whole_match = match.group(0)
		keyword = match.group(1)
		keyword_text = match.group(2)
		link = "no-link"

		# Find keyword in csv
		keywords_csv = open(keyword_replace_csv)
		csvreader = csv.reader(keywords_csv)
		for row in csvreader:
			if row[0] == keyword:
				link = row[1]
				break
		keywords_csv.close()

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
	generate_pages()
