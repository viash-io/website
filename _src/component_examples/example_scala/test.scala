import scala.sys.process._
import java.nio.file.{Files, Paths}
import scala.io.Source

// VIASH START
case class ViashMeta(executable: String)
val meta = ViashMeta(
  "target/example_scala"
)
// VIASH END
val inputPath = Paths.get("foo.txt")
val outputPath = Paths.get("bar.txt")
val content = "hello\nthere"

println(">>> Create input test file")
Files.write(inputPath, content.getBytes("UTF-8"))

println(">>> Run executable")
s"${meta.executable} --input $inputPath --output $outputPath".!

println(">>> Check whether output file exists")
assert(Files.exists(outputPath), "Output file not found")

println(">>> Check whether input and output file are the same")
val outputLines = Source.fromFile(outputPath.toFile()).getLines.mkString("\n")
assert(
  content == outputLines, 
  s"""Output not the same
    |expected: '$content'
    |found: '$outputLines'
    |""".stripMargin
)

println(">>> Test finished successfully")