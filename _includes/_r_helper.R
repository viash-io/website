library(purrr)
library(tibble)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

qua <- ":::"
quo <- "```"

strip_margin <- function(str, margin = "\\|") {
  regex <- paste0("(\\n?)[ \\t]*", margin)
  gsub(regex, "\\1", str)
}

# # run command and display as a mardown codeblock
# # `...` doesn't work, for some reason
# run_cmd <- function(command, args = character(), wd = NULL, error_on_status = TRUE, stderr_to_stdout = FALSE) {
#   # run command
#   cmd_out <- processx::run(
#     command = command,
#     args = args,
#     wd = wd,
#     error_on_status = error_on_status,
#     stderr_to_stdout = stderr_to_stdout
#   )

#   # indent output
#   out_indented <-
#     strsplit(cmd_out$stdout, "\n")[[1]] %>%
#     paste0("    ", .) %>%
#     paste(., collapse = "\n")
  
#   # format as markdown
#   paste0(
#     quo, "bash\n",
#     command, " ", paste(args, collapse = " "), "\n",
#     quo, "\n",
#     "\n",
#     out_indented, "\n"
#   )
# }

# render code as qmd and display as markdown
run_quarto <- function(src_qmd, wdir, engine = "knitr") {
  # generate temp file path
  file_qmd <- tempfile(pattern = "quarto_inline_", fileext = ".qmd")
  on.exit(file.remove(file_qmd))

  # assume src does not contain a header
  src_and_header <- strip_margin(glue::glue("
    |---
    |engine: {engine}
    |---
    |
    |{quo}{{r setup, include=FALSE}}
    |knitr::opts_knit$set(root.dir = '{wdir}')
    |{quo}
    |
    |{src_qmd}
    |"))

  # write qmd source code
  readr::write_lines(src_and_header, file_qmd)

  # render to markdown
  out <- processx::run(
    command = "quarto",
    args = c(
      "render", file_qmd,
      "--to", "markdown",
      "--output", "-"
    ),
    echo=FALSE,
    error_on_status = FALSE
  )

 if (out$status != 0) {
    stop(out$stderr)
  }

  # strip header
  paste0(out$stdout, "\n") %>%
    paste(collapse = "") %>%
    gsub("---.*\n---\n+", "", .) %>%
    # escape hashes in titles
    strsplit("\n") %>% .[[1]] %>%
    gsub("^(#+[^#\n]+)#(.*)", "\\1\\\\#\\2", .) %>%
    paste(collapse = "\n")
}

qrt <- function(
  qmd_txt,
  .dir = tempdir(),
  .envir = parent.frame(),
  .open = "{%",
  .close = "%}",
  .margin = "\\|",
  .eval = any(grepl("``` *\\{", qmd_txt))
) {
  qmd_glued <- glue::glue(qmd_txt, .envir = .envir, .open = .open, .close = .close)
  qmd_stripped <- strip_margin(qmd_glued, margin = .margin)
  md <-
    if (.eval) {
      run_quarto(qmd_stripped, .dir)
    } else {
      qmd_stripped
    }
  cat(md)
}

write_yaml <- function(x, file, ...) {
  handlers <- list(
    logical = function(x) {
      result <- ifelse(x, "true", "false")
      class(result) <- "verbatim"
      return(result)
    }
  )
  yaml::write_yaml(
    x = x,
    file = file,
    handlers = handlers,
    indent.mapping.sequence = TRUE,
    ...
  )
}