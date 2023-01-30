## VIASH START
par <- list(
  "input" = 'file.txt',
  "output" = 'output.txt'
)
## VIASH END

# copy file
cat("Copying '", par$input, "' to '", par$output, "'.\n", sep = "")
file.copy(par$input, par$output)
