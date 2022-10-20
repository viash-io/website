Console.WriteLine($"Copying '{par.input}' to '{par.output}'.");

// To copy a file to another location and
// overwrite the destination file if it already exists.
System.IO.File.Copy(par.input, par.output, true);