import git, subprocess, json, csv, re, yaml, jinja2
from pathlib import Path

entry_lists = {}

repo = git.Repo(".", search_parent_directories=True) # Get root dir of repo
repo_root = repo.working_tree_dir

json_export = "config_schema_export.json"
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

reference_dir = repo_root + "/reference/"
config_dir = reference_dir + "/config"

def generate_json():
	""" Calls viash in order to generate a config export. """
	
	# Run bin/viash export config_schema
	json = subprocess.run(["viash", "export", "config_schema"], stdout=subprocess.PIPE).stdout.decode('utf-8')
	json_file = Path(repo_root, "reference", json_export)
	with open(json_file, 'w') as outfile:
		outfile.write(json)

	print(f"Generated {reference_dir}/{json_export}")

def read_config_page_settings():
	global config_pages_settings
	config_file = Path(repo_root, '_src', 'automation', 'config_pages_settings.yaml')
	with open(config_file, 'r') as infile:
			config_pages_settings = yaml.safe_load(infile)

def read_json_entries():
	""" Load the generated JSON file and pass the entries to be read by the get_json_entries function. """

	json_file = Path(repo_root, "reference", json_export)
	with open(json_file, 'r') as infile:
		viash_json = json.load(infile)

	for topic in viash_json:
		if isinstance(viash_json[topic], dict):
			for subtopic in viash_json[topic]:
				get_json_entries(page_title = subtopic, topic = topic, json_entry = viash_json[topic][subtopic])
		else:
			get_json_entries(page_title= topic, topic = topic, json_entry = viash_json[topic])		


def get_json_entries(page_title, json_entry, topic):
	""" Reads the generated JSON file and extract all information into instances of the JsonEntryData class. """

	if topic == 'arguments': # Keep title of argument pages as-is
		title = page_title
	else:
		title = clean_title(page_title)

	# Sort json entries alphabetically and store in a dictionary
	sorted_dict = sorted(json_entry, key=lambda x: x["name"], reverse=False)

	page_data = {}
	page_data['topic'] = topic
	page_data['title'] = title
	page_data['data'] = []

	for newData in sorted_dict:
		if 'description' in newData:
			newData['description'] = replace_keywords(newData["description"])
		page_data['data'].append(newData)

	filename = topic
	if topic != page_title:
		filename = f"{topic}/{page_title}"

	if filename in config_pages_settings['structure']:
		filename = config_pages_settings['structure'][filename]
	else:
		print(f"Could not find {filename} in the config pages settings structure")
		
	if topic == 'functionality' or topic == 'requirements':
		render_jinja_page("combined_page.j2.qmd", config_dir, filename, page_data)
	else:
		render_jinja_page("grouped_page.j2.qmd", config_dir, filename, page_data)
	
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

	yaml_file = Path(folder, filename).with_suffix('.yaml')
	qmd_file = Path(folder, filename).with_suffix('.qmd')
	template_file = Path(repo_root, "_src" ,"automation", template)
	
	with open(yaml_file, 'w') as outfile:
			yaml.safe_dump(data, outfile, default_flow_style=False)

	qmd = subprocess.run(["j2", template_file, yaml_file], stdout=subprocess.PIPE).stdout.decode('utf-8')
	with open(qmd_file, 'w') as outfile:
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

		if keyword in config_pages_settings['keywords']:
			link = config_pages_settings['keywords'][keyword]

		# Replace match with hyperlink
		text = text.replace(whole_match, f"[{keyword_text}]({link})")

	return text

if __name__ == "__main__":
	generate_json()
	read_config_page_settings()
	read_json_entries()
