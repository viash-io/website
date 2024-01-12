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
			d['description'] = replace_keywords(d["description"])

	topic = this_parameter['type']

	# split words and capitalize
	# do some extra substitutions to clean things up a bit
	title = re.sub(r"(\w)([A-Z])", r"\1 \2", topic).title() \
		.replace("Java Script", "JavaScript") \
		.replace("C Sharp", "C#") \
		.replace(" Argument", "")
	filename = topic

	if topic.endswith("Repository"):
		json_data = patch_repository(json_data)

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

def fudge_named_examples(this_info):
	# print(f"this_info before {this_info}")

	if 'example' not in this_info:
		return this_info

	examples = this_info['example']
	print(f"examples {examples}")
	examples_orig = []
	for example in examples:
		ex = example.copy()
		ex['description'] = "Example without `name` field in case used in `.functionality.dependencies`"
		examples_orig.append(ex)

	examples_new = []
	for example in examples:
		ex = example.copy()
		ex['description'] = "Example with `name` field in case used in `.functionality.repositories`"
		if 'path: src/test/resources/testns' in ex['example']:
			ex['example'] = "name: viash-testns\n" + ex['example']
		elif 'openpipeline' in ex['example']:
			ex['example'] = "name: openpipeline\n" + ex['example']
		elif 'type: local' in ex['example']:
			ex['example'] = "name: my_local_code\n" + ex['example']
		examples_new.append(ex)

	this_info['example'] = examples_orig + examples_new
	return this_info

def patch_repository(info: list) -> list:
	descr = """:::{.callout-warning}
When defining repositories under `.functionality.repositories`, the repository definition needs a `name` field so it can be refered to from a dependency.

When defining a repository directly in a dependency under `.functionality.dependencies`, the `name` field must be omitted.
:::

The identifier used to refer to this repository from dependencies."""

	# print(f"json_data before {info}")
	# duplicate examples for named repositories
	info = list(map(lambda x: fudge_named_examples(x) if x['name'] == '__this__' else x, info))
	# add name field
	info.append({'name': 'name', 'type': 'String', 'niceType': 'String', 'description': descr})
	print(f"json_data after {info}")
	return info

if __name__ == "__main__":
	read_json_entries()
