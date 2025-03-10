import java.util.Arrays;
// import java.util.concurrent.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.BrokenBarrierException;

public class ParallelRadixSort {
	int n;
  int t;
	int seed;
  ExecutorService threadpool;
	CyclicBarrier sync;
	int useBits = 4;

	public static void main(String[] args) {
		if(args.length < 2) {
			System.out.println("This program takes three arguments: <n> <seed> <t>");
      System.out.println("If 2 arguments are supplied, t defaults to number of cores availible to the jvm");
			return;//System.exit(1);
		}

		int n = Integer.parseInt(args[0]);
		int seed = Integer.parseInt(args[1]);

		ParallelRadixSort prs = new ParallelRadixSort(n, seed);

		int unsortedArray[] = Oblig4Precode.generateArray(n, seed);

		int[] sortedArray = prs.sort(unsortedArray);

		Oblig4Precode.saveResults(Oblig4Precode.Algorithm.PARA, seed, sortedArray);

	}

  public ParallelRadixSort(int n, int seed) {
    this(n, seed, Runtime.getRuntime().availableProcessors());
  }

	public ParallelRadixSort(int n, int seed, int t) {
		this.n = n;
    this.t = t;
		this.seed = seed;
		this.sync = new CyclicBarrier(t);
	}

	public int[] sort(int[] unsortedArray) {
    // threadpool = Executors.newFixedThreadPool(t-1);
		threadpool = Executors.newCachedThreadPool();
		int[] a = unsortedArray;

		// STEP A - Find max value
    int max = parallelArrayMax(a);
		// Discover how many bits the max value needs
		int numBits = 1;
		while(max >= (1L << numBits)) numBits++;

		// Calculate how many digits we need
		int numDigits = Math.max(1, numBits/useBits);

		System.out.printf("Max %d giving %d bits and %d digits when useBits %d\n", max, numBits, numDigits, useBits);


		int[] bit = new int[numDigits];

		int rest = numBits % numDigits;

		// Distribute the bits over the digits
		for(int i=0; i < bit.length; i++) {
			bit[i] = numBits/numDigits;

			if(rest-- > 0) bit[i]++;
		}

		int[] b = new int[a.length];

		int shift = 0;

		for(int i=0; i < bit.length; i++) {
			System.out.printf("Round %d with maskLength %d and shift %d\n",i, bit[i], shift);
			radixSort(a, b, bit[i], shift);
			shift += bit[i];

			int[] tmp = a;
			a = b;
			b = tmp;
		}

    threadpool.shutdown();
		return a;
	}

  private int parallelArrayMax(int[] a) {
    int[] results = new int[t];
    int partitionSize = a.length/t;
    int finalPartition = a.length-partitionSize*(t-1);


    for (int i=1; i<t; i++) {
      int lo = finalPartition+(i-1)*partitionSize;
      int hi = finalPartition+i*partitionSize;
      int idx = i;
      threadpool.submit(() -> {
        results[idx] = arrayMax(a, lo, hi);
				try {
					sync.await();
		    } catch (InterruptedException e) {} catch (BrokenBarrierException e) {}
      });
    }

		results[0] = arrayMax(a, 0, finalPartition);

    try {
      sync.await();
    } catch (InterruptedException e) {} catch (BrokenBarrierException e) {}

    return arrayMax(results);
  }

  private int arrayMax(int[] a) {
    int max = 0;
    for(int i=0; i < a.length; i++)
      if(a[i] > max) max = a[i];
    return max;
  }

  private int arrayMax(int[] a, int left, int right) {
    int max = 0;
    for(int i=left; i < right; i++)
      if(a[i] > max) max = a[i];
    return max;
  }

