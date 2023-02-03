import re
import os
import textwrap
from typing import Tuple

## VIASH START
par = {
    'input': "_src/automation/generate_version_blog_pages/test_changelog.md",
    'output': "output/",
    'verbose': False
}
## VIASH END

def combine_into_file(version: str, header: str, whats_new: list[str], changes: list[str]) -> None:
    """ Combine sections into a new file """

    if par['output'] is None or par['verbose']:
        print("\n---------")
        print(f"version: {version}")
        print(f"header:\n{header}")
        print(f"\n\nwhats_new:\n{whats_new}")
        print(f"\n\nchanges:\n{changes}")

    if par['output'] is not None:
        output_dir = par['output'] + "/viash-" + version
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_dir + "/index.qmd", "w", encoding="utf-8") as file:
            file.write(header)
            if whats_new:
                file.writelines(whats_new)
            if changes:
                file.writelines(changes)

def bump_md_line(string: str) -> str:
    """ if header, bump header up one level """
    if re.match(r"^#+ .+$", string):
        string = "#" + string
    return string

def bump_markdown_headers(lines: list[str]) -> list[str]:
    """ map headers and bump up one level """
    out = map(bump_md_line, lines)
    return list(out)

def handle_title(header: str) -> Tuple[str, str]:
    """ Split the title and create a header section """
    matches = re.search(r"^# Viash (\d+[\.\d+]+) \(([\dy]{4}-[\dM]{2}-[\dd]{2})\): (.*)$", header)

    version, date, subtitle = matches.group(1, 2, 3)

    # ---
    # title: "Viash 0.6.2"
    # subtitle: "Two bug fixes"
    # date: 2022/10/11
    # categories:
    #     - New Release
    # author: Viash Team
    # ---
    header = textwrap.dedent(f"""\
    title: "Viash {version}"
    subtitle: "{subtitle}"
    date: "{date}"
    categories: [ New Release ]
    author: Viash Team
    ---
    """)

    return version, header


def handle_whats_new(lines: list[str]) -> list[str]:
    """ Adapt what's new section to add header and bump headers to higher level """

    if not lines:
        return lines

    title = "\n## What's new?\n"
    out = bump_markdown_headers(lines)
    out.insert(0, title)
    return out


def handle_changes(lines: list[str]) -> list[str]:
    """ Adapt full changelog section to add header and bump headers to higher level """

    if not lines:
        return lines

    title = "## Full changelog\n\n"
    out = bump_markdown_headers(lines)
    out.insert(0, title)
    return out


def handle_section(lines: list[str]):
    """ Split version data into title, what's new, and full changelog parts and write to file """

    # take first line and process as header
    header = lines.pop(0)
    parsed_version, parsed_header = handle_title(header)

    # take lines while there are lines or we encounter a
    # markdown header, process as "what's new" section
    buff = []
    while lines and not re.match("^#+ [A-Z ]+$", lines[0]):
        buff.append(lines.pop(0))

    parsed_whats_new = handle_whats_new(buff)

    # treat remaining list as "changes" section
    parsed_changes = handle_changes(lines)

    # save output
    combine_into_file(parsed_version, parsed_header, parsed_whats_new, parsed_changes)


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
