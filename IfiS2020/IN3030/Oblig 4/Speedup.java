import java.util.*;
import java.io.PrintWriter;
import java.io.FileNotFoundException;

public class Speedup {
  static boolean writeToFile = false;
  static boolean full = false;
  static boolean prints = true;
  static int n = 10000000;
  static int t = Runtime.getRuntime().availableProcessors();
  static boolean verify = false;
  static int seed = 0;
  static PrintWriter writer = null;

  public static void parseArgs(String[] args)  {
    if (args.length == 0) System.out.println("No arguments supplied. Run the program with -h or --help to see the list of arguments");
    for (String s : args) {
      switch (s) {
        case "-h":
        case "--help":
          System.out.println("Speedup: program to measure ParallelRadixSort and Oblig4");
          System.out.println("n=[integer] | the input size of the two algorithms. Defaults to 10000000");
          System.out.println("seed=[integer] | the seed for the randomly generated arrays");
          System.out.println("t=[integer] | the number of threads to be used. Defaults to Runtime.getRuntime().availableProcessors()");
          System.out.println("-f, --full | bencmarks runtimes with inputs 1000, 10000, ..., 100000000");
          System.out.println("-v, --verify | verifies that the arrays are sorted as described in the obligtext");
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
            } else if (arg[0].equals("t")) {
              t = value;
            } else if (arg[0].equals("seed")) {
              seed = value;
            } else {
              // hacky :))
              throw new IndexOutOfBoundsException();
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
      for (int i=1000; i<100000001; i*=10) {
        n = i;
        runBenchmark();
      }
    } else {
      runBenchmark();
    }

    if (writeToFile) writer.close();
  }


  public static void runBenchmark() {
    Oblig4 seq = new Oblig4(n, seed);
    ParallelRadixSort para = new ParallelRadixSort(n, seed, t);
    long[] medianSeq = new long[7];
    long[] medianPara = new long[7];
    for (int i=0; i<7; i++) {
      int[] arr1 = Oblig4Precode.generateArray(n, seed);
      int[] arr2 = Arrays.copyOf(arr1, arr1.length);
      long s1 = System.nanoTime();
      int[] seqArr = seq.sort(arr1);
      long s2 = System.nanoTime();
      int[] paraArr = para.sort(arr2);
      long s3 = System.nanoTime();
      medianSeq[i] = s2-s1;
      medianPara[i] = s3-s2;
      if (prints) {
        System.out.println("Equal arrays? "+Arrays.equals(seqArr, paraArr));
      }

      if (verify) {
        verifySort(seqArr, "sequential");
        verifySort(paraArr, "parallel");
      }
    }
    Arrays.sort(medianSeq);
    Arrays.sort(medianPara);
    long seqMilis = medianSeq[3]/1000000;
    long paraMilis = medianPara[3]/1000000;
    double speedup = (double)seqMilis/(double)paraMilis;
    if (prints) System.out.println("Median seq time:"+seqMilis+"ms");
    if (prints) System.out.println("Median parallel time:"+paraMilis+"ms");
    if (prints) System.out.println("Speedup: "+speedup);
    if (writeToFile) {
      writer.print(n+",");
      writer.print(seqMilis+",");
      writer.print(paraMilis+",");
      writer.println(speedup);
    }
  }

  public static void verifySort(int[] arr, String message) {
    int j = 0;
    for (int i=1; i<arr.length; i++) {
      if (arr[j] > arr[i]) {
        throw new RuntimeException("Unsorted digit on index "+i+" ("+arr[j]+" > "+arr[i]+")");
      }
    }
    System.out.println("Verified that "+message+" array: is sorted");
  }
}
