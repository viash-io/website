targetDir = "../../target/nextflow" // 1

// 2
include { remove_comments } from "$targetDir/nextflow_modules/remove_comments/main.nf"
include { take_column } from "$targetDir/nextflow_modules/take_column/main.nf"
include { combine_columns } from "$targetDir/nextflow_modules/combine_columns/main.nf"

workflow {
  Channel.fromPath(params.input) // 3
  
    // 4
    // File -> (String, File)
    | map{ file -> [ file.baseName, file ] }
    
    // 5
    // (String, File) -> (String, File)
    | remove_comments

    // 6
    // (String, File) -> (String, File)
    | take_column

    // 7
    // (String, File)* -> List[(String, File)]
    | toList()

    // 8
    // List[(String, File)] -> (String, {input: List[File]})
    | map{ tups -> 
      files = tups.collect{id, file -> file}
      [ "combined", [ input: files ] ] 
    }

    // 9
    // (String, {input: List[File]}) -> (String, File)
    | combine_columns.run(
      auto: [ publish: true ]
      )

    // 10
    | view{ file -> "Output: $file" }
}