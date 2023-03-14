using System;
using System.IO;
using System.Diagnostics;

// VIASH START
var meta = new {
  executable = "target/example_csharp"
};
// VIASH END

string inputPath = "foo.txt";
string outputPath = "bar.txt";
string content = "hello\nthere\n";

Console.WriteLine(">>> Create input test file");
File.WriteAllText(inputPath, content);

Console.WriteLine(">>> Run executable");

var startInfo = new ProcessStartInfo(meta.executable)
{
    Arguments = $"--input {inputPath} --output {outputPath}",
    UseShellExecute = false,
    RedirectStandardOutput = true,
    CreateNoWindow = true
};
using(var cmd = Process.Start(startInfo))
{
    cmd.WaitForExit();
}


Console.WriteLine(">>> Check whether output file exists");
if (!File.Exists(outputPath)) {
    Console.WriteLine("Output file was not found");
    Environment.Exit(1);
}

Console.WriteLine(">>> Check whether input and output file are the same");
var outputLines = File.ReadAllText(outputPath);
if (content != outputLines) {
    Console.WriteLine(
        "Input and output should be the same\n" +
        $"expected content: {content}\n" +
        $"found: {outputLines}\n"
    );
    Environment.Exit(1);
}

Console.WriteLine(">>> Test finished successfully");