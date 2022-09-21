import git, subprocess, json, csv, re
from pathlib import Path

TOPIC_FUNCTIONALITY = "functionality"
TOPIC_PLATFORMS = "platforms"
TOPIC_REQUIREMENTS = "requirements"
TOPIC_ARGUMENTS = "arguments"

THIS_IDENTIFIER = "__this__"

class JsonEntryData:
	title = ""
	topic = ""
	name = ""
	type = ""
	description = ""
	examples = []
	removed = ""
	deprecated = ""
	since = ""

functionality_entry_list = []
platforms_entry_list = []
requirements_entry_list = []
arguments_entry_list = []

repo = git.Repo(".", search_parent_directories=True) # Get root dir of repo
repo_root = repo.working_tree_dir

json_export = "config_schema_export.json"
keyword_replace_csv = repo_root + "/bin-data/keyword_links.csv"
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

reference_dir = repo_root + "/documentation/reference/"
config_dir = reference_dir + "/config"

def generate_json():
	""" Calls viash in order to generate a config export. """
	
	# Run bin/viash export config_schema
	# bin = repo_root + "/bin/"
	# json = subprocess.run([bin + "viash", "export", "config_schema"], stdout=subprocess.PIPE).stdout.decode('utf-8')
	# f = open(reference_dir + json_export, "w")
	# f.write(json)
	# f.close()

	print(f"Generated {reference_dir}/{json_export}")


def read_json_entries():
	""" Load the generated JSON file and pass the entries to be read by the get_json_entries function. """

	reference_dir = repo_root + "/documentation/reference/"
	json_file = open(reference_dir + json_export, "r")
	viash_json = json.load(json_file)
	json_file.close()

	for topic in viash_json:
		if topic == "functionality":
			get_json_entries(page_title= topic, topic = topic, json_entry = viash_json[topic])
		else:
			for subtopic in viash_json[topic]:
				get_json_entries(page_title = subtopic, topic = topic, json_entry = viash_json[topic][subtopic])


def get_json_entries(page_title, json_entry, topic):
	""" Reads the generated JSON file and extract all information into instances of the JsonEntryData class. """

	if topic == TOPIC_ARGUMENTS: # Keep title of argument pages as-is
		title = page_title
	else:
		title = clean_title(page_title)

	# Sort json entries alphabetically and store in a dictionary
	sorted_dict = sorted(json_entry, key=lambda x: x["name"], reverse=False)

	for i in range(len(sorted_dict)):
		newData = JsonEntryData()
		newData.topic = topic
		newData.title = title
		newData.name = sorted_dict[i]["name"] if "name" in sorted_dict[i] else None
		newData.examples = sorted_dict[i]["example"] if "example" in sorted_dict[i] else None
		newData.removed = sorted_dict[i]["removed"] if "removed" in sorted_dict[i] else None
		newData.deprecated = sorted_dict[i]["deprecated"] if "deprecated" in sorted_dict[i] else None
		newData.since = sorted_dict[i]["since"] if "since" in sorted_dict[i] else None
		newData.type = sorted_dict[i]["type"] if "type" in sorted_dict[i] else None
		newData.description = sorted_dict[i]["description"] if "description" in sorted_dict[i] else None

		add_json_data_to_list(newData)
		

def add_json_data_to_list(data : JsonEntryData):
	""" Adds the JsonEntryData to an entry list based on its topic. """
	if data.topic == TOPIC_FUNCTIONALITY:
		functionality_entry_list.append(data)
	elif data.topic == TOPIC_ARGUMENTS:
		arguments_entry_list.append(data)	
	elif data.topic == TOPIC_PLATFORMS:
		platforms_entry_list.append(data)	
	elif data.topic == TOPIC_REQUIREMENTS:
		requirements_entry_list.append(data)

def generate_pages():
	"""Feed JsonEntryData lists to page generation functions."""

	generate_combined_page(entry_list= functionality_entry_list, page_title= "Functionality", save_filename= "functionality", title_is_name=False)
	generate_combined_page(entry_list= requirements_entry_list, page_title= "Setup Requirements", save_filename= "requirements", title_is_name=True)
	generate_grouped_pages(entry_list= platforms_entry_list, save_dir= config_dir + "/platforms")
	generate_grouped_pages(entry_list= arguments_entry_list, save_dir= config_dir + "/arguments")

