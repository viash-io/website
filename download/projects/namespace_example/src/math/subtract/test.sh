set -ex # Exit the script when one of the checks fail. Output all commands.

echo ">>> Checking whether output is correct"

# Run the component with and output the results to test-output.txt
"./$meta_functionality_name" --num1 100 --num2 20 > test-output.txt

# Check if test-output.txt exists
[[ ! -f test-output.txt ]] && echo "Test output file could not be found!" && exit 1 

# Check if we get the expected result
grep -q '80' test-output.txt 

# Exit with a 0 code to note a success 
echo ">>> Test finished successfully!"
exit 0 
