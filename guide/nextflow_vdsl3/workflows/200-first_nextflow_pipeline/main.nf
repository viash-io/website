workflow {
  Channel.fromList( [" a ", "   b", "  c", "d  "] )
    | map{ elem -> elem.trim() }
    | view
}