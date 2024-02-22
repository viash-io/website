import json, re, yaml
from pathlib import Path
import glob

## VIASH START
par = {
  'output': 'reference/cli'
}
meta = {
	"resources_dir": "_src/automation/generate_reference_cli_pages"
}
## VIASH END

ref_dict = {}
def add_entry(topic, name, href):
	# print(f'topic: {topic}, name: {name}, href: {href} ')
	if topic in ref_dict:
		ref_dict[topic].append({ 'text': name, 'href': href + '.html' })
	else:
		ref_dict[topic] = [{ 'text': name, 'href': href + '.html' }]

def get_topic_from_qmd(qmd_file):
	""" Get the topic from the qmd file. """
	# TODO: Read the header from the qmd file and parse as YAML
	with open(qmd_file, 'r') as infile:
		for line in infile:
			if line.startswith('title:'):
				return line.split(':')[1].strip().strip('"')

def add_entries_from_glob(glob_pattern, topic, skip_index):
	""" Add entries from a glob pattern. """
	files = glob.glob(glob_pattern)
	for file in sorted(files):
		if skip_index and file.endswith('index.qmd'):
			continue
		add_entry(topic, get_topic_from_qmd(file), "/" + file.replace('.qmd', ''))

def generate_reference_page():
	""" Load the generated JSON files and create reference entries. """

	# List the CLI commands
	add_entries_from_glob('reference/cli/*.qmd', "Viash CLI Commands", True)

	# Add some static pages :(
	add_entry("Viash Config", "Config Overview", "/reference/config/index")
	add_entry("Viash Config", "Functionality", "/reference/config/functionality/index")
	add_entry("Viash Config", "Runners", "/reference/config/runners/index")
	add_entry("Viash Config", "Engines", "/reference/config/engines/index")
	add_entry("Viash Config", "Platforms", "/reference/config/platforms/index")
	add_entry("Miscellaneous", "Project Config", "/reference/project/index")
	add_entry("Miscellaneous", "Environment Variables", "/reference/config/environmentVariables")
	add_entry("Miscellaneous", "Config Mods", "/reference/config_mods/index")
	add_entry("Miscellaneous", "Viash Code Block", "/reference/viash_code_block/index")
	
	# Runners/Engines/Platforms are not simply contained in a main folder, grab index files. For other matches, skip the index files.
	add_entries_from_glob('reference/config/runners/*/index.qmd', "Runners", False)
	add_entries_from_glob('reference/config/engines/*/index.qmd', "Engines", False)
	add_entries_from_glob('reference/config/platforms/*/index.qmd', "Platforms", False)
	add_entries_from_glob('reference/config/engines/docker/setup/*.qmd', "Docker Setup Requirements", True)
	add_entries_from_glob('reference/config/functionality/arguments/*.qmd', "Argument Types", True)
	add_entries_from_glob('reference/config/functionality/resources/*.qmd', "Resource Types", True)
	
	# Minor final touch on the output and save to file
	output = []
	for key, value in ref_dict.items():
		output.append({ 'title': key, 'links': sorted(value, key=lambda k: k['text'] ) })

	with open(par['output'], 'w') as outfile:
		outfile.write(yaml.safe_dump(output))

if __name__ == "__main__":
	generate_reference_page()

