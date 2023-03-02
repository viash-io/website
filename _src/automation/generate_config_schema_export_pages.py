import git, subprocess, json, csv, re, yaml, jinja2
from pathlib import Path

entry_lists = {}

repo = git.Repo(".", search_parent_directories=True) # Get root dir of repo
repo_root = repo.working_tree_dir

keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

config_dir = Path(repo_root, "reference", "config")
json_file = Path(repo_root, "reference", "config_schema_export.json")
template_file = Path(repo_root, "_src" ,"automation", "template_page.j2.qmd")

def generate_json():
	""" Calls viash in order to generate a config export. """
	
	# Run bin/viash export config_schema
	json = subprocess.run(["viash", "export", "config_schema"], stdout=subprocess.PIPE).stdout.decode('utf-8')
	with open(json_file, 'w') as outfile:
		outfile.write(json)

	print(f"Generated {json_file}")

def read_config_page_settings():
	global config_pages_settings
	config_file = Path(repo_root, '_src', 'automation', 'config_pages_settings.yaml')
	with open(config_file, 'r') as infile:
			config_pages_settings = yaml.safe_load(infile)

def read_json_entries():
	""" Load the generated JSON file and pass the entries to be read by the get_json_entries function. """

	with open(json_file, 'r') as infile:
		viash_json = json.load(infile)

	for topic in viash_json:
		if isinstance(viash_json[topic], dict):
			for subtopic in viash_json[topic]:
				get_json_entries(subtopic = subtopic, topic = topic, json_entry = viash_json[topic][subtopic])
		else:
			get_json_entries(subtopic= topic, topic = topic, json_entry = viash_json[topic])		

def get_json_entries(subtopic, json_entry, topic):
	""" Reads the generated JSON file and extract all information into instances of the JsonEntryData class. """

	if topic == 'arguments': # Keep title of argument pages as-is
		title = subtopic
	else:
		title = re.sub(r"(\w)([A-Z])", r"\1 \2", subtopic).title() # split words and capitalize

	# Sort json entries alphabetically and store in a dictionary
	sorted_dict = sorted(json_entry, key=lambda x: x["name"], reverse=False)

	page_data = {}
	page_data['topic'] = topic
	page_data['title'] = title
	page_data['data'] = []

	for newData in sorted_dict:
		# Fix our markdown identifiers to proper markdown links
		if 'description' in newData:
			newData['description'] = replace_keywords(newData["description"])
		page_data['data'].append(newData)

	if topic != subtopic:
		filename = f"{topic}/{subtopic}"
	else:
		filename = topic

	if filename in config_pages_settings['structure']:
		filename = config_pages_settings['structure'][filename]
	else:
		print(f"Could not find {filename} in the config pages settings structure")
		
	render_jinja_page(config_dir, filename, page_data)
	
def render_jinja_page(folder: str, filename: str, data: dict):
	""" Write data to yaml file and run jinja. """
	
	full_path = Path(folder, filename)
	base_dir = full_path.parent
	yaml_file = Path(base_dir, "_" + full_path.name).with_suffix('.yaml')
	qmd_file = full_path.with_suffix('.qmd')

	base_dir.mkdir(parents=True, exist_ok=True)	
	
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
