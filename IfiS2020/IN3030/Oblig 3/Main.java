import java.util.*;

public class Main {

    @FunctionalInterface
    interface Factorizer {
      LinkedList<Long>[] factorize(int[] primes, long[] numbers);
    }

    public static void panic() {
      System.out.println("This program takes 2 arguments!");
      System.out.println(" N: integer greater than 16 | The size of the sieve");
      System.out.println(" k: integer | number of threads. If 0, number of availible threads is chosen");
      System.out.println(" (optional) -skipTiming | skips the timing of median of 7 runs for both sieves and factorization");

      System.exit(1);
    }

    public static void main(String[] args) {
      int n, k;
      try {
        n = Integer.parseInt(args[0]);
        if (n <= 16) panic();
        k = Integer.parseInt(args[1]);
        if (k == 0) k = Runtime.getRuntime().availableProcessors();
        testSieveCorrectness();
        PrimeFactorization.t = k;
        if (!(args.length > 2 && args[2].equals("--skipTiming"))) {
          benchmarkSievesAndFactorization(n, k);
        }

        int[] primes = new SequentialSieve(n).startPrimeFinding();
        long[] numbers = new long[100];
        for (int i=0; i<numbers.length; i++) numbers[i] = ((long)n*(long)n)-(100-i);
        System.out.println(Arrays.toString(numbers));
        LinkedList<Long>[] factors = PrimeFactorization.factorizeGreatestPara(primes, numbers);
        PrimeFactorization.primeFactorsToPrecode(new Oblig3Precode(n), factors, numbers);
        System.out.println("** Factors have been written to file ***");
      } catch (Exception e) {
        e.printStackTrace();
        panic();
      }

    }

    public static void testSieveCorrectness() {
      System.out.println("*** Testing sieve correctness ***\n");
      SequentialSieve ss = new SequentialSieve(100);
      ParallelSieve ps = new ParallelSieve(100);
      int[] results1 = ss.startPrimeFinding();
      int[] results2 = ps.startPrimeFinding();
      System.out.println("Sequential sieve: "+Arrays.toString(results1));
      System.out.println("Parallel sieve: "+Arrays.toString(results2));
      if (Arrays.equals(results1, results2)) {
        System.out.println("These arrays are totally equal, the parallel sieve seems to be correct");
      } else {
        System.out.println("These arrays arent equal, there must be something wrong with the parallel sieve");
      }
    }

    public static void benchmarkSievesAndFactorization(int n, int k) {
      PrimeFactorization.t = k;
      long[] numbers = new long[100];
      long nSquared = (long)n * (long)n;
      for (int i=99; i>=0; i--) numbers[i] = nSquared-(i+1);
      long[] numbers2 = Arrays.copyOf(numbers, numbers.length);
      long sieveSeqTime = getMedianTimeSieveSeq(n);
      System.out.println("Measuing median times of 7 runs in nanoseconds");
      System.out.println("n = "+n);
      System.out.println("sequentialSieve: "+sieveSeqTime);
      long sieveParaTime = getMedianTimeSievePara(n);
      System.out.println("parallelSieve: "+sieveParaTime);

      SequentialSieve ss = new SequentialSieve(n);
      int[] primes = ss.startPrimeFinding();
      Factorizer seqFact = (int[] primes_, long[] numbers_) -> PrimeFactorization.factorizeGreatestSeq(primes_, numbers_);
      long factSeqTime = getMedianTime(seqFact, n, primes, numbers);
      Factorizer paraFact = (int[] primes_, long[] numbers_) -> PrimeFactorization.factorizeGreatestPara(primes_, numbers_);
      long factParaTime = getMedianTime(paraFact, n, primes, numbers);

      System.out.println("sequential factorization: "+factSeqTime);
      System.out.println("parallel factorization: "+factParaTime);
    }
    public static long getMedianTime(Factorizer factorizer, int n, int[] primes, long[] numbers) {
      long[] timings = new long[7];
      long before, after, diff;
      for (int i=0; i<7; i++) {
        before = System.nanoTime();
        factorizer.factorize(primes, numbers);
        after = System.nanoTime();
        diff = after-before;
        timings[i] = diff;
      }
      Arrays.sort(timings);
      return timings[3];
    }

    public static long getMedianTimeSieveSeq(int n) {
      SequentialSieve sieve = new SequentialSieve(n);
      long[] timings = new long[7];
      long before, after, diff;
      for (int i=0; i<7; i++) {
        before = System.nanoTime();
        sieve.startPrimeFinding();
        after = System.nanoTime();
        diff = after-before;
        timings[i] = diff;
      }
      Arrays.sort(timings);
      return timings[3];
    }

    public static long getMedianTimeSievePara(int n) {
      ParallelSieve sieve = new ParallelSieve(n);
      long[] timings = new long[7];
      long before, after, diff;
      for (int i=0; i<7; i++) {
        before = System.nanoTime();
        sieve.startPrimeFinding();
        after = System.nanoTime();
        diff = after-before;
        timings[i] = diff;
      }
      Arrays.sort(timings);
      return timings[3];
    }

}
