import re
from pathlib import Path
import jinja2

## VIASH START
par = {
    'input': '../viash/CHANGELOG.md',
    'output': 'blog/posts'
}
meta = {
    "resources_dir": "_src/automation/generate_version_blog_pages"
}
## VIASH END

output = Path(par["output"])
template_file = Path(meta['resources_dir'], "template_blog_page.j2.qmd")

with open(template_file) as f:
	template = jinja2.Template(f.read())

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

    qmd_file = output / f'viash-{version}/index.qmd'
    render_jinja_page(qmd_file, data)

def render_jinja_page(path: Path, data: dict):
	"""Run jinja on data and write results to file."""
	path.parent.mkdir(parents=True, exist_ok=True)	
	content = template.render(**data)
	path.write_text(content)

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
