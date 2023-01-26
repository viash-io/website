library(tibble)
library(rlang)
library(dplyr)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

# construct language tibble
langs <- tribble(
  ~id, ~label, ~script,
  "bash", "Bash", "script.sh",
  "csharp", "C\\#", "script.csx",
  "js", "JavaScript", "script.js",
  "python", "Python", "script.py",
  "r", "R", "script.R",
  "scala", "Scala", "script.scala"
) %>%
  mutate(
    example_config = paste0(repo_path, "/download/examples/example_", id, "/config.vsh.yaml"),
    example_script = paste0(repo_path, "/download/examples/example_", id, "/", script)
  )