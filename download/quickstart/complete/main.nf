targetDir = "./target/nextflow" 

include { remove_comments } from "$targetDir/example/remove_comments/main.nf" 
include { take_column } from "$targetDir/example/take_column/main.nf" 
include { combine_columns } from "$targetDir/example/combine_columns/main.nf" 

workflow {
  Channel.fromPath(params.input)
    | map{ file -> [ file.baseName, file ] }
    | remove_comments
    | take_column
    | toList()
    | map{ tups -> 
      files = tups.collect{id, file -> file}
      [ "combined", [ input: files ] ] 
      }
    | combine_columns.run(
      auto: [ publish: true ]
      )
    | view{ file -> "Output: $file" }
}