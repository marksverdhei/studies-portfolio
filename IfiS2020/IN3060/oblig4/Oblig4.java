import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.RDFS;
import org.apache.jena.util.FileManager;
import org.apache.jena.query.*;
import java.util.*;
import java.io.*;

public class Oblig4 {
  public static void main(String[] args) {
    if (args.length != 4) {
      System.out.println("Spply exactly 4 arguments:\ninputPath: path to the family graph\nqueryPath: path to the sparql construct query\noutputPath: path to the file to write\nsimpsonsUri: path or uri to simpsons.ttl");
      System.exit(1);
    }

    String inputPath, queryPath, outputPath, simpsonsUri;
    inputPath = args[0];
    queryPath = args[1];
    outputPath = args[2];
    simpsonsUri = args[3];
    String outputType = outputPath.split("\\.")[1];
    Model model = FileManager.get().loadModel(inputPath);
    model.add(FileManager.get().loadModel(simpsonsUri));

    InfModel inf = ModelFactory.createRDFSModel(model);

    Query q = QueryFactory.read(queryPath);
    System.out.println(q.toString());

    QueryExecution qexec = QueryExecutionFactory.create(q, inf);
    Model resultModel = qexec.execConstruct();
    qexec.close();

    //System.out.println(model);
    System.out.println(resultModel);
    try {
      PrintWriter pw = new PrintWriter(outputPath);
      resultModel.write(pw, outputType);
      System.out.println("*** Model successfully written to "+outputPath+" ***");
    } catch (Exception e) {
      System.out.println("Not able to write to file");
      e.printStackTrace();
    }
  }
}
