import json, re, yaml
from pathlib import Path
import jinja2

## VIASH START
par = {
  'input': 'reference/cli_schema_export.json',
  'output': 'reference/cli'
}
meta = {
	"resources_dir": "_src/automation/generate_reference_cli_pages"
}
## VIASH END

output = Path(par["output"])
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

template_file = Path(meta['resources_dir'], "template_cli_page.j2.qmd")
config_file = Path(meta['resources_dir'], 'config_pages_settings.yaml')

with open(template_file) as f:
	template = jinja2.Template(f.read())

with open(config_file, 'r') as infile:
	config_pages_settings = yaml.safe_load(infile)

def generate_pages():
	""" Load the generated JSON file and creates pages for every command entry. """

	with open(par['input'], 'r') as infile:
		viash_json = json.load(infile)

	for entry in viash_json:
		# create_page(entry["name"], entry)
		if "bannerCommand" in entry:
			create_page(entry["name"], entry)
		else:
			for subcommand in entry['subcommands']:
				create_page(f"{entry['name']} {subcommand['name']}", subcommand)		

def create_page(name, json_data):
	""" Do minor transformations and let jinja do its thing """

	if "bannerCommand" in json_data: # Info is in top level command
		page_data = {'title': f'viash {name}'.title(), 'usesSubcommands': False, 'data': [json_data]}
	else:
		page_data = {'title': f'viash {name}'.title(), 'usesSubcommands': True, 'data': json_data['subcommands']}

	# replace keywords in 'descr' fields
	for d in page_data['data']:
		if 'opts' in d:
			for arg in d['opts']:
				if 'descr' in arg:
					arg['descr'] = replace_keywords(arg["descr"])

	qmd_file = output / f"{name.replace(' ', '_')}.qmd"
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
			print(f"Could not find {keyword} in the cli pages settings keywords")

		# Replace match with hyperlink
		text = text.replace(whole_match, f"[{keyword_text}]({link})")

	return text

if __name__ == "__main__":
	generate_pages()

