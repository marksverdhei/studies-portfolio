import java.util.*;
import java.io.PrintWriter;
import java.io.FileNotFoundException;

public class TestOblig1 {
  static Random random = new Random(0);

  @FunctionalInterface
  public interface A2 {
    public int[] findKgreatest(int[] a, int k);
  }

  public static long timeA2(A2 algorithm, int[] a, int k, String message) {
    long startTime, endTime, diff;
    startTime = System.nanoTime();
    algorithm.findKgreatest(a, k);
    endTime = System.nanoTime();
    diff = endTime-startTime;
    System.out.println(message);
    System.out.println("Time: "+diff+"ns");
    return diff;
  }

  public static void testCorrectness() {
    try {
      assert false;
      System.out.println("Assertions not enabled. Run java with flag -ea to enable");
    } catch (AssertionError e) {
      System.out.println("Assertions enabled\nTesting correctness");
    }

    int[] a, b, z, y;
    long startTime, endTime;
    int k;

    // start on small array
    a = new int[]{1, 2, 3, 4, 5, 6, 7, 8};
    y = Oblig1.a1(a, 5);

    b = Arrays.copyOf(a, a.length);
    z = Oblig1.a2sequential(a, 5);
    assert Arrays.equals(a, b) : "Mutated original array";
    System.out.println("Results:");
    System.out.println("y = " + Arrays.toString(y));
    System.out.println("z = " + Arrays.toString(z));
    assert Arrays.equals(z, y) : "Wrong result";

    z = Oblig1.a2parallel(a, 5, 2);
    assert Arrays.equals(a, b) : "Mutated original array";
    System.out.println("y = " + Arrays.toString(y));
    System.out.println("z = " + Arrays.toString(z));
    assert Arrays.equals(z, y) : "Wrong result";

    z = Oblig1.a2parallel(a, 5, 4);
    assert Arrays.equals(a, b) : "Mutated original array";
    System.out.println("y = " + Arrays.toString(y));
    System.out.println("z = " + Arrays.toString(z));
    assert Arrays.equals(z, y) : "Wrong result";


    for (int i=5; i<1000000; i*=2) {
      System.out.println("Size "+i);
      a = new int[i];
      for (int j=0; j<a.length; j++) a[j] = random.nextInt();
      b = Arrays.copyOf(a, a.length);
      y = Oblig1.a1(a, 5);
      z = Oblig1.a2parallel(a, 5, 4);
      assert Arrays.equals(a, b) : "Mutated original array";
      System.out.println("Sequential answer = " + Arrays.toString(y));
      System.out.println("Parallel answer = " + Arrays.toString(z));
      assert Arrays.equals(z, y) : "Wrong result";
    }


  }

  public static long findMedian(long[] a) {
    long[] b = Arrays.copyOf(a, a.length);
    Arrays.sort(b);
    if (b.length % 2 == 0) {
      return (b[b.length/2] + b[(b.length/2)+1])/2;
    } else {
      return b[(b.length/2)+1];
    }
  }

  public static long[][] testTimings(int n) {

    A2 a1 = (int[] a, int k) -> Oblig1.a1(a, k);
    A2 p1 = (int[] a, int k) -> Oblig1.a2parallel(a, k, 2);
    A2 p2 = (int[] a, int k) -> Oblig1.a2parallel(a, k, 4);
    A2 p3 = (int[] a, int k) -> Oblig1.a2parallel(a, k, 8);
    A2 p4 = (int[] a, int k) -> Oblig1.a2parallel(a, k, 16);
    A2 p5 = (int[] a, int k) -> Oblig1.a2parallel(a, k, 32);
    A2 sequential = (int[] a, int k) -> Oblig1.a2sequential(a, k);

    if (n >= 1000000000) {
      System.out.println("Array size too high for a1");
      a1 = (int[] a, int k) -> {
        return new int[0];
      };
    }

    int[] a, z;
    long[][] timings = new long[2][7];
    long startTime, endTime;
    int e = 0;
    for (int k=20; k<=100; k+= 80) {
      a = new int[n];
      for (int i=0; i<a.length; i++) a[i] = random.nextInt();
      System.out.println("Array size: "+n);
      timings[e] = new long[7];
      long[][] tempMarks = new long[7][7];
      for (int i=0; i<7; i++) {
        tempMarks[0][i] = timeA2(a1, a, k, "Running a1 with k = " + k);
        tempMarks[1][i] = timeA2(sequential, a, k, "Running Sequential with k = " + k);
        tempMarks[2][i] = timeA2(p1, a, k, "Running parallel with 2 threads k = " + k);
        tempMarks[3][i] = timeA2(p2, a, k, "Running parallel with 4 threads k = " + k);
        tempMarks[4][i] = timeA2(p3, a, k, "Running parallel with 8 threads k = " + k);
        tempMarks[5][i] = timeA2(p4, a, k, "Running parallel with 16 threads k = " + k);
        tempMarks[6][i] = timeA2(p5, a, k, "Running parallel with 32 threads k = " + k);
      }

      for (int i=0; i<7; i++) {
        timings[e][i] = findMedian(tempMarks[i]);
      }
      e++;
    }
    return timings;
  }

  public static void runBenchmarksAndWriteToFile() {
    PrintWriter pw = null;
    try {
      pw = new PrintWriter("benchmarks.csv");
    } catch (FileNotFoundException e) {
      e.printStackTrace();
      System.exit(1);
    }

    for (int n=1000; n<=100000000; n*=10) {
      pw.println("n = "+n);
      long[][] timings = testTimings(n);
      pw.println("k = 20");
      for (long i : timings[0]) {
        pw.print(i+",");
      }
      pw.println();
      pw.println("k = 100");
      for (long i : timings[1]) {
        pw.print(i+",");
      }
      pw.println();
    }
    pw.close();
  }

  public static void main(String[] args) {
    testCorrectness();
    runBenchmarksAndWriteToFile();
    // int n;
    // if (args.length > 0) {
    //   n = Integer.parseInt(args[0]);
    // } else {
    //   n = 1000000;
    // }
    // testTimings(n);

  }
}
