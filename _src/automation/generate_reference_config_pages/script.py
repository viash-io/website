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

	for topic, topic_json in viash_json.items():
		if isinstance(topic_json, dict):
			for subtopic, subtopic_json in topic_json.items():
				generate_page(topic, subtopic, subtopic_json)
		else:
			generate_page(".", topic, topic_json)

def generate_page(topic: str, subtopic: str, json_data: list):
	""" Receives JSON data, does some minor data manipulation and writes to yaml & qmd. """

	# if topic == 'arguments': # Keep title of argument pages as-is
	# 	title = subtopic
	# else:
	title = re.sub(r"(\w)([A-Z])", r"\1 \2", subtopic).title() # split words and capitalize

	# Fix description markdown keywords to links
	for d in json_data:
		if d['name'] == '__merge__':
			d['name'] = '`__merge__' # Bump __merge__ behind __this__ when sorted
		if 'description' in d:
			d['description'] = replace_keywords(d["description"])

	page_data = {"topic": topic, "title": title, "data": json_data}

	filename = f"{topic}/{subtopic}"

	try:
		page_data['order'] = config_pages_settings['order'][filename]
	except:
		pass

	try:
		filename = config_pages_settings['structure'][filename]
	except KeyError:
		print(f"Could not find {filename} in the config pages settings structure")

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

if __name__ == "__main__":
	read_json_entries()
