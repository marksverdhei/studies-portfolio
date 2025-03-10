import java.util.*;
import java.io.*;
public class Benchmark {
  final static int seed = 42;
  static double[][] a, b;
  @FunctionalInterface
  interface Matmul {
    public double[][] matmul(double[][] a, double[][] b);
  }

  public static void main(String[] args) {
    runBenchmarksAndWriteToFile();
  }

  public static void runBenchmarksAndWriteToFile() {
    Matmul defaultSeq = (double[][] a, double[][] b) -> Matrix.matmul(a, b);
    Matmul bTransposedSeq = (double[][] a, double[][] b) -> Matrix.matmulBTransposed(a, b);
    Matmul aTransposedSeq = (double[][] a, double[][] b) -> Matrix.matmulATransposed(a, b);
    Matmul defaultPara = (double[][] a, double[][] b) -> ParallelMatrix.matmul(a, b);
    Matmul bTransposedPara = (double[][] a, double[][] b) -> ParallelMatrix.matmulBTransposed(a, b);
    Matmul aTransposedPara = (double[][] a, double[][] b) -> ParallelMatrix.matmulATransposed(a, b);

    try {
      PrintWriter pw = new PrintWriter("benchmarks.txt");
      for (int i : new int[]{100, 200, 500, 1000}) {
        System.out.println("Benchmarking with "+i+"x"+i+" matrices");
        a = Oblig2Precode.generateMatrixA(seed, i);
        b = Oblig2Precode.generateMatrixB(seed, i);

        pw.println("n="+i+", mode=defaultSeq, time="+timeMatmul(defaultSeq, a,b));
        pw.println("n="+i+", mode=defaultPara, time="+timeMatmul(defaultPara, a,b));
        Matrix.transpose(b);
        pw.println("n="+i+", mode=bTransposedSeq, time="+timeMatmul(bTransposedSeq, a,b));
        pw.println("n="+i+", mode=bTransposedPara, time="+timeMatmul(bTransposedPara, a,b));
        Matrix.transpose(b);
        Matrix.transpose(a);
        pw.println("n="+i+", mode=aTransposedSeq, time="+timeMatmul(aTransposedSeq, a,b));
        pw.println("n="+i+", mode=aTransposedPara, time="+timeMatmul(aTransposedPara, a,b));


      }
      pw.flush();
      pw.close();
    } catch (FileNotFoundException e) {
      e.printStackTrace();
      System.exit(1);
    }


  }

  public static long timeMatmul(Matmul m, double[][] a, double[][] b) {
    long[] timings = new long[7];
    for (int i=0; i<7; i++) {
      long t0 = System.nanoTime();
      m.matmul(a, b);
      long t = System.nanoTime();
      timings[i] = t-t0;
    }
    Arrays.sort(timings);
    return timings[3];
  }
}
