library(purrr)
library(tibble)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

qua <- ":::"
quo <- "```"

# run command and display as a mardown codeblock
# `...` doesn't work, for some reason
run_cmd <- function(command, args = character(), wd = NULL, error_on_status = TRUE, stderr_to_stdout = FALSE) {
  # run command
  cmd_out <- processx::run(
    command = command,
    args = args,
    wd = wd,
    error_on_status = error_on_status,
    stderr_to_stdout = stderr_to_stdout
  )

  # indent output
  out_indented <-
    strsplit(cmd_out$stdout, "\n")[[1]] %>%
    paste0("    ", .) %>%
    paste(., collapse = "\n")
  
  # format as markdown
  paste0(
    quo, "bash\n",
    command, " ", paste(args, collapse = " "), "\n",
    quo, "\n",
    "\n",
    out_indented, "\n"
  )
}