import java.nio.file.StandardCopyOption.REPLACE_EXISTING
import java.nio.file.Files
import java.nio.file.Paths

println(s"Copying '${par.input}' to '${par.output}'.")

Files.copy(Paths.get(par.output), Paths.get(par.output), REPLACE_EXISTING)
