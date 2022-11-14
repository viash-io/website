library(fs)

## VIASH START
par <- list(
  "input" = 'file.txt',
  "output" = 'output.txt'
)
## VIASH END

cat("Copying '", par$input, "' to '", par$output, "'.\n")
file_copy(par$input, par$output)

