import git, subprocess, json, csv
from pathlib import Path

# Get root dir of repo
repo = git.Repo(".", search_parent_directories=True)
repo_root = repo.working_tree_dir
json_export = "cli_export.json"
reference_dir = ""
keyword_replace_csv = ""

def generate_json():
    bin = repo_root + "/bin/"
    global reference_dir
    global keyword_replace_csv
    reference_dir = repo_root + "/documentation/reference/"
    keyword_replace_csv = repo_root + "/bin-data/KeywordReplacements.csv"

    # TODO: Remove comments below once viash has --cli_export

    # json = subprocess.run([bin + "viash", "--cli_export"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    # f = open(reference_dir + json_export, "w")
    # f.write(json)
    # f.close()

    # print(f"Generated {reference_dir}/{json_export}")


def create_qmd():
    reference_dir = repo_root + "/documentation/reference/"
    json_file = open(reference_dir + json_export, "r")
    viash_json = json.load(json_file)
    json_file.close()

    for key in viash_json:
        create_page(key["name"], key)


def create_page(name, json_entry):
    qmd = ""
    qmd += header(f"viash {name}")

    if "bannerCommand" in json_entry:  # Info is in top level command
        qmd += add_command(json_entry)
    else:  # Info is in subcommands
        for subcommand in json_entry["subcommands"]:
            qmd += add_command(subcommand)

    write_qmd_file("viash", name, qmd)


def add_command(command):
    name = "viash " + command["name"]
    qmd = ""
    
    if name != command["bannerCommand"]:
        qmd += "## " + command["bannerCommand"] + "\n\n"

    # qmd += "Command: `" +  command["bannerCommand"] + "`\n\n"
    qmd += command["bannerDescription"] + "\n\n"
    qmd += "**Usage:**\n\n"
    qmd += "`" + command["bannerUsage"] + "`\n\n"

    # if "footer" in command:
    #     qmd += callout("note", command["footer"])


    qmd += create_opts_table(command["opts"])

    return qmd


def header(title):
    qmd = ""
    qmd += f"---\ntitle: {title}\n"
    qmd += "search: true\n"
    qmd += "execute:\n"
    qmd += "  echo: false\n"
    qmd += "  output: asis\n"
    qmd += "---\n\n"
    return qmd

def callout(type, content):
    return "::: {" + f".callout-{type}" + "}\n" + content + "\n:::\n"


def create_opts_table(opts):
    qmd = ""
    qmd += "| Argument | Description | Type |\n"
    qmd += "|-|:----|-:\n"

    sorted_opts = sorted(opts, key=lambda x: x["name"], reverse=False)


    for opt in sorted_opts:
        if opt['name'] == "config":
            argument = f"`{opt['name']}`"
        else:
            argument = f"`--{opt['name']}`"

        if "short" in opt:
            argument += f", `-{opt['short']}`"

        description = replace_terms(opt["descr"])

        if opt["required"]:
            description += " **This is a required argument.**"

        qmd += f"| {argument} | {description} | `{opt['type']}` |\n"

    # Always add --help
    qmd += f"| `--help`, `-h` | Show help message |  |\n"

    qmd += "\n\n"
    return qmd


def replace_terms(text: str) -> str:
    keywords_csv = open(keyword_replace_csv)
    csvreader = csv.reader(keywords_csv)
    for row in csvreader:
        text = text.replace(row[0], row[1])
    keywords_csv.close()
    return text

def write_qmd_file(dir_in_reference, file_name, content):
    Path(reference_dir + f"{dir_in_reference}/").mkdir(parents=True, exist_ok=True)
    qmd_file = open(reference_dir + f"{dir_in_reference}/{file_name}.qmd", "w")
    qmd_file.write(content)
    qmd_file.close()

if __name__ == "__main__":
    generate_json()
    create_qmd()
