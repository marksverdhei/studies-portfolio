import java.util.Arrays;
import java.io.PrintWriter;
import java.io.FileNotFoundException;

public class Speedup {
  static boolean writeToFile = false;
  static boolean full = false;
  static boolean prints = true;
  static int n = 100;
  static int t = 0;
  static boolean verify = false;
  static int seed = 0;
  static PrintWriter writer = null;

  public static void parseArgs(String[] args)  {
    if (args.length == 0) {
        System.out.println("No arguments supplied. Run the program with -h or --help to see the list of arguments");
        // System.exit(1);
    }

    for (String s : args) {
      switch (s) {
        case "-h":
        case "--help":
          System.out.println("Speedup: program to measure the sequential and parallel convex hull algorithm");
          System.out.println("n=[integer] | the input size of the two algorithms. Defaults to 100");
          System.out.println("seed=[integer] | the seed for the randomly generated points");
          System.out.println("-f, --full | bencmarks runtimes with inputs 100, 1000, ..., 10000000");
          System.out.println("-v, --verify | verifies that the parallel and sequential versions give equal results");
          System.out.println("-tf, --toFile | writes the measurements to the file speedups.txt");
          System.out.println("-q, --quiet | runs the program without printing to the console");
          System.exit(0);
          break;

        case "-f":
        case "--full":
          full = true;
          break;

        case "-v":
        case "--verify":
          verify = true;
          break;

        case "-tf":
        case "--toFile":
          writeToFile = true;
          break;

        case "-q":
        case "--quiet":
          prints = false;
          break;

        default:
          try {
            String[] arg = s.split("=");
            int value = Integer.parseInt(arg[1]);
            if (arg[0].equals("n")) {
              n = value;
            } else if (arg[0].equals("seed")) {
              seed = value;
            } else {
              // hacky :))
              throw new Exception();
            }
          } catch (Exception e) {
            System.out.println("Was not able to interpret argument: '"+s+"'");
            System.out.println("Proceeding");
          }
          break;
      }
    }
  }
  public static void main(String[] args) {
    parseArgs(args);

    if (writeToFile) {
      try {
        writer = new PrintWriter("speedups.txt");
      } catch (FileNotFoundException e) {
        System.out.println("File not found, proceeding without writing to file");
        writeToFile = false;
      }
    }

    if (full) {
      for (int i=100; i<10000001; i *= 10) {
        n = i;
        runBenchmark();
      }
    } else {
      runBenchmark();
    }

    if (writeToFile) writer.close();
  }


  public static void runBenchmark() {
    long[] medianSeq = new long[7];
    long[] medianPara = new long[7];
    for (int i=0; i<7; i++) {
      // TODO: PREPARE INPUTS
      Oblig5 seq = new Oblig5(n, seed);
      Oblig5 para = new Oblig5(n, seed);
      long s1 = System.nanoTime();
      // Perform sequential algorithm
      seq.initSeq();
      long s2 = System.nanoTime();
      // perform parallel algorithm
      para.initPara();
      long s3 = System.nanoTime();
      medianSeq[i] = s2-s1;
      medianPara[i] = s3-s2;

      if (prints) {

      }

      if (verify) {
        verifyEqualResults(seq, para);
      }
    }
    Arrays.sort(medianSeq);
    Arrays.sort(medianPara);
    long seqMilis = medianSeq[3]/1000000;
    long paraMilis = medianPara[3]/1000000;
    double speedup = (double)medianSeq[3]/(double)medianPara[3];
    if (prints) System.out.println("Input size: "+n);
    if (prints) System.out.println("Median seq time:"+seqMilis+"ms");
    if (prints) System.out.println("Median parallel time:"+paraMilis+"ms");
    if (prints) System.out.println("Speedup: "+speedup);
    if (writeToFile) {
      writer.print(n+",");
      writer.print(medianSeq[3]+",");
      writer.print(medianPara[3]+",");
      writer.println(speedup);
    }
  }

  public static void verifyEqualResults(Oblig5 seq, Oblig5 para) {
    if (!seq.coHull.equals(para.coHull)) {
        throw new RuntimeException("NOT EQUAL RESULTS:\nSEQ: "+Arrays.toString(seq.coHull.data)+"\nPARA:"+Arrays.toString(para.coHull.data)+"\n");
    }
  }
}
