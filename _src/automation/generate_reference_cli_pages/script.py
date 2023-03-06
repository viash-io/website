
## VIASH START
# The following code has been auto-generated by Viash.
par = {
  'input': r'/path/to/file',
  'output': r'reference/cli'
}
## VIASH END
import subprocess, json, re, yaml
from pathlib import Path

keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

template_file = Path(meta['resources_dir'], "template_cli_page.j2.qmd")
config_file = Path(meta['resources_dir'], 'config_pages_settings.yaml')

with open(config_file, 'r') as infile:
	config_pages_settings = yaml.safe_load(infile)


def generate_pages():
	""" Load the generated JSON file and creates pages for every command entry. """

	with open(par['input'], 'r') as infile:
		viash_json = json.load(infile)

	for entry in viash_json:
		create_page(entry["name"], entry)

def create_page(name, json_data):
	""" Do minor transformations and let jinja do its thing """

	if "bannerCommand" in json_data: # Info is in top level command
		page_data = {'title': f'viash {name}', 'usesSubcommands': False, 'data': [json_data]}
	else:
		page_data = {'title': f'viash {name}', 'usesSubcommands': True, 'data': json_data['subcommands']}

	# replace keywords in 'descr' fields
	for d in page_data['data']:
		if 'opts' in d:
			for arg in d['opts']:
				if 'descr' in arg:
					arg['descr'] = replace_keywords(arg["descr"])

	render_jinja_page(par['output'], name, page_data)

def render_jinja_page(folder: str, filename: str, data: dict):
	""" Write data to yaml file and run jinja. """
	
	full_path = Path(folder, filename)
	base_dir = full_path.parent
	yaml_file = Path(base_dir, "_" + full_path.name).with_suffix('.yaml')
	qmd_file = full_path.with_suffix('.qmd')

	base_dir.mkdir(parents=True, exist_ok=True)	
	
	with open(yaml_file, 'w') as outfile:
		yaml.safe_dump(data, outfile, default_flow_style=False)

	qmd = subprocess.check_output(["j2", template_file, yaml_file]).decode('utf-8')
	with open(qmd_file, 'w') as outfile:
		outfile.write(qmd)

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

