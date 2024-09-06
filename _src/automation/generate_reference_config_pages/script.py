import json, re, yaml
from pathlib import Path
import jinja2

## VIASH START
par = {
  'input': 'reference/config_schema_export.json',
  'output': 'reference/cli'
}
meta = {
	"resources_dir": "_src/automation/generate_reference_config_pages"
}
## VIASH END

output = Path(par["output"])
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

template_file = Path(meta['resources_dir'], "template_config_page.j2.qmd")
config_file = Path(meta['resources_dir'], 'config_pages_settings.yaml')

with open(template_file) as f:
	template = jinja2.Template(f.read())

with open(config_file, 'r') as infile:
	config_pages_settings = yaml.safe_load(infile)

def read_json_entries():
	""" Load the generated JSON file, split into logical page chunks and generate pages. """

	with open(par['input'], 'r') as infile:
		viash_json = json.load(infile)

	for topic_json in viash_json:
		generate_page(topic_json)

def generate_page(json_data: list):
	""" Receives JSON data, does some minor data manipulation and writes to yaml & qmd. """

	this_parameter = {}
	# Fix description markdown keywords to links
	for d in json_data:
		if d['name'] == '__merge__':
			d['name'] = '`__merge__' # Bump __merge__ behind __this__ when sorted
		if d['name'] == '__this__':
			this_parameter = d
		if 'description' in d:
			d['description'] = inject_project_config_copying_notes(this_parameter['niceType'], d['name'], d['description'])
			d['description'] = replace_keywords(d["description"])

	topic = this_parameter['type']

	# split words and capitalize
	# do some extra substitutions to clean things up a bit
	title = re.sub(r"(\w)([A-Z])", r"\1 \2", topic).title() \
		.replace("Java Script", "JavaScript") \
		.replace("C Sharp", "C#") \
		.replace(" Argument", "")
	filename = topic

	if topic.endswith("RepositoryWithName"):
		json_data = patch_repository(json_data)
		title = title.removesuffix(" With Name")

	page_data = {"title": title, "data": json_data}

	try:
		page_data['order'] = config_pages_settings['order'][filename]
	except:
		pass

	try:
		filename = config_pages_settings['structure'][filename]
	except KeyError:
		print(f"Could not find {filename} in the config pages settings structure")
	
	if filename is not None:
		qmd_file = output / (filename + ".qmd")
		render_jinja_page(qmd_file, page_data)
	
def render_jinja_page(path: Path, data: dict):
	"""Run jinja on data and write results to file."""
	path.parent.mkdir(parents=True, exist_ok=True)	
	content = template.render(**data)
	path.write_text(content)

def replace_keywords(text: str) -> str:
	""" Finds all keywords in the format @[keyword](text) and returns the replacements based on the keywords settings. """

	# Find all keyword links
	matches = re.finditer(keyword_regex, text, re.MULTILINE)

	for matchNum, match in enumerate(matches, start=1):
		whole_match = match.group(0)
		keyword_text, keyword = match.groups()

		try:
			link = config_pages_settings['keywords'][keyword]
		except KeyError:
			link = "no-link"
			print(f"Could not find {keyword} in the config pages settings keywords")

		# Replace match with hyperlink
		text = text.replace(whole_match, f"[{keyword_text}]({link})")

	return text

def inject_project_config_copying_notes(class_name: str, parameter_name: str, text: str) -> str:
	""" Injects a note about copying the project config when using the parameter. """

	# print(f"Injecting project config copying notes for {class_name}.{parameter_name}")

	note = None

	match f"{class_name}.{parameter_name}":
		case "Functionality.version" | "Functionality.license" | "Functionality.organization":
			note = f"When the `{parameter_name}` field is left empty in a component's `.functionality` configuration, the value of `.version` in the @[package config](package_config) will be copied during build."
		case "Config.version" | "Config.license" | "Config.organization":
			note = f"When the `{parameter_name}` field is left empty in a component's configuration, the value of `.version` in the @[package config](package_config) will be copied during build."
		case "PackageConfig.version" | "PackageConfig.license" | "PackageConfig.organization":
			note = f"When the `{parameter_name}` field is left empty in a component's @[configuration](config), the value of `.version` in the package config will be copied during build."
		case "Functionality.repositories":
			note = "Any repositories defined under `.repositories` in the @[package config](package_config) will be prepended to the repositories defined in a component's @[configuration](functionality) of the `.functionality.repositories` field."
		case "Config.repositories":
			note = "Any repositories defined under `.repositories` in the @[package config](package_config) will be prepended to the repositories defined in a component's @[configuration](config) of the `.repositories` field."
		case "PackageConfig.repositories":
			note = "Any repositories defined under `.repositories` in the project config will be prepended to the list of repositories defined in a component's `.repositories` field."
		case "Links.repository" | "Links.docker_registry":
			note = f"When the `{parameter_name}` field is left empty in a component's `.links` @[configuration](config), the value of `.links.repository` in the @[package config](package_config) will be copied during build."

	if note is not None:
		return text + "\n\n:::{.callout-note}\n" + note + "\n:::\n\n"

	return text

def fudge_named_examples(this_info):
	# print(f"this_info before {this_info}")

	if 'example' not in this_info:
		return this_info

	examples = this_info['example']
	# print(f"examples {examples}")
	examples_orig = []
	for example in examples:
		ex = example.copy()
		ex['description'] = "Example without `name` field in case used in `.dependencies`"
		# strip name field from the example
		ex['example'] = re.sub(r"^name:.*\n", "", ex['example'])
		examples_orig.append(ex)

	examples_new = []
	for example in examples:
		ex = example.copy()
		ex['description'] = "Example with `name` field in case used in `.repositories`"
		examples_new.append(ex)

	this_info['example'] = examples_orig + examples_new
	return this_info

def patch_repository(info: list) -> list:
	descr = """:::{.callout-warning}
When defining repositories under `.repositories`, the repository definition needs a `name` field so it can be refered to from a dependency.

When defining a repository directly in a dependency under `.dependencies`, the `name` field must be omitted.
:::"""

	# print(f"json_data before {info}")
	# duplicate examples for named repositories
	info = list(map(lambda x: fudge_named_examples(x) if x['name'] == '__this__' else x, info))
	# add extra text to the name field
	for field in info:
		if field['name'] == 'name':
			field['description'] = descr + "\n\n" + field['description']
		if field['name'] == 'type' and field['description'] == "Defines the repository type. This determines how the repository will be fetched and handled.":
			field['description'] = "Defines the repository as a locally present and available repository."

	# print(f"json_data after {info}")
	return info

if __name__ == "__main__":
	read_json_entries()