def generate_combined_page(entry_list, page_title, save_filename, title_is_name):
	"""
	Parses a list of JsonEntryData and combines it into a single page.

	Arguments:
		 entry_list: List of JsonEntryData to parse
		 page_title: Title of the combined page
		 save_filename: Name of the file without any extensions
		 title_is_name: If True, the title property of every JsonEntryData will be used as if it was the name property
	"""

	qmd = qmd_header(title=page_title)
	entry_list = sorted(entry_list, key=lambda x: x.title, reverse=False)

	for data in entry_list:
		data : JsonEntryData = data

		if title_is_name: # The title property should be used as if it was the name of the property. This is the case with small separate pages.
			qmd += qmd_h2(data.title)
			qmd += qmd_paragraph(replace_keywords(data.description))
			qmd += qmd_parse_examples(data.examples)
		else:
			if data.name != THIS_IDENTIFIER:
				qmd += qmd_h2(data.name)
				qmd += qmd_parse_type(data.type)
				qmd += qmd_removed_deprecated(data.removed, data.deprecated)
				qmd += qmd_paragraph(replace_keywords(data.description))
				qmd += qmd_parse_examples(data.examples)
			else:
				qmd += qmd_paragraph(replace_keywords(data.description))
				qmd += qmd_parse_examples(data.examples)

	write_qmd_file(directory=config_dir, file_name=save_filename, content=qmd)
	

def generate_grouped_pages(entry_list, save_dir):
	"""
	Parses a list of JsonEntryData, groups them by title and creates a page for each title.

	Arguments:
		 entry_list: List of JsonEntryData to parse
		 save_dir: Subdirectory of config to place files. Will be created if it doesn't exist.
	"""

	# Group entries per title
	uniqueTitles = set(map(lambda x:x.title, entry_list))
	groupedList = [[y for y in entry_list if y.title==x] for x in uniqueTitles]

	for group in groupedList:
		# Take title from first entry in group and use that as the header for this page
		qmd = qmd_header(group[0].title)
		filename = group[0].title.replace(" ", "")

		for data in group:
			data : JsonEntryData = data
			if data.name != THIS_IDENTIFIER:
				qmd += qmd_h2(data.name)
				qmd += qmd_parse_type(data.type)
				qmd += qmd_removed_deprecated(data.removed, data.deprecated)
				qmd += qmd_paragraph(replace_keywords(data.description))
				qmd += qmd_parse_examples(data.examples)
			else:
				qmd += qmd_paragraph(replace_keywords(data.description))
				qmd += qmd_parse_examples(data.examples)

		write_qmd_file(directory=save_dir, file_name=filename, content=qmd)
	
def clean_title(title) -> str:
	""" Returns title with added spaces and capitalization for better readability. """
	title = title.replace("Platform", " Platform")
	title = title.replace("Requirements", " Requirements")
	title = title.replace("Legacy", " Legacy")
	title = title.replace("Vdsl3", " Vdsl3")
	title = title.replace("Vdsl3", "VDSL3")
	return title.title()

def qmd_paragraph(text) -> str:
	""" Returns text with newlines added. """
	return text + "\n\n"

def qmd_h2(text) -> str:
	""" Returns text with H2 markdown and newlines. """
	return "## " + text + "\n\n"

def qmd_h3(text) -> str:
	""" Returns text with H3 markdown and newlines. """
	return "### " + text + "\n\n"

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

def qmd_callout(type, content) -> str:
	""" Returns a quarto callout block: https://quarto.org/docs/authoring/callouts.html """
	return "::: {" + f".callout-{type}" + "}\n" + content + "\n:::\n"

def qmd_removed_deprecated(removed_dict, deprecated_dict) -> str:
	""" Returns markdown with added warning callouts based on the removed and deprecated properties of JsonEntryData  """
	qmd = ""

	if removed_dict is not None:
		qmd += qmd_callout(
				"warning",
				"Removed since "
				+ removed_dict["since"]
				+ ". "
				+ removed_dict["message"],
			)
	
	if deprecated_dict is not None:
		qmd += qmd_callout(
				"warning",
				"Deprecated since "
				+ deprecated_dict["since"]
				+ ". "
				+ deprecated_dict["message"],
			)

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

def qmd_parse_type(type_string) -> str:
	""" Returns a human readable markdown version of the type property.  """
	qmd ="**Type**: "

	if type_string.startswith("Option of"):
		type = type_string.replace("Option of","").strip()
		qmd += f"`{type}`"
	elif type_string.startswith("OneOrMore of"):
		type = type_string.replace("OneOrMore of","").strip()
		qmd += f"`{type}` / `List of {type}`"
	else:
		qmd += f"`{type_string}`"
	
	qmd += "\n\n"
	return qmd

def qmd_parse_examples(examples) -> str:
	""" Returns a human readable markdown version of a list of examples with code formatting.  """
	qmd = ""

	if examples is None or len(examples) == 0:
		return qmd

	qmd += qmd_h3("Example")
	for ex in examples:
		if "description" in ex:
			qmd += ex["description"] + "\n\n"

		qmd += (
			"```"
			+ ex["format"]
			+ "\n"
			+ ex["example"].replace("\\n", "\n")
			+ "\n```\n\n"
		)
	
	return qmd

def write_qmd_file(directory, file_name, content):
	""" Write a qmd file to disk in the specified directory, with the given filename and content. """
	Path(directory).mkdir(parents=True, exist_ok=True)
	qmd_file = open(f"{directory}/{file_name}.qmd", "w")
	qmd_file.write(content)
	qmd_file.close()

if __name__ == "__main__":
	generate_json()
	read_json_entries()
	generate_pages()
