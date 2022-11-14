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

run_quarto <- function(src_qmd, dir = tempdir(), engine = "knitr") {
  # generate temp file path
  file_qmd <- tempfile(pattern = "quarto_inline_", tmpdir = dir, fileext = ".qmd")
  file_md <- gsub("\\.qmd$", ".md", file_qmd)

  src_and_header <- paste0("---\nengine: ", engine, "\n---\n\n", src_qmd)
  # write qmd source code
  readr::write_lines(src_and_header, file_qmd)

  # run quarto
  out <- processx::run(
    command = "quarto",
    args = c(
      "render", file_qmd,
      "--to", "markdown",
      "--output", "-"
    )
  )

  # strip header
  src_md1 <- paste(paste0(out$stdout, "\n"), collapse = "")
  src_md2 <- gsub("---.*\n---\n+", "", src_md1)
  src_md2
}


run_knitr <- function(src, dir = NULL) {
  if (!is.null(dir)) {
    src <- paste0(
      "```{r set-root}\n",
      "knitr::opts_knit$set(root.dir = '", dir, "')\n",
      "```\n\n",
      src
    )
  }
  knitr::knit(text = src)
}
