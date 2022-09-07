import re, csv, git

repo = git.Repo(".", search_parent_directories=True)
repo_root = repo.working_tree_dir
keyword_replace_csv = repo_root + "/bin-data/keyword_links.csv"
keyword_regex = r"\@\[(.*?)\]\((.*?)\)"

# Example input text
test_str = "Viash automatically creates a @[mykeyword](this is the text that should appear) for components and @[executable](executables) with a Docker backend."
print("Input:")
print(test_str)

# Find all keyword links
matches = re.finditer(keyword_regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
	whole_match = match.group(0)
	keyword = match.group(1)
	text = match.group(2)
	link = "no-link"

	# Find keyword in csv
	keywords_csv = open(keyword_replace_csv)
	csvreader = csv.reader(keywords_csv)
	for row in csvreader:
		if row[0] == keyword:
			link = row[1]
			break
	keywords_csv.close()

	# Replace match with hyperlink
	test_str = test_str.replace(whole_match, f"[{text}]({link})")

# Print result
print("Output:")
print(test_str)