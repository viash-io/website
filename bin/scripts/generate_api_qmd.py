import json
import git, subprocess, json

# Get root dir of repo
repo = git.Repo('.', search_parent_directories=True)
repo_root = repo.working_tree_dir


def generate_json():
    bin = repo_root + "/bin/"
    subprocess.run(["python", bin + "scripts/generate_json_api.py"])
    

def create_qmd():
    reference_dir = repo_root + "/documentation/reference/"
    json_file = open(reference_dir + "viash_ref.json", "r")
    viash_json = json.load(json_file)
    json_file.close()


    qmd = ""
    # qmd = ":::{.column-page}\n\n"
    qmd += "---\ntitle: \"Viash (Python)\"\n---\n\n"

    for command in viash_json:
        if ('banner' in command): # Info is in top level command
            qmd += add_command(command)
        else: # Info is in subcommands
            for subcommand in command['subcommands']:
                qmd += add_command(subcommand)

    # qmd += ":::\n"

    qmd_file = open(reference_dir + "viash/viash_python.qmd", "w")
    qmd_file.write(qmd)
    qmd_file.close()

def add_command(command):
    md = ""

    split_banner = command['banner'].split('\n')
    for i in range(len(split_banner)):
        line = split_banner[i].strip()

        if (i == 0):
            md += f"## {line}\n\n"
            continue

        if (line == "Arguments:"):
                continue

        if (line.endswith(':')):
                md += "**" + line + "**  \n\n"

        elif (line.startswith('viash')):
                md += "`" + line + "`  \n\n"
        else:
            md += line + "  \n\n"

    md += create_opts_table(command['opts'])

    return md

def create_opts_table(opts):
    md =""
    md += "| Argument | Description | Type |\n"
    md += "|-|:----|-:\n"

    for opt in opts:
        argument = f"`--{opt['name']}`"
        if ('short' in opt):
            argument += f", `-{opt['short']}`"

        description = opt['descr'].replace("$","\$") # Prevents dollar sign being detected as LaTeX start
        md += f"| {argument} | {description} | {opt['type']} |\n"

    
    md += "\n\n"
    return md


if __name__ == "__main__":
    generate_json()
    create_qmd()