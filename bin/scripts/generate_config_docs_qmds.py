import json
import git, subprocess, json

# Get root dir of repo
repo = git.Repo('.', search_parent_directories=True)
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
        if (not key.endswith("Requirements")):
            create_page(viash_json, key, viash_json[key])



def create_page(full_json, name, json_entry):
    qmd = ""

    title = name.replace("Platform"," Platform")
    title = title.replace("Legacy"," Legacy")
    qmd += f"---\ntitle: \"{title.title()}\"\n---\n\n"

    for i in range(len(json_entry)):
        if (json_entry[i]["name"] == "__this__"):
            qmd += json_entry[i]["description"].replace('"','') + "\n\n"
            continue
    
        qmd += "## " + json_entry[i]["name"] + "\n\n"
        if ('description' in json_entry[i]):
            qmd += json_entry[i]["description"] + "\n\n"
        if ('example' in json_entry[i] and len(json_entry[i]["example"]) > 0):
            qmd += "### Example(s)" + "\n\n"
            for example in json_entry[i]["example"]:
                qmd += "```" + example["format"] + "\n"  + example["example"].replace('\\n','\n') + "\n```\n\n"
        if ('since' in json_entry[i]):
            qmd += "Introduced in " + json_entry[i]["since"] + "\n\n"

        

    qmd_file = open(reference_dir + f"config/{name}.qmd", "w")
    qmd_file.write(qmd)
    qmd_file.close()


if __name__ == "__main__":
    generate_json()
    create_qmd()