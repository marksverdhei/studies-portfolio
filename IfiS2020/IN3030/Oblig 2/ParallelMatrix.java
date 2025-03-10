import java.util.concurrent.*;
import java.util.*;
public class ParallelMatrix {

  public static int arrHalf(int n) {
    // useful utility when partitioning
    return n/2 + (n % 2);
  }

  public static double[][] matmul(double[][] a, double[][] b) {
    int p = Runtime.getRuntime().availableProcessors();
    int threads = (int)Math.pow(4, Math.ceil(Math.log(p)/Math.log(4)));

    int n = a.length;
    double[][] c = new double[n][n];
    CountDownLatch stopSignal = new CountDownLatch(threads);

    int yl = 0;
    int yr = n-1;
    int xl = 0;
    int xr = n-1;

    recursivePartition(p, yl, yr, xl, xr, a, b, c, stopSignal);
    try {
      stopSignal.await();
    } catch (InterruptedException e) {
      e.printStackTrace();
      System.exit(1);
    }
    return c;
  }

  public static double[][] matmulBTransposed(double[][] a, double[][] b) {
    int p = Runtime.getRuntime().availableProcessors();
    int threads = (int)Math.pow(4, Math.ceil(Math.log(p)/Math.log(4)));

    int n = a.length;
    double[][] c = new double[n][n];
    CountDownLatch stopSignal = new CountDownLatch(threads);

    int yl = 0;
    int yr = n-1;
    int xl = 0;
    int xr = n-1;

    recursivePartitionBTransposed(p, yl, yr, xl, xr, a, b, c, stopSignal);
    try {
      stopSignal.await();
    } catch (InterruptedException e) {
      e.printStackTrace();
      System.exit(1);
    }
    return c;
  }

  public static double[][] matmulATransposed(double[][] a, double[][] b) {
    int p = Runtime.getRuntime().availableProcessors();
    int threads = (int)Math.pow(4, Math.ceil(Math.log(p)/Math.log(4)));
    // optionally split them into 2 if the partition can be split into 2
    // int threads = (int)Math.pow(2, Math.ceil(Math.log(p)/Math.log(2)));

    int n = a.length;
    double[][] c = new double[n][n];
    CountDownLatch stopSignal = new CountDownLatch(threads);

    int yl = 0;
    int yr = n-1;
    int xl = 0;
    int xr = n-1;

    recursivePartitionATransposed(p, yl, yr, xl, xr, a, b, c, stopSignal);
    try {
      stopSignal.await();
    } catch (InterruptedException e) {
      e.printStackTrace();
      System.exit(1);
    }
    return c;
  }

  public static void calculateSingleCell(int i, int j, double[][] a, double[][] b, double[][] c) {
    for (int k=0; k<c.length; k++) c[i][j] += a[i][k] * b[k][j];
  }

  public static void calculateSingleCellBTransposed(int i, int j, double[][] a, double[][] b, double[][] c) {
    for (int k=0; k<c.length; k++) c[i][j] += a[i][k] * b[j][k];
  }

  public static void calculateSingleCellATransposed(int i, int j, double[][] a, double[][] b, double[][] c) {
    for (int k=0; k<c.length; k++) c[i][j] += a[k][i] * b[k][j];
  }

  /**
   *
   * @param p number of remaining cores
   *
   */
  public static void recursivePartition(int p, int yl, int yr, int xl, int xr,
          double[][] a, double[][] b, double[][] c, CountDownLatch stopSignal) {
    if (p <= 1 || yr-yl == 0 || xr-xl == 0) {
      Runnable t = () -> {
        calculatePartition(yl, yr, xl, xr, a, b, c);
        stopSignal.countDown();
      };
      new Thread(t).start();
    // } else if (p == 2) {
    // consider splitting into two to reduce overhead
    } else {
      int q = p/4;
      int yH = arrHalf(yr);
      int xH = arrHalf(xr);

      recursivePartition(q, yl, yH, xl, xH, a, b, c, stopSignal);
      recursivePartition(q, yl, yH, xH+1, xr, a, b, c, stopSignal);
      recursivePartition(q, yH+1, yr, xl, xH, a, b, c, stopSignal);
      recursivePartition(q, yH+1, yr, xH+1, xr, a, b, c, stopSignal);
    }
  }

  public static void recursivePartitionBTransposed(int p, int yl, int yr, int xl, int xr,
          double[][] a, double[][] b, double[][] c, CountDownLatch stopSignal) {
    if (p <= 1 || yr-yl == 0 || xr-xl == 0) {
      Runnable t = () -> {
        calculatePartitionBTransposed(yl, yr, xl, xr, a, b, c);
        stopSignal.countDown();
      };
      new Thread(t).start();
    // } else if (p == 2) {
    // consider splitting into two to reduce overhead
    } else {
      int q = p/4;
      int yH = arrHalf(yr);
      int xH = arrHalf(xr);

      recursivePartitionBTransposed(q, yl, yH, xl, xH, a, b, c, stopSignal);
      recursivePartitionBTransposed(q, yl, yH, xH+1, xr, a, b, c, stopSignal);
      recursivePartitionBTransposed(q, yH+1, yr, xl, xH, a, b, c, stopSignal);
      recursivePartitionBTransposed(q, yH+1, yr, xH+1, xr, a, b, c, stopSignal);
    }
  }

  public static void recursivePartitionATransposed(int p, int yl, int yr, int xl, int xr,
          double[][] a, double[][] b, double[][] c, CountDownLatch stopSignal) {
    if (p <= 1 || yr-yl == 0 || xr-xl == 0) {
      Runnable t = () -> {
        calculatePartitionATransposed(yl, yr, xl, xr, a, b, c);
        stopSignal.countDown();
      };
      new Thread(t).start();
    // } else if (p == 2) {
    // consider splitting into two to reduce overhead
    } else {
      int q = p/4;
      int yH = arrHalf(yr);
      int xH = arrHalf(xr);

      recursivePartitionATransposed(q, yl, yH, xl, xH, a, b, c, stopSignal);
      recursivePartitionATransposed(q, yl, yH, xH+1, xr, a, b, c, stopSignal);
      recursivePartitionATransposed(q, yH+1, yr, xl, xH, a, b, c, stopSignal);
      recursivePartitionATransposed(q, yH+1, yr, xH+1, xr, a, b, c, stopSignal);
    }
  }


  public static void calculatePartition(int yl, int yr, int xl, int xr,
                              double[][] a, double[][] b, double[][] c) {
    for (int i=yl; i<=yr; i++) {
      for (int j=xl; j<=xr; j++) {
        calculateSingleCell(i, j, a, b, c);
      }
    }
  }


  public static void calculatePartitionBTransposed(int yl, int yr, int xl, int xr,
                              double[][] a, double[][] b, double[][] c) {
    for (int i=yl; i<=yr; i++) {
      for (int j=xl; j<=xr; j++) {
        calculateSingleCellBTransposed(i, j, a, b, c);
      }
    }
  }
  public static void calculatePartitionATransposed(int yl, int yr, int xl, int xr,
                              double[][] a, double[][] b, double[][] c) {
    for (int i=yl; i<=yr; i++) {
      for (int j=xl; j<=xr; j++) {
        calculateSingleCellATransposed(i, j, a, b, c);
      }
    }
  }

}
