import git, subprocess, json, re, yaml
from pathlib import Path

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
	""" Load the folder structure and keyword replacements file. """

	global config_pages_settings
	config_file = Path(repo_root, '_src', 'automation', 'config_pages_settings.yaml')
	with open(config_file, 'r') as infile:
			config_pages_settings = yaml.safe_load(infile)

def read_json_entries():
	""" Load the generated JSON file, split into logical page chunks and generate pages. """

	with open(json_file, 'r') as infile:
		viash_json = json.load(infile)

	for topic in viash_json:
		if isinstance(viash_json[topic], dict):
			for subtopic in viash_json[topic]:
				generate_page(topic, subtopic, viash_json[topic][subtopic])
		else:
			generate_page(".", topic, viash_json[topic])

def generate_page(topic: str, subtopic: str, json_data: dict):
	""" Receives JSON data, does some minor data manipulation and writes to yaml & qmd. """

	if topic == 'arguments': # Keep title of argument pages as-is
		title = subtopic
	else:
		title = re.sub(r"(\w)([A-Z])", r"\1 \2", subtopic).title() # split words and capitalize

	# Sort data entries alphabetically on 'name'
	sorted_dict = sorted(json_data, key=lambda x: x["name"], reverse=False)

	# Fix description markdown keywords to links
	for d in sorted_dict:
		if 'description' in d:
			d['description'] = replace_keywords(d["description"])

	page_data = {}
	page_data['topic'] = topic
	page_data['title'] = title
	page_data['data'] = sorted_dict

	filename = f"{topic}/{subtopic}"

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
	""" Finds all keywords in the format @[keyword](text) and returns the replacements based on the keywords settings. """

	# Find all keyword links
	matches = re.finditer(keyword_regex, text, re.MULTILINE)

	for matchNum, match in enumerate(matches, start=1):
		whole_match = match.group(0)
		keyword, keyword_text = match.groups()

		if keyword in config_pages_settings['keywords']:
			link = config_pages_settings['keywords'][keyword]
		else:
			link = "no-link"
			print(f"Could not find {keyword} in the config pages settings keywords")

		# Replace match with hyperlink
		text = text.replace(whole_match, f"[{keyword_text}]({link})")

	return text

if __name__ == "__main__":
	generate_json()
	read_config_page_settings()
	read_json_entries()
