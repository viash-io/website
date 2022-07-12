set -ex # Exit the script when one of the checks fail. Output all commands.

# Check 1
echo ">>> Checking whether output is correct"

# Run md_url_checker component with its required inputs and output the results to test-output.txt
./md_url_checker --inputfile Testfile.md > test-output.txt

[[ ! -f test-output.txt ]] && echo "Test output file could not be found!" && exit 1 # Check if test-output.txt exists
grep -q '1: https://www.google.com' test-output.txt # Did the script find the URL?
grep -q 'HTTP/2 404' test-output.txt  # Did the web request return a 404 for the page that doesn't exist?

# Check 2
echo ">>> Checking whether an output file was created correctly"

[[ ! -f output.txt ]] && echo "Output file could not be found!" && exit 1 # Check if output.txt exists
grep -q 'URL: https://www.google.com' output.txt # Was the URL written correctly in the report?
grep -q 'Status: ERROR! URL cannot be reached. Status code: HTTP/2 404' output.txt # Was the error written correctly in the report?
grep -q 'Link name: install viash here' output.txt # Was link name written correctly in the report?

echo ">>> Test finished successfully!"
exit 0 # Exit with a 0 code to note a success 