	private void radixSort(int[] a, int[] b, int maskLen, int shift) {
		int[][] allCount = new int[t][];
		// The size / mask of the digit we are interested in this turn
		int mask = (1<< maskLen) - 1;
		// STEP B - Count frequency of each digit
		int[] digitFrequency = countDigitFrequencies(a, mask, shift, allCount);

		// STEP C - Calculate pointers for digits

		int[][] digitPointers = new int[t][digitFrequency.length];
		int[] accumulators = new int[t];

		int partitionSize = digitFrequency.length/t;
		int finalPartition = digitFrequency.length-partitionSize*(t-1);
		int partitionSize2 = a.length/t;
		int finalPartition2 = a.length - (t-1)*partitionSize2;

		for (int k=1; k<t; k++) {
			int idx = k;
			threadpool.submit(() -> {

				int lo = finalPartition+(idx-1)*partitionSize;
				int hi = finalPartition+idx*partitionSize;
				// step c
				for (int i=0; i<lo; i++) {
					accumulators[idx] += digitFrequency[i];
				}

				for (int i=lo; i<hi; i++) {
					digitPointers[0][i] = accumulators[idx];
					accumulators[idx] += digitFrequency[i];
				}

				for (int j=1; j<t; j++) {
					for (int i=lo; i<hi; i++) {
						digitPointers[j][i] = digitPointers[j-1][i] + allCount[j-1][i];
					}
				}

				try {
					sync.await();
				} catch (Exception e) {}

				// step d
				lo = finalPartition2+(idx-1)*partitionSize2;
				hi = finalPartition2+idx*partitionSize2;
				for (int i=lo; i<hi; i++) {
					b[digitPointers[idx][(a[i] >>> shift) & mask]++] = a[i];
				}

				try {
					sync.await();
				} catch (Exception e) {}
			});
		}

		for (int i=0; i<finalPartition; i++) {
			digitPointers[0][i] = accumulators[0];
			accumulators[0] += digitFrequency[i];
		}

		for (int j=1; j<t; j++) {
			for (int i=0; i<finalPartition; i++) {
				digitPointers[j][i] = digitPointers[j-1][i]+allCount[j-1][i];
			}
		}

		try {
			sync.await();
		} catch (Exception e) {}

		// STEP D - Move numbers into correct places
		// System.out.println("length of digitPointers: "+digitPointers.length);

		for(int i = 0; i < finalPartition2; i++) {
			b[digitPointers[0][(a[i] >>> shift) & mask]++] = a[i];
		}

		try {
			sync.await();
		} catch (Exception e) {}
	}

	// private int[] countDigitFrequencies(int[] a, int mask, int shift) {
	// 	// The count of each digit
	// 	int[] digitFrequency = new int[mask+1];
	//
	// 	for(int i=0; i < a.length; i++) {
	// 		digitFrequency[(a[i] >>> shift) & mask]++;
	// 	}
	//
	// 	return digitFrequency;
	// }

	private int[] countDigitFrequencies(int[] a, int mask, int shift, int[][] allCount) {
		// The count of each digit

		// TODO: Find out if this has to be changed
		int numSif = mask+1;

		// int[][] allCount = new int[t][];

		int[] sumCount = new int[numSif];

		int partitionSize = a.length/t;
		int finalPartition = a.length-partitionSize*(t-1);

		int partitionSize2 = numSif/t;
		int finalPartition2 = numSif-partitionSize2*(t-1);


		for (int i=1; i<t; i++) {
			int idx = i;
			threadpool.submit(() -> {
				int lo = finalPartition+(idx-1)*partitionSize;
				int hi = finalPartition+(idx)*partitionSize;

				int[] count = new int[numSif];

				for(int j=lo; j < hi; j++) {
					count[(a[j] >>> shift) & mask]++;
				}

				allCount[idx] = count;
				try {
					sync.await();
				} catch (InterruptedException e) {} catch (BrokenBarrierException e) {}

				lo = finalPartition2+(idx-1)*partitionSize2;
				hi = finalPartition2+idx*partitionSize2;

				for (int j=lo; j<hi; j++) {
					for (int k=0; k<t; k++) {
						sumCount[j] += allCount[k][j];
					}
				}
				try {
					sync.await();
				} catch (InterruptedException e) {} catch (BrokenBarrierException e) {}
			});
		}

		int[] count = new int[numSif];
		for(int j=0; j < finalPartition; j++) {
			count[(a[j] >>> shift) & mask]++;
		}

		allCount[0] = count;
		try {
			sync.await();
		} catch (InterruptedException e) {} catch (BrokenBarrierException e) {}

		for (int j=0; j<finalPartition2; j++) {
			for (int k=0; k<t; k++) {
				sumCount[j] += allCount[k][j];
			}
		}
		try {
			sync.await();
		} catch (InterruptedException e) {} catch (BrokenBarrierException e) {}

		return sumCount;
	}

	// int[] doCount(int[] a, int lo, int hi) {
	//
	// }

}
