  //
  // void traverse(int p) {
  //     int pSquared = p * p;
  //     int partitionSize = (n-pSquared)+1/numberOfThreads;
  //     int iterations = partitionSize/(p*2);
  //     CountDownLatch stopSignal = new CountDownLatch(numberOfThreads);
  //
  //     for (int t=0; t<numberOfThreads; t++) {
  //       int start = pSquared+t*(p*2*iterations);
  //       int stop = Math.min(pSquared+partitionSize*(t+1), n);
  //       Runnable worker = () -> {
  //         for (int i=start; i<stop; i += p*2) {
  //             flip(i);
  //         }
  //         stopSignal.countDown();
  //       };
  //       new Thread(worker).start();
  //     }
  //
  //     try {
  //       stopSignal.await();
  //     } catch (InterruptedException e) {}
  // }
  //
  // void consumePrimes(Lock lock, CountDownLatch stopSignal, Queue<Integer> q) {
  //   boolean empty = false;
  //   int p = 2;
  //   while (!empty) {
  //     lock.lock();
  //     try {
  //       if (!q.isEmpty()) {
  //         p = q.remove();
  //       } else {
  //         empty = true;
  //       }
  //     } finally {
  //       lock.unlock();
  //     }
  //     if (!empty) traverse(p);
  //   }
  //   stopSignal.countDown();
  // }
  //
  // static void testSieves3() {
  //   for (int k : new int[]{10, 100, 1000, 10000, 100000}) {
  //     SequentialSieve sieve1 = new SequentialSieve(k);
  //     SequentialSieve sieve2 = new SequentialSieve(k) {
  //       int sqrtN = squaredN;
  //       @Override
  //       void sieveUpToSquared() {
  //         Deque<Integer> q = new LinkedList<Integer>();
  //         int currentPrime = 3;
  //         primeCount++;
  //
  //         while (currentPrime <= sqrtN) {
  //           q.add(currentPrime);
  //           traverseToSqrt(currentPrime);
  //           // traverse(currentPrime);
  //           currentPrime = findNextPrime(currentPrime + 2);
  //           primeCount++;
  //         }
  //
  //         fillAllUncheckedComposites(q);
  //       }
  //
  //       void traverseToSqrt(int p) {
  //         for (int i = p * p; i <= sqrtN; i += p * 2){
  //             flip(i);
  //         }
  //       }
  //
  //       void fillAllUncheckedComposites(Deque<Integer> q) {
  //         while (!q.isEmpty()) {
  //           traverse(q.removeLast());
  //         }
  //       }
  //     };
  //
  //     int[] z1, z2;
  //     z1 = sieve1.startPrimeFinding();
  //     z2 = sieve2.startPrimeFinding();
  //     System.out.println("Equal at k="+k+"? "+Arrays.equals(z1, z2));
  //   }
  // }


    //
    // public static List<Integer> primeFactorsParallel(int n, int[] primes) {
    //   return primeFactorsParallel(n, 0, primes);
    // }
    //
    // public static List<Integer> primeFactorsParallel(int n, int t, int[] primes) {
    //
    //   if (t == 0) t = Runtime.getRuntime().availableProcessors();
    //   final int numberOfThreads = t;
    //
    //   BlockingQueue<Integer> factors = new LinkedBlockingDeque<Integer>(numberOfThreads*2);
    //   for (int i=0; i<numberOfThreads-1; i++) {
    //     int offset = i;
    //     Runnable task = () -> {
    //       for (int j=offset; j<primes.length; j+=numberOfThreads-1) {
    //         int p = primes[j];
    //         if (n % p == 0) {
    //           try {
    //             factors.put(p);
    //           } catch (InterruptedException e) {}
    //         }
    //       }
    //     };
    //     Thread worker = new Thread(task);
    //     worker.start();
    //   }
    //   int z = n;
    //   List<Integer> allPrimeFactors = new ArrayList<>();
    //   while (z != 1) {
    //     try {
    //       int somePrime = factors.take();
    //       while (z % somePrime == 0) {
    //         z /= somePrime;
    //         allPrimeFactors.add(somePrime);
    //       }
    //     } catch (InterruptedException e) {}
    //   }
    //   // allPrimeFactors.sort(Comparator.naturalOrder());
    //   return allPrimeFactors;
    // }
    //
    //
    //
    // public static List<Integer> primeFactorsParallel2(int n, int[] primes) {
    //   return primeFactorsParallel2(n, 0, primes);
    // }
    //
    // public static List<Integer> primeFactorsParallel2(int n, int t, int[] primes) {
    //
    //   if (t == 0) t = Runtime.getRuntime().availableProcessors();
    //   final int numberOfThreads = t;
    //   ExecutorService executor = Executors.newFixedThreadPool(numberOfThreads-1);
    //   BlockingQueue<Integer> factors = new LinkedBlockingDeque<Integer>(numberOfThreads*2);
    //   for (int i=0; i<numberOfThreads-1; i++) {
    //     int offset = i;
    //     executor.submit(() -> {
    //       for (int j=offset; j<primes.length; j+=numberOfThreads-1) {
    //         int p = primes[j];
    //         if (n % p == 0) {
    //           try {
    //             factors.put(p);
    //           } catch (InterruptedException e) {}
    //         }
    //       }
    //     });
    //   }
    //   int z = n;
    //   List<Integer> allPrimeFactors = new ArrayList<>();
    //   while (z != 1) {
    //     try {
    //       int somePrime = factors.take();
    //       while (z % somePrime == 0) {
    //         z /= somePrime;
    //         allPrimeFactors.add(somePrime);
    //       }
    //     } catch (InterruptedException e) {}
    //   }
    //   // allPrimeFactors.sort(Comparator.naturalOrder());
    //   executor.shutdownNow();
    //   return allPrimeFactors;
    // }
    //
    // public static List<Integer> primeFactorsParallel3(int n, int t, int[] primes) {
    //
    //   if (t == 0) t = Runtime.getRuntime().availableProcessors();
    //   final int numberOfThreads = t;
    //
    //   BlockingQueue<Integer> factors = new LinkedBlockingDeque<Integer>(numberOfThreads*2);
    //   for (int i=0; i<numberOfThreads-1; i++) {
    //     int offset = i;
    //     Runnable task = () -> {
    //       for (int j=offset; j<primes.length; j+=numberOfThreads-1) {
    //         int p = primes[j];
    //         if (n % p == 0) {
    //           try {
    //             factors.put(p);
    //           } catch (InterruptedException e) {}
    //         }
    //       }
    //     };
    //     Thread worker = new Thread(task);
    //     worker.start();
    //   }
    //   int z = n;
    //   List<Integer> allPrimeFactors = new ArrayList<>();
    //   while (z != 1) {
    //     try {
    //       int somePrime = factors.take();
    //       while (z % somePrime == 0) {
    //         z /= somePrime;
    //         allPrimeFactors.add(somePrime);
    //       }
    //     } catch (InterruptedException e) {}
    //   }
    //   // allPrimeFactors.sort(Comparator.naturalOrder());
    //   return allPrimeFactors;
    // }

    // 
    // public static List<Integer> primeFactors(long n, int[] primes) {
    //   List<Integer> factors = new LinkedList<Integer>();
    //   double sqrtN = Math.sqrt(n)+1;
    //   int i = 0;
    //   int p;
    //
    //   do {
    //     p = primes[i];
    //     while (n % p == 0) {
    //       n /= p;
    //       factors.add(p);
    //     }
    //     i++;
    //   } while (n != 1 && p < sqrtN && i<primes.length);
    //
    //   if (i > primes.length) factors.add((int)n);
    //   return factors;
    // }
