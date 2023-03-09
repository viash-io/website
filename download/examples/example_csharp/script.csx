using System.IO;

// VIASH START
var par = new {
  input = "path/to/file.txt",
  output = "output.txt"
};
// VIASH END

// copy file
Console.WriteLine($"Copying '{par.input}' to '{par.output}'.");
File.Copy(par.input, par.output, true);
