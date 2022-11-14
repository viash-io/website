library(tibble)
library(rlang)
library(dplyr)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

# construct language tibble
langs <- tribble(
  ~id, ~label, ~script,
  "bash", "Bash", "script.sh",
  "python", "Python", "script.py",
  "r", "R", "script.R",
  "js", "JavaScript", "script.js",
  "scala", "Scala", "script.scala",
  "csharp", "C\\#", "script.csx"
) %>%
  mutate(
    example_config = paste0(repo_path, "/download/examples/example_", id, "/config.vsh.yaml"),
    example_script = paste0(repo_path, "/download/examples/example_", id, "/", script)
  )