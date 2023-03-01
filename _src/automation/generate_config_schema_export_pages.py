import git, subprocess, json, csv, re, yaml, jinja2
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
	def __repr__ (self):
		arg_str = ', '.join([ x + '=' + (str(y) if len(str(y)) < 20 else str(y)[:17]+'...') for x, y in self.__dict__.items() if y ])
		return 'JsonEntryData(' + arg_str + ')'

functionality_entry_list = []
platforms_entry_list = []
requirements_entry_list = []
arguments_entry_list = []

repo = git.Repo(".", search_parent_directories=True) # Get root dir of repo
repo_root = repo.working_tree_dir

json_export = "config_schema_export.json"
keyword_replace_csv = repo_root + "/_src/automation/keyword_links.csv"
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

reference_dir = repo_root + "/reference/"
config_dir = reference_dir + "/config"

def generate_json():
	""" Calls viash in order to generate a config export. """
	
	# Run bin/viash export config_schema
	json = subprocess.run(["viash", "export", "config_schema"], stdout=subprocess.PIPE).stdout.decode('utf-8')
	f = open(reference_dir + json_export, "w")
	f.write(json)
	f.close()

	print(f"Generated {reference_dir}/{json_export}")


def read_json_entries():
	""" Load the generated JSON file and pass the entries to be read by the get_json_entries function. """

	reference_dir = repo_root + "/reference/"
	json_file = open(reference_dir + json_export, "r")
	viash_json = json.load(json_file)
	json_file.close()

	for topic in viash_json:
		if isinstance(viash_json[topic], dict):
			for subtopic in viash_json[topic]:
				get_json_entries(page_title = subtopic, topic = topic, json_entry = viash_json[topic][subtopic])
		else:
			get_json_entries(page_title= topic, topic = topic, json_entry = viash_json[topic])		


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
	# print('\n'.join([ str(r) for r in functionality_entry_list]))
	# print('\n'.join([ str(r) for r in requirements_entry_list]))
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

	entry_list = sorted(entry_list, key=lambda x: x.title, reverse=False)

	page_data = {}
	page_data['pageTitle'] = page_title
	page_data['title_is_name'] = title_is_name
	page_data['data'] = []

	for data in entry_list:
		d = {}
		d['title'] = data.title
		d['topic'] = data.topic
		d['name'] = data.name
		d['type'] = data.type
		d['description'] = replace_keywords(data.description)
		d['examples'] = data.examples
		d['removed'] = data.removed
		d['deprecated'] = data.deprecated
		# d['since'] = data.since
		page_data['data'].append(d)
		
	render_jinja_page("combined_page.j2.qmd", config_dir, save_filename, page_data)

def generate_grouped_pages(entry_list, save_dir):
	"""
	Parses a list of JsonEntryData, groups them by title and creates a page for each title.
JsonEntryData
	Arguments:
		 entry_list: List of JsonEntryData to parse
		 save_dir: Subdirectory of config to place files. Will be created if it doesn't exist.
	"""

	# Group entries per title
	uniqueTitles = set(map(lambda x:x.title, entry_list))
	groupedList = [[y for y in entry_list if y.title==x] for x in uniqueTitles]

	for group in groupedList:
		page_data = {}
		page_data['pageTitle'] = group[0].title
		# page_data['title_is_name'] = title_is_name
		page_data['data'] = []
		
		for data in group:
			d = {}
			# d['title'] = data.title
			# d['topic'] = data.topic
			d['name'] = data.name
			d['type'] = data.type
			if data.description:
				d['description'] = replace_keywords(data.description)
			else:
				print(f"Warning: description could not be found for \"{group[0].type}.{data.name}\"")
			d['examples'] = data.examples
			d['removed'] = data.removed
			d['deprecated'] = data.deprecated
			# d['since'] = data.since
			page_data['data'].append(d)
		
		filename = group[0].title.replace(" ", "")
		render_jinja_page("grouped_page.j2.qmd", save_dir, filename, page_data)
	
def clean_title(title) -> str:
	""" Returns title with added spaces and capitalization for better readability. """
	title = title.replace("Platform", " Platform")
	title = title.replace("Requirements", " Requirements")
	title = title.replace("Legacy", " Legacy")
	title = title.replace("Vdsl3", " Vdsl3")
	title = title.replace("Vdsl3", "VDSL3")
	return title.title()

def render_jinja_page(template: str, folder: str, filename: str, data: dict):
	""" Write data to yaml file and run jinja. """
	Path(folder).mkdir(parents=True, exist_ok=True)	

	path_file = Path(folder, filename)
	with open(path_file.with_suffix(".yaml"), 'w') as outfile:
			yaml.safe_dump(data, outfile, default_flow_style=False)

	path_template = Path(repo_root, "_src" ,"automation", template)
	
	qmd = subprocess.run(["j2", path_template, path_file.with_suffix(".yaml")], stdout=subprocess.PIPE).stdout.decode('utf-8')
	with open(path_file.with_suffix(".qmd"), 'w') as outfile:
		outfile.write(qmd)

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

if __name__ == "__main__":
	generate_json()
	read_json_entries()
	generate_pages()
