import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;


public class ParallelSieve {

  int n;
  int sqrtN;
  int primeCount;
  int numberOfThreads;
  byte[] bytes;

  public ParallelSieve(int n) {
    this(n, 0);
  }
  public ParallelSieve(int n, int p) {
      this.n = n;
      numberOfThreads = p != 0 ? p : Runtime.getRuntime().availableProcessors();
      sqrtN = (int) Math.sqrt(n);
      bytes = new byte[n / 16 + 1];   // add 1 because of Integer rounding

  }


  int[] startPrimeFinding() {

    sieveUpToSquared(); // sieve out all non-primes by using primes up to sqrtN
    countPrimesAfterSquared(); // count primes after sqrtN
    //System.out.println("\n-----No. of primes: " + primeCount);
    return collectPrimes(); // add all primes to a list
  }


  void sieveUpToSquared() {
    int[] currentPrime = new int[]{3};
    primeCount++;

    CyclicBarrier cb = new CyclicBarrier(numberOfThreads, () -> {
      if (currentPrime[0] <= sqrtN) {
        currentPrime[0] = findNextPrime(currentPrime[0] + 2);
        primeCount++;
      } else {
        currentPrime[0] = -1;
      }
    });

    int partitionSize = n/numberOfThreads;
    int finalPartitionSize = n - partitionSize*(numberOfThreads-1);
    Thread[] workers = new Thread[numberOfThreads];
    for (int i=0; i<numberOfThreads; i++) {
      int offset = i;
      workers[i] = new Thread(() -> {
        int lo, hi;
        if (offset == 0) {
          lo = 0;
          hi = finalPartitionSize;
        } else {
          lo = finalPartitionSize+((offset-1)*partitionSize);
          hi = finalPartitionSize+(offset*partitionSize);
        }

        while (currentPrime[0] != -1) {
          checkCompositesInParallel(currentPrime[0], lo, hi);
          try {
            cb.await();
          } catch (InterruptedException e) {} catch (BrokenBarrierException e) {}
        }
      });
    }


    for (Thread t : workers) t.start();
    for (Thread t : workers) {
      try {
        t.join();
      } catch (InterruptedException e) {}
    }
  }

  void checkCompositesInParallel(int p, int low, int high) {
    // low and high are indices
    // System.out.println("low:"+low);
    // System.out.println("high:"+high);
    int factor = (low/p)+1;
    factor += (factor+1)%2;
    if (factor < p) factor = p;
    int k = factor * p;
    while (k < high) {
      flip(k);
      k += 2*p;
    }
  }

  void checkCompositesInParallel(List<Integer> q, int low, int high, CountDownLatch stopSignal) {
    // low and high are indices
    // System.out.println("low:"+low);
    // System.out.println("high:"+high);
    for (int p : q) {
      int factor = (low/p)+1;
      if (factor % 2 == 0) factor += 1;
      if (factor < p) factor = p;
      int k = factor * p;
      while (k < high) {
        flip(k);
        k += 2*p;
      }
    }
    stopSignal.countDown();
  }

  void fillAllUncheckedComposites(final List<Integer> q) {
    final CountDownLatch stopSignal = new CountDownLatch(numberOfThreads);
    int lengthOfUnfilled = n;
    int partitionSize = lengthOfUnfilled/numberOfThreads;
    int finalPartitionSize = lengthOfUnfilled - partitionSize*(numberOfThreads-1);
    int offset = finalPartitionSize;

    for (int i=0; i<numberOfThreads-1; i++) {
      int t = i;
      new Thread(() -> {
        int low, high;
        low = offset+(t*partitionSize);
        high = offset+((t+1)*partitionSize);
        checkCompositesInParallel(q, low, high, stopSignal);
      }).start();
    }

    checkCompositesInParallel(q, sqrtN, offset, stopSignal);

    try {
      stopSignal.await();
    } catch (InterruptedException e) {}


  }


  void countPrimesAfterSquared() {
      int startAt;

      if ((sqrtN + 1) % 2 == 0) {
          startAt = sqrtN + 2;
      } else {
          startAt = sqrtN + 1;
      }

      int currentPrime = findNextPrime(startAt);

      while (currentPrime != 0) {
          primeCount++;
          currentPrime = findNextPrime(currentPrime + 2);
      }
  }


  int[] collectPrimes() {

      int[] primes = new int[primeCount];
      primes[0] = 2;
      int currentPrime = 3;

      for (int i = 1; i < primeCount; i++){
          primes[i] = currentPrime;
          currentPrime = findNextPrime(currentPrime + 2);
      }
      return primes;
  }

  void traverseToSqrt(int p) {
    for (int i = p * p; i <= sqrtN; i += p * 2){
        flip(i);
    }
  }

  void traverse(int p) {
    for (int i = p * p; i < n; i += p * 2){
        flip(i);
    }
  }


  void flip(int i) {

      int byteCell = i / 16;  // find respective cell (index) in byte[] bytes
      int bit = (i / 2) % 8;  // find respective bit within byteIndex

      /*
      * 1 << bit shifts a binary 1 bit number of spaces to the left in the byte.
      * 1 << 0 = 0001
      * 1 << 1 = 0010
      * 1 << 2 = 0100
      * 1 << 3 = 1000, etc.
      *
      * | is the OR operand where we basically switch the relevant bit to a 1.
      * |= works similarly to +=
      * */
      bytes[byteCell] |= (1 << bit);
  }


  boolean isPrime(int i) {

      int byteCell = i / 16;
      int bit = (i / 2) % 8;

      /*
      * see bit shift explanation in flip(), same thing here.
      * difference is instead of OR we have an AND operand, which in this case is used to compare
      * your respective bit to a flipped bit, meaning it returns 0 if it hasn't been flipped (is a prime)
      * and > 0 if it has been flipped.
      * */
      return (bytes[byteCell] & (1 << bit)) == 0;
  }


  int findNextPrime(int p) {
      for (int i = p; i < n; i += 2) {
          if (isPrime(i))
              return i;
      }
      return 0;
  }

}
