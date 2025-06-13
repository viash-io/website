workflow {
  ch = Channel.empty()

  ch << " a "
  ch << "   b"
  ch << "  c"
  ch << "d "

  ch
    | map{ elem -> elem.trim() }
    | subscribe{ print "$it" }
}