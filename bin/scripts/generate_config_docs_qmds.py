import json
import git, subprocess, json

# Get root dir of repo
repo = git.Repo(".", search_parent_directories=True)
repo_root = repo.working_tree_dir
json_export = "schema_export.json"
reference_dir = ""


def generate_json():
    bin = repo_root + "/bin/"
    global reference_dir
    reference_dir = repo_root + "/documentation/reference/"

    # TODO: Remove comments below once viash has --schema_export

    # json = subprocess.run([bin + "viash", "--schema_export"], stdout=subprocess.PIPE).stdout.decode('utf-8')
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
        if not key.endswith("Requirements"):
            create_page(viash_json, key, viash_json[key])


def create_page(full_json, page_name, json_entry):
    qmd = ""

    title = page_name.replace("Platform", " Platform")
    title = title.replace("Legacy", " Legacy")
    # qmd += f"---\ntitle: \"{title.title()}\"\n---\n\n"
    qmd += header(title.title())

    sorted_dict = sorted(json_entry, key=lambda x: x["name"], reverse=False)

    for i in range(len(sorted_dict)):
        if sorted_dict[i]["name"] == "__this__":
            qmd += sorted_dict[i]["description"].replace('"', "") + "\n\n"
            continue

        name = sorted_dict[i]["name"]
        qmd += "## " + name + "\n\n"

        if "removed" in  sorted_dict[i]:
            removed = sorted_dict[i]["removed"]
        else:
            removed = None

        if "deprecated" in  sorted_dict[i]:
            deprecated = sorted_dict[i]["deprecated"]
        else:
            deprecated = None

        if "type" in  sorted_dict[i]:
            type = sorted_dict[i]["type"]
        else:
            type = None

        if "description" in  sorted_dict[i]:
            description = sorted_dict[i]["description"]
        else:
            description = None

        if "example" in sorted_dict[i] and len(sorted_dict[i]["example"]) > 0:
            example = sorted_dict[i]["example"]
        else:
            example = None            

        if "since" in sorted_dict[i]:
            since = sorted_dict[i]["since"]
        else:
            since = None   

        if removed is not None:
            qmd += callout(
                "warning",
                "Removed since "
                + removed["since"]
                + ". "
                + removed["message"],
            )
        if deprecated is not None:
            qmd += callout(
                "warning",
                "Deprecated since "
                + deprecated["since"]
                + ". "
                + deprecated["message"],
            )
        if type is not None:
            qmd += parse_type(type)
        if description is not None:
            qmd += description + "\n\n"
        if example is not None:
            qmd += "### Example(s)" + "\n\n"
            for ex in example:
                qmd += (
                    "```"
                    + ex["format"]
                    + "\n"
                    + ex["example"].replace("\\n", "\n")
                    + "\n```\n\n"
                )
        # if since is not None:
        #     qmd += pill("Introduced: " + since)

    qmd += "\n\n"

    qmd_file = open(reference_dir + f"config/{page_name}.qmd", "w")
    qmd_file.write(qmd)
    qmd_file.close()


def header(title):
    qmd = ""
    qmd += f"---\ntitle: {title}\n"
    qmd += "search: true\n"
    qmd += "execute:\n"
    qmd += "  echo: false\n"
    qmd += "  output: asis\n"
    qmd += "---\n\n"
    return qmd


def pill(content):
    return "::: {.smallpill}\n" + content + "\n:::\n"


def callout(type, content):
    return "::: {" + f".callout-{type}" + "}\n" + content + "\n:::\n"

def parse_type(type_string):
    qmd ="**Type**: "

    if type_string.startswith("Option of"):
        type = type_string.replace("Option of","").strip()
        qmd += f"`{type}`"
    elif type_string.startswith("OneOrMore of"):
        type = type_string.replace("OneOrMore of","").strip()
        qmd += f"`{type}` / `List of {type}`"
    else:
        qmd += f"`{type_string}`"
    
    qmd += "\n\n"
    return qmd


if __name__ == "__main__":
    generate_json()
    create_qmd()
