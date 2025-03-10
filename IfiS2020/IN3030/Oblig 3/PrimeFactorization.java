import java.util.*;
import java.util.concurrent.*;
public class PrimeFactorization {
  static int t = Runtime.getRuntime().availableProcessors();
  static ExecutorService executor = null;


  public static void main(String[] args) {
    int n = 2000000000;
    long m = (long)n * (long)n;
    SequentialSieve ss = new SequentialSieve(n);
    int[] primes = ss.startPrimeFinding();
    long[] numbers = new long[100];
    for (int i=0; i<100; i++) {
      numbers[i] = m-(100-i);
    }

    long[] numbers2 = Arrays.copyOf(numbers, 100);

    System.out.println("m = "+m);
    long a = System.nanoTime();
    LinkedList<Long>[] facs2 = factorizeGreatestPara(primes, numbers2);
    long b = System.nanoTime();
    double c = b-a;
    System.out.println(Arrays.deepToString(facs2));
    System.out.println();
    long x = System.nanoTime();
    LinkedList<Long>[] facs = factorizeGreatestSeq(primes, numbers);
    long y = System.nanoTime();
    double z = y-x;
    System.out.println("Speedup = "+z/c);
    System.out.println("Sequential took "+z/Math.pow(10,9)+" seconds");
    System.out.println("Parallel took "+c/Math.pow(10,9)+" seconds");
    System.out.println(facs);

  }

  static void primeFactorsToPrecode(Oblig3Precode o3, LinkedList<Long>[] factors, long[] numbers) {
    for (int i=0; i<100; i++) {
      for (long f : factors[i]) {
        o3.addFactor(numbers[i], f);
      }
    }
  }

  // public static TreeMap<Long, LinkedList<Long>> factorizeGreatestSeq(int[] primes, long[] numbers) {
  //   TreeMap<Long, LinkedList<Long>> factors = new TreeMap<Long, LinkedList<Long>>();
  //
  //   for (long num : numbers) {
  //     LinkedList<Long> v = new LinkedList<Long>();
  //
  //     int i = 0;
  //     long p;
  //     long c = num;
  //     do {
  //       p = (long)primes[i];
  //       while (c % p == 0) {
  //         c /= p;
  //         v.add(p);
  //       }
  //       i++;
  //     } while (c != 1 && i<primes.length);
  //
  //     if (i >= primes.length) v.add(num);
  //     factors.put(num, v);
  //   }
  //
  //   return factors;
  // }

  public static LinkedList<Long>[] factorizeGreatestSeq(int[] primes, long[] nums) {
    long[] numbers = Arrays.copyOf(nums, 100);
    LinkedList<Long>[] factors = new LinkedList[100];

    for (int j=0; j<100; j++) {
      LinkedList<Long> v = new LinkedList<Long>();

      int i = 0;
      long p;
      long c = numbers[j];
      do {
        p = (long)primes[i];
        while (c % p == 0) {
          c /= p;
          v.add(p);
        }
        i++;
      } while (c != 1 && i<primes.length);

      if (i >= primes.length) v.add(c);
      factors[j] = v;
    }

    return factors;
  }

