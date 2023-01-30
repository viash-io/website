import java.nio.file.StandardCopyOption.REPLACE_EXISTING
import java.nio.file.Files
import java.nio.file.Paths

// VIASH START
case class ViashPar(input: String, output: String)
val par = ViashPar(
  "path/to/file.txt",
  "output.txt"
)
// VIASH END

// copy file
println(s"Copying '${par.input}' to '${par.output}'.")
val fileIn = Paths.get(par.input)
val fileOut = Paths.get(par.output)
Files.copy(fileIn, fileOut, REPLACE_EXISTING)
