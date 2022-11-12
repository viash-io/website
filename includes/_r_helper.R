library(purrr)
library(tibble)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

# construct language tibble
langs <- tribble(
  ~id, ~label, ~script,
  "bash", "Bash", "script.sh",
  "csharp", "C\\#", "script.csx",
  "js", "JavaScript", "script.js",
  "python", "Python", "script.py",
  "scala", "Scala", "script.scala",
  "r", "R", "script.R"
)

qua <- ":::"
quo <- "```"

run_cmd <- function(command, args = character(), wd = NULL) {
  # run command
  cmd_out <- processx::run(
    command = command,
    args = args,
    wd = wd
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