  public static LinkedList<Long>[] factorizeGreatestPara(int[] primes, long[] numbers) {
    CyclicBarrier sync = new CyclicBarrier(t);
    Thread[] pool = new Thread[t];
    LinkedList<Long>[][] all = new LinkedList[t][100];
    int partitionSize = 100/t;
    int[] los = new int[t];
    int[] his = new int[t];
    for (int i=0; i<t; i++) {
      los[i] = partitionSize*i;
      his[i] = partitionSize*(i+1);
    }
    his[t-1] = 100;

    for (int i=0; i<t; i++) {
      int offset = i;
      pool[i] = new Thread(() -> {
        LinkedList<Long>[] localFactors = new LinkedList[100];
        for (int j=0; j<t; j++) {
          // System.out.println("Epoch: "+j);
          int idx = j+offset;
          int lo = los[idx%los.length];
          int hi = his[idx%his.length];

          for (int k=lo; k<hi; k++) {
            LinkedList<Long> facs = new LinkedList<>();
            long n = numbers[k];
            for (int l=offset; l<primes.length && n!=1; l+=t) {
              long f = primes[l];
              while (n % f == 0) {
                n /= f;
                facs.add(f);
              }
            }
            numbers[k] = n;
            localFactors[k] = facs;
          }
          try {
            sync.await();
          } catch (BrokenBarrierException e) {} catch (InterruptedException e) {}
        }

        all[offset] = localFactors;
      });
      pool[i].start();
    }

    for (Thread t : pool) {
      try {
        t.join();
      } catch (InterruptedException e) {}
    }



    LinkedList<Long>[] ret = all[0];
    for (int i=0; i<100; i++) {
      LinkedList<Long> curFacs = ret[i];
      for (int j=1; j<all.length; j++) {
        LinkedList<Long> otherFacs = all[j][i];
        curFacs.addAll(otherFacs);
      }

      long num = numbers[i];
      if (curFacs.isEmpty() || num != 1) {
        curFacs.add(num);
      }
    }

    return ret;
  }
  //
  // public static ArrayList<LinkedList<Long>> factorizeGreatestPara(int[] primes, long[] numbers) {
  //
  //   CountDownLatch doneSignal = new CountDownLatch(t);
  //   ArrayList<LinkedList<Long>>[] all = new ArrayList[t];
  //
  //   for (int i=0; i<t; i++) {
  //     int offset = i;
  //     new Thread(() -> {
  //       ArrayList<LinkedList<Long>> localFactors = new ArrayList<>(100);
  //       for (long num : numbers) {
  //
  //         LinkedList<Long> f = new LinkedList<>();
  //         int k = offset;
  //         long c = num;
  //         while (c > 1 && k<primes.length) {
  //           long p = primes[k];
  //           while (c % p == 0) {
  //             c /= p;
  //             f.add(p);
  //           }
  //           k += t;
  //         }
  //         localFactors.add(f);
  //       }
  //       all[offset] = localFactors;
  //       doneSignal.countDown();
  //     }).start();
  //   }
  //   try {
  //     doneSignal.await();
  //   } catch (InterruptedException e) {}
  //
  //   ArrayList<LinkedList<Long>> ret = all[0];
  //   for (int i=0; i<100; i++) {
  //     LinkedList<Long> curFacs = ret.get(i);
  //     for (int j=1; j<all.length; j++) {
  //       LinkedList<Long> otherFacs = all[j].get(i);
  //       curFacs.addAll(otherFacs);
  //     }
  //
  //     long num = numbers[i];
  //     if (curFacs.isEmpty()) {
  //       curFacs.add(num);
  //     } else {
  //       for (long fac : curFacs) {
  //         num /= fac;
  //       }
  //       if (num != 1) {
  //         curFacs.add(num);
  //       }
  //     }
  //   }
  //
  //   return ret;
  // }
  //
  // private static void primeFactorsToPrecodeParallel(final long n, int[] primes) {
  //   CountDownLatch stopSignal = new CountDownLatch(t);
  //   ArrayList<Integer>[] lists = new ArrayList[t];
  //   for (int i=0; i<t; i++) {
  //     int offset = i;
  //     executor.submit(() -> {
  //       int idx = offset;
  //       do {
  //         int p = primes[idx];
  //         if (n % p == 0) {
  //           q.put(p);
  //         }
  //         idx += t;
  //       } while (idx<primes.length);
  //     stopSignal.countDown();
  //     });
  //   }
  //   try {
  //     stopSignal.await();
  //   } catch (InterruptedException e) {}
  //
  //   long c = n;
  //   for (int p : q) {
  //     do {
  //       c /= p;
  //       oblig3.addFactor(n, p);
  //     } while (c % p == 0);
  //   }
  //   if (c != 1) oblig3.addFactor(n, c);
  // }
}
