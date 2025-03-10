import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.RDFS;
import org.apache.jena.util.FileManager;
import java.util.*;
import java.io.*;

public class Simpsons {
  static Model model;
  public static void main(String[] args) {
    if (args.length != 2) {
      System.out.println("Supply two arguments\n\t[1]: path to input rdf-file\n\t[2]: path to output file");
      System.exit(1);
    }
    String rdfPath = args[0];
    String outPath = args[1];

    // Task 1:
    // TODO: Replace simpsons.ttl with rdfPath
    model = FileManager.get().loadModel("simpsons.ttl");
    // Task 2:
    String rdf, xsd, sim, fam, foaf;
    rdf = model.getNsPrefixURI("rdf");
    xsd = model.getNsPrefixURI("xsd");
    sim = model.getNsPrefixURI("sim");
    fam = model.getNsPrefixURI("fam");
    foaf = model.getNsPrefixURI("foaf");

    Resource maggie, mona, abe, herb, person;
    maggie = model.createResource(sim+"Maggie");
    mona = model.createResource(sim+"Mona");
    abe = model.createResource(sim+"Abraham");
    herb = model.createResource(sim+"Herb");
    person = model.createResource(foaf+"Person");

    Property type, age, name, hasSpouse, hasFather;
    type = model.createProperty(rdf+"type");
    age = model.createProperty(foaf+"age");
    name = model.createProperty(foaf+"name");
    hasSpouse = model.createProperty(fam+"hasSpouse");
    hasFather = model.createProperty(fam+"hasFather");

    model.add(model.createStatement(maggie, type, person));
    model.add(model.createStatement(maggie, name, model.createTypedLiteral("Maggie Simpson")));
    model.add(model.createStatement(maggie, age, model.createTypedLiteral(1)));

    model.add(model.createStatement(mona, type, person));
    model.add(model.createStatement(mona, name, model.createTypedLiteral("Mona Simpson")));
    model.add(model.createStatement(mona, age, model.createTypedLiteral(70)));

    model.add(model.createStatement(abe, type, person));
    model.add(model.createStatement(abe, name, model.createTypedLiteral("Abraham Simpson")));
    model.add(model.createStatement(abe, age, model.createTypedLiteral(78)));

    model.add(model.createStatement(abe, hasSpouse, mona));
    model.add(model.createStatement(mona, hasSpouse, abe));

    model.add(model.createStatement(herb, type, person));

    Resource herbsFather = model.createResource();
    model.add(model.createStatement(herb, hasFather, herbsFather));

    ResIterator resources = model.listResourcesWithProperty(type, person);

    Resource infant, minor, old;
    infant = model.createProperty(fam+"Infant");
    minor = model.createProperty(fam+"Minor");
    old = model.createProperty(fam+"Old");

    while (resources.hasNext()) {
       Resource r = resources.next();
       if (r.hasProperty(age)) {
         int ageValue = r.getRequiredProperty(age).getInt();
         if (ageValue < 2) {
           model.add(model.createStatement(r, type, infant));
         }

         if (ageValue < 18) {
           model.add(model.createStatement(r, type, minor));
         }

         if (ageValue > 70) {
           model.add(model.createStatement(r, type, old));
         }

       }
    }

    PrintWriter pw = null;
    try {
      pw = new PrintWriter(outPath);
    } catch (FileNotFoundException e) {
      System.out.println(e);
      System.exit(1);
    }
    model.write(pw, "ttl");
  }
}
