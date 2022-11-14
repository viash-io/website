using System.IO;

// VIASH START
var par = new {
  input = "path/to/file.txt",
  output = "output.txt"
};
// VIASH END

Console.WriteLine($"Copying '{par.input}' to '{par.output}'.");

// To copy a file to another location and
// overwrite the destination file if it already exists.
File.Copy(par.input, par.output, true);
