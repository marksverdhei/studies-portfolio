/*
TODO: Write check to compare with sequential algorithm
TODO: Show speedup in tables and graphical representation

*/
import java.util.*;
public class Matrix {
  public static String toString(double[][] a) {
    StringBuilder s = new StringBuilder(a.length);
    s.append("["+Arrays.toString(a[0])+"\n");
    for (int i=1; i<a.length-1; i++) {
      s.append(" "+Arrays.toString(a[i]));
    }
    s.append(" "+Arrays.toString(a[a.length-1])+"]");
    return s.toString();
  }

  public static void printMatrix(double[][] a) {
    System.out.print("["+Arrays.toString(a[0])+"\n");
    for (int i=1; i<a.length-1; i++) {
      System.out.println(" "+Arrays.toString(a[i]));
    }
    System.out.println(" "+Arrays.toString(a[a.length-1])+"]");
  }

  public static boolean equals(double[][] a, double[][] b) {
    if (a.length != b.length) {
      return false;
    } else {
      for (int i=0; i<a.length; i++) {
        if (!Arrays.equals(a[i], b[i])) return false;
      }
      return true;
    }
  }

  public static double[][] copyOf(double[][] a) {
    double[][] b = new double[a.length][a[0].length];
    for (int i=0; i<a.length; i++) {
      b[i] = Arrays.copyOf(a[i], a[i].length);
    }

    return b;
  }

  public static void transpose(double[][] a) {
    for (int i=0; i<a.length; i++) {
      for (int j=i; j<a.length; j++) {
        double swap = a[i][j];
        a[i][j] = a[j][i];
        a[j][i] = swap;
      }
    }
  }

  public static double[][] matmul(double[][] a, double[][] b) {
    int n = a.length;
    double[][] c = new double[n][n];
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        for (int k=0; k<n; k++) {
          c[i][j] += a[i][k] * b[k][j];
        }
      }
    }

    return c;
  }

  public static double[][] matmulBTransposed(double[][] a, double[][] b) {
    int n = a.length;
    double[][] c = new double[n][n];
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        for (int k=0; k<n; k++) {
          c[i][j] += a[i][k] * b[j][k];
        }
      }
    }
    return c;
  }

  public static double[][] matmulATransposed(double[][] a, double[][] b) {
    int n = a.length;
    double[][] c = new double[n][n];
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        for (int k=0; k<n; k++) {
          c[i][j] += a[k][i] * b[k][j];
        }
      }
    }
    return c;
  }
}
