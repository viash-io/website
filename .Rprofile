source("renv/activate.R")

if (requireNamespace("knitr", quietly = TRUE)) {
  local({
    hook_old <- knitr::knit_hooks$get("output")  # save the old hook
    knitr::knit_hooks$set(output = function(x, options) {
      regex = "(?:(?:\\x{001b}\\[)|\\x{009b})(?:(?:[0-9]{1,3})?(?:(?:;[0-9]{0,3})*)?[A-M|f-m])|\\x{001b}[A-M]"
      out <- gsub(regex, "", x, perl = TRUE, useBytes = TRUE)
      hook_old(out, options)
    })
  })
}