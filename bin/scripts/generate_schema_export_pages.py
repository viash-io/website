from ast import If
import git, subprocess, json, csv, re
from pathlib import Path

TOPIC_FUNCTIONALITY = "functionality"
TOPIC_PLATFORMS = "platforms"
TOPIC_REQUIREMENTS = "requirements"
TOPIC_ARGUMENTS = "arguments"

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
			get_json_entries(page_name= topic, topic = topic, json_entry = viash_json[topic])
		else:
			for subtopic in viash_json[topic]:
				get_json_entries(page_name = subtopic, topic = topic, json_entry = viash_json[topic][subtopic])


def get_json_entries(page_name, json_entry, topic):
	""" Reads the generated JSON file and extract all information into instances of the JsonEntryData class. """

	if topic == TOPIC_ARGUMENTS: # Keep title of argument pages as-is
		title = page_name
	else:
		title = clean_title(page_name)

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
	generate_simple_combined_page(entry_list= requirements_entry_list, page_name= "Setup Requirements", save_dir= config_dir, save_filename= "requirements")
	generate_related_pages(entry_list= platforms_entry_list, save_dir= config_dir)

def generate_simple_combined_page(entry_list, page_name, save_dir, save_filename):
	qmd = qmd_header(title=page_name)
	entry_list = sorted(entry_list, key=lambda x: x.title, reverse=False)

	for data in entry_list:
		data : JsonEntryData = data
		qmd += qmd_h2(data.title)
		qmd += qmd_paragraph(replace_keywords(data.description))
		qmd += qmd_parse_examples(data.examples)

	write_qmd_file(directory=save_dir, file_name=save_filename, content=qmd)
	

def generate_related_pages(entry_list, save_dir):

	for data in entry_list:
		data : JsonEntryData = data
		

	for data in entry_list:
		data : JsonEntryData = data
		qmd = ""
		qmd += qmd_h2(data.title)
		qmd += qmd_paragraph(replace_keywords(data.description))
		qmd += qmd_parse_examples(data.examples)
		print(qmd)
	
	

def clean_title(title) -> str:
	title = title.replace("Platform", " Platform")
	title = title.replace("Requirements", " Requirements")
	title = title.replace("Legacy", " Legacy")
	title = title.replace("Vdsl3", " Vdsl3")
	title = title.replace("Vdsl3", "VDSL3")
	return title.title()

def qmd_paragraph(text):
	return text + "\n\n"

def qmd_h2(text):
	return "## " + text + "\n\n"

def qmd_h3(text):
	return "### " + text + "\n\n"

def qmd_header(title):
	""" Returns the page metadata markdown that belongs at the top of a qmd file, with the title filled in. """

	qmd = ""
	qmd += f"---\ntitle: {title}\n"
	qmd += "search: true\n"
	qmd += "execute:\n"
	qmd += "  echo: false\n"
	qmd += "  output: asis\n"
	qmd += "---\n\n"
	return qmd

def qmd_callout(type, content):
	""" Returns a quarto callout block: https://quarto.org/docs/authoring/callouts.html """
	return "::: {" + f".callout-{type}" + "}\n" + content + "\n:::\n"

def replace_keywords(text: str) -> str:
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

def qmd_parse_examples(examples):
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
	Path(directory).mkdir(parents=True, exist_ok=True)
	qmd_file = open(f"{directory}/{file_name}.qmd", "w")
	qmd_file.write(content)
	qmd_file.close()

if __name__ == "__main__":
	generate_json()
	read_json_entries()
	generate_pages()
