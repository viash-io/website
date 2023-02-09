## VIASH START
meta <- list(
  "target/example_r"
)
## VIASH END

input_path <- "foo.txt"
output_path <- "bar.txt"
content <- c("hello", "there")

cat(">>> Create input test file\n")
writeLines(content, input_path)

cat(">>> Run executable\n")
system2(
  meta$executable,
  c(
    "--input", input_path,
    "--output", output_path
  )
)

cat(">>> Check whether output file exists\n")
if (!file.exists(output_path)) {
  stop("Output file was not found")
}

cat(">>> Check whether input and output file are the same\n")
output_lines <- readLines(output_path)

if (!identical(content, output_lines)) {
  stop(paste0(
    "Input and output should be the same\n",
    "expected content: ", content, "\n",
    "found: ", output_lines, "\n"
  ))
}

cat(">>> Test finished successfully\n")
