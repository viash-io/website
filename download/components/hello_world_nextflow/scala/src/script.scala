import java.io._

val writer = new FileWriter(par.output.get)
try { writer.append("Hello " + par.input.get) }
finally { writer.close }        