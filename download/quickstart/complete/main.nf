targetDir = "./target/nextflow" 

include { remove_comments } from "$targetDir/example/remove_comments/main.nf" 

workflow {
  Channel.fromPath(params.input) // 3
    | map{ file -> [ file.baseName, file ] } 
    | view{ file -> "Input: $file" }
    | remove_comments.run( 
    auto: [ publish: true ])
    | view{ file -> "Output: $file" } 
}