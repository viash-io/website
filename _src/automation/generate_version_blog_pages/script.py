import subprocess, re, yaml
from pathlib import Path

## VIASH START
par = {
    'input': "_src/automation/generate_version_blog_pages/test_changelog.md",
    'output': "output/"
}
## VIASH END

template_file = Path(meta['resources_dir'], "template_blog_page.j2.qmd")

def bump_md_line(string: str) -> str:
    """ if header, bump header up one level """
    if re.match(r"^#+ .+$", string):
        string = "#" + string
    return string

def bump_markdown_headers(lines: list[str]) -> list[str]:
    """ map headers and bump up one level """
    out = map(bump_md_line, lines)
    return list(out)

def handle_section(lines: list[str]):
    """ Split version data into title, what's new, and full changelog parts and render with jinja """

    # take first line and process as header
    header = lines.pop(0)
    matches = re.search(r"^# Viash (\d+[\.\d+]+) \(([\dy]{4}-[\dM]{2}-[\dd]{2})\): (.*)$", header)
    version, date, subtitle = matches.group(1, 2, 3)

    # take lines while there are lines or we encounter a
    # markdown header, process as "what's new" section
    whats_new = []
    while lines and not re.match("^#+ [A-Z ]+$", lines[0]):
        whats_new.append(lines.pop(0))

    data = {
        "version": version,
        "date": date,
        "subtitle": subtitle,
        "whats_new": "".join(bump_markdown_headers(whats_new)),
        "changes": "".join(bump_markdown_headers(lines))
    }

    render_jinja_page(par['output'], f'viash-{version}/index.qmd', data)

def render_jinja_page(folder: str, filename: str, data: dict):
	""" Write data to yaml file and run jinja. """
	
	full_path = Path(folder, filename)
	base_dir = full_path.parent
	yaml_file = Path(base_dir, "_" + full_path.name).with_suffix('.yaml')
	qmd_file = full_path.with_suffix('.qmd')

	base_dir.mkdir(parents=True, exist_ok=True)	
	
	with open(yaml_file, 'w') as outfile:
		yaml.safe_dump(data, outfile, default_flow_style=False)

	subprocess.run(["j2", template_file, yaml_file, "-o", qmd_file])

def load_log(changelog_path: str):
    """ Load changelog and split into sections """
    with open(changelog_path, "r", encoding="utf8") as file:
        contents = file.readlines()

    # collect sections into a temporary buffer
    buff = []

    for line in contents:
        if re.match("^# Viash.*$", line):
            # new section, process previous one
            if buff:
                handle_section(buff)

            # start new buffer
            buff.clear()

        # store this line
        buff.append(line)

    # end by processing remaining buffer
    handle_section(buff)


if __name__ == "__main__":
    load_log(par['input'])
