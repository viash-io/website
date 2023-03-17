library(tibble)
library(rlang)
library(dplyr)

repo_path <- system("git rev-parse --show-toplevel", intern = TRUE)

# construct language tibble
langs <- tribble(
  ~id, ~label, ~script, ~script_type, ~container,
  "bash", "Bash", "script.sh", "bash_script", '"bash:4.0"',
  "csharp", "C#", "script.csx", "csharp_script", '"ghcr.io/data-intuitive/dotnet-script:1.3.1"',
  "js", "JavaScript", "script.js", "javascript_script", '"node:19-bullseye-slim"',
  "python", "Python", "script.py", "python_script", '"python:3.10-slim"',
  "r", "R", "script.R", "r_script", '"eddelbuettel/r2u:22.04"',
  "scala", "Scala", "script.scala", "scala_script", '"sbtscala/scala-sbt:eclipse-temurin-19_36_1.7.2_2.13.10"'
) %>%
  mutate(
    example_config = paste0(repo_path, "/_src/component_examples/example_", id, "/config.vsh.yaml"),
    example_script = paste0(repo_path, "/_src/component_examples/example_", id, "/", script)
  )