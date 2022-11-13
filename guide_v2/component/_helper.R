# construct language tibble
langs <- tribble(
  ~id, ~label, ~script,
  "bash", "Bash", "script.sh",
  "python", "Python", "script.py",
  "r", "R", "script.R",
  "js", "JavaScript", "script.js",
  "scala", "Scala", "script.scala",
  "csharp", "C\\#", "script.csx"
)