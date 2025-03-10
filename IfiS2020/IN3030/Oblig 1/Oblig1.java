import java.util.*;
import java.util.concurrent.*;
// import java.util.Random;

public class Oblig1 {

  static void swap(int[] a, int i, int j) {
    int c = a[i]; a[i] = a[j]; a[j] = c;
  }

/** This sorts a [v..h] in ascending order with the insertion algorithm */
  static void insertSort (int [] a, int v, int h) {
    int i, t;
    for (int k = v; k < h; k++) {
      // invariant: a [v..k] is now sorted ascending (smallest first)
      t = a[k + 1];
      i = k;
      while (i >= v && a[i] < t) {
          a[i + 1] = a[i];
          i--;
      }
      a[i + 1] = t;
    } // than for k
  } // end insertSort


  // A1
  public static int[] a1(int[] a, int k) {
    int[] b = Arrays.copyOf(a, a.length);
    Arrays.sort(b);
    int size = Math.min(k, b.length);
    int[] z = new int[size];
    for (int i=0; i<size; i++) z[i] = b[b.length-(i+1)];
    return z;
  }

  public static int[] a2sequential(int[] a, int k) {
    return a2sequential(a, k, 0, a.length);
  }
  // A2
  public static int[] a2sequential(int[] a, int k, int l, int r) {
    // create copy of the array
    int[] z = new int[k];
    int len = r-l;
    if (len < k) {
      for (int i=0; i<len; i++) z[i] = a[i+l];
      for (int i=len; i<z.length; i++) z[i] = Integer.MIN_VALUE;
      insertSort(z, 0, z.length-1);
      return z;
    }

    for (int i=0; i<k; i++) z[i] = a[i+l];
    // Perform insertion sort on the sub-array

    insertSort(z, 0, z.length-1);

    for (int i=l+k; i<r; i++) {
      if (a[i] > z[k-1]) {
        z[k-1] = a[i];
        int j = k-1;
        while (j != 0 && z[j]>(z[j-1])) {
          swap(z, j, j-1);
          j--;
        }
      }
    }

    return z;
  }

  public static int[] a2parallel(int[] a, int k, int t) {

    int[] z = new int[k];
    // Idea: partition the array into k subarrays
    PriorityBlockingQueue<Integer> q = new PriorityBlockingQueue<>(k,
      new Comparator<Integer>(){
        @Override
        public int compare(Integer i1, Integer i2) {
          return i2.compareTo(i1);
        }
    });

    CountDownLatch doneSignal = new CountDownLatch(t);

    int partitionSize = a.length/t;
    // System.out.println("Partition size: "+partitionSize);
    int finalPartitionsize = partitionSize+(a.length%t);

    for (int i=0; i<t-1; i++) {
      int l = i*partitionSize;
      int r = l+partitionSize;

      Runnable task = () -> {
        a2partition(a, k, q, l, r);
        doneSignal.countDown();
      };
      new Thread(task).start();
    }
    a2partition(a, k, q, a.length-finalPartitionsize, a.length);
    doneSignal.countDown();
    try {
      doneSignal.await();
    } catch (InterruptedException e) {
      ;
    }

    // collect items and return

    for (int i=0; i<k; i++) {
      z[i] = q.remove();
    }

    return z;
  }

  public static void a2partition(int[] a, int k, PriorityBlockingQueue<Integer> q, int l, int r) {
    int[] z = a2sequential(a, k, l, r);

    for (int i=0; i<z.length; i++) {
      q.put(z[i]);
    }
  }

  public static void main(String[] args) {
    System.out.println("Run test Oblig1 to see benchmarks");
  }
}
