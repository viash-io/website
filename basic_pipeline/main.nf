targetDir = "./target" // 1

include { remove_comments } from "$targetDir/remove_comments/main.nf" // 2

workflow {
  Channel.fromPath(params.input) // 3
    | map{ file -> [ file.baseName, file ] } // 4
    | view{ file -> "Input: $file" } // 5
    | remove_comments.run( // 6
      auto: [ publish: true ]
      )
    | view{ file -> "Output: $file" } // 7
}