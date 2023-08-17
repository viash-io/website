import json, re, yaml
from pathlib import Path

## VIASH START
par = {
  'cli': 'reference/cli_schema_export.json',
  'config': 'reference/config_schema_export.json',
  'output': 'reference/cli'
}
meta = {
	"resources_dir": "_src/automation/generate_reference_cli_pages"
}
## VIASH END

output = Path(par["output"])
# keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

config_file = Path(meta['resources_dir'], 'config_pages_settings.yaml')

with open(config_file, 'r') as infile:
	config_pages_settings = yaml.safe_load(infile)

ref_dict = {}
def add_entry(topic, name, href):
	# print(f'topic: {topic}, name: {name}, href: {href} ')
	if topic in ref_dict:
		ref_dict[topic].append({ 'text': name, 'href': href + '.html' })
	else:
		ref_dict[topic] = [{ 'text': name, 'href': href + '.html' }]

def generate_reference_page():
	""" Load the generated JSON files and create reference entries. """

	# List the CLI commands
	with open(par['cli'], 'r') as infile:
		cli_json = json.load(infile)

	for entry in cli_json:
		if "bannerCommand" in entry:
			name = f'Viash {entry["name"]}'.title()
			filename = entry["name"]
			add_entry("Viash CLI Commands", name, f'./reference/cli/{filename}')
		else:
			for subcommand in entry['subcommands']:
				name = f'Viash {entry["name"]} {subcommand["name"]}'.title()
				filename = f'{entry["name"]}_{subcommand["name"]}'
				add_entry("Viash CLI Commands", name, f'/reference/cli/{filename}')

	# Add some static pages :(
	add_entry("Viash Config", "Viash Config Overview", "/reference/config/index")
	add_entry("Viash Config", "Functionality", "/reference/config/functionality/index")
	add_entry("Viash Config", "Viash Project Config", "/reference/project/index")

	# Add config pages highlighting field groups
	with open(par['config'], 'r') as infile:
		config_json = json.load(infile)

	# Regex filters. Platforms are not simply contained in a main folder, grab index files. For other matches, skip the index files.
	to_document = {
		'\./platforms/\w*/index': "Platforms",
		'\./functionality/arguments/(?!index$)\w*': "Argument Types",
		'\./functionality/resources/(?!index$)\w*': "Resource Types",
		'\./platforms/docker/setup/(?!index$)\w*': "Docker Setup Requirements"
	}

	for entry in config_json:
		this_parameter = {}
		# Get the __this__ parameter
		for d in entry:
			if d['name'] == '__this__':
				this_parameter = d
				break

		topic = this_parameter['type']
		title = re.sub(r"(\w)([A-Z])", r"\1 \2", topic).title() \
			.replace("Java Script", "JavaScript") \
			.replace("C Sharp", "C#") \
			.replace(" Argument", "")
		filename = config_pages_settings['structure'][topic]
		for key, value in to_document.items():
			if re.match(key, filename):
				add_entry(value, title, f'/reference/config{filename.strip(".")}')
				break

	# Minor final touch on the output and save to file
	output = []
	for key, value in ref_dict.items():
		output.append({ 'title': key, 'links': sorted(value, key=lambda k: k['text'] ) })

	with open(par['output'], 'w') as outfile:
		outfile.write(yaml.safe_dump(output))

if __name__ == "__main__":
	generate_reference_page()

