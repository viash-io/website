library(tibble)
library(rlang)
library(dplyr)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

# construct language tibble
langs <- tribble(
  ~id, ~label, ~script, ~script_type, ~container,
  "bash", "Bash", "script.sh", "bash_script", '"bash:4.0"',
  "csharp", "C#", "script.csx", "csharp_script", '"dataintuitive/dotnet-script:1.2.1"\n    setup: [{ type: apk, packages: bash }]',
  "js", "JavaScript", "script.js", "javascript_script", '"node:15-buster"',
  "python", "Python", "script.py", "python_script", '"python:3.10"',
  "r", "R", "script.R", "r_script", '"rocker/tidyverse:4.2"',
  "scala", "Scala", "script.scala", "scala_script", '"sbtscala/scala-sbt:eclipse-temurin-19_36_1.7.2_2.13.10"'
) %>%
  mutate(
    example_config = paste0(repo_path, "/_src/component_examples/example_", id, "/config.vsh.yaml"),
    example_script = paste0(repo_path, "/_src/component_examples/example_", id, "/", script)
  )