import org.apache.jena.rdf.model.*;
import org.apache.jena.datatypes.xsd.XSDDatatype;
import java.io.*;
import java.util.*;
import org.apache.jena.query.*;
import org.apache.jena.reasoner.*;

public class Oblig4 {
  Oblig4(){
  }
  static Model load(String path){
    //Creates a default model from given path and returns it
    Model m = ModelFactory.createDefaultModel();
    m = m.read(path);
    return m;
  }

  static String read(String file)throws IOException{
    //Reads file and returns contents as string
    File f = new File(file);
    BufferedReader br = new BufferedReader(new FileReader(file));
    String query = "";
    String st;
    while ((st = br.readLine()) != null){
      query = query + st;
    }

    return query;
  }

  static void write(String out, Model m){
    //Writes model to file with filename out
    try{
      m.write(new FileOutputStream(out), "TTL");
    }
    catch(IOException e){
      System.out.println("File not found");
    }
  }

  public static void main(String[] args)throws IOException{
    /*
    compile:
      javac -cp "/path/to/jena/lib/*" Oblig4.java
    run:
      java -cp "/path/to/jena/lib/*;" Oblig4 family.ttl oblig4.rq out.ttl simpsons.ttl
    */
    Model graph = load(args[0]); //Argument 1: RDFS file
    String queryString = read(args[1]); //Argument 2: query file
    //String out_path = args[2];  //Argument 3: output filename
    //Model graph = load(args[3]);  //Argument 4: simpsons.ttl file

    //Reasoner reas = ReasonerRegistry.getOWLReasoner();
    //InfModel rm = ModelFactory.createInfModel(reas, rdfs, graph);
    Query query = QueryFactory.create(queryString);
    QueryExecution qexec = QueryExecutionFactory.create(query, graph);
    ResultSet result = qexec.execSelect();
    String toPrint = ResultSetFormatter.asText(result);
    System.out.println(toPrint);

    qexec.close();
    //System.out.println(resultModel);
    //write(out_path, rm.add(resultModel));

    //System.out.println("Result model written to file: " + out_path);
  }
}
//https://sws.ifi.uio.no/in3060/v20/oblig/3/simpsons.ttl
