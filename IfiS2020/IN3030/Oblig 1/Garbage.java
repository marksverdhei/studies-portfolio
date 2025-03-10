// public class Garbage {
//
//     public static int[] a3parallel(final int[] a, final int k, int t) {
//       final PriorityBlockingQueue<Integer> q = new PriorityBlockingQueue<>(k);
//
//       for (int i=0; i<k; i++) {
//         q.put(a[i]);
//       }
//
//       int searchArraySize = a.length-k;
//       int partitionsize = searchArraySize/k;
//       int finalPartitionsize = partitionsize+(searchArraySize%k);
//
//       final CountDownLatch startSignal = new CountDownLatch(t);
//       final CountDownLatch stopSignal = new CountDownLatch(t);
//
//       for (int i=0; i<t-1; i++) {
//         final int l = k+(partitionsize*i);
//         System.out.println(l);
//         final int r = k+(partitionsize*(i+1));
//         Thread tn = new Thread() {
//           @Override
//           public void run() {
//             startSignal.countDown();
//             try {
//               startSignal.await();
//             } catch (InterruptedException e) {}
//             a3partition(a, l, r, q);
//             stopSignal.countDown();
//           }
//         };
//         tn.start();
//       }
//
//       startSignal.countDown();
//       try {
//         startSignal.await();
//       } catch (InterruptedException e) {}
//       a3partition(a, a.length-finalPartitionsize, a.length, q);
//       stopSignal.countDown();
//       try {
//         stopSignal.await();
//       } catch (InterruptedException e) {}
//       int[] z = new int[k];
//       for (int i=k-1; i>=0; i--) {
//         z[i] = q.remove();
//       }
//       return z;
//     }
//
//     public static void a3partition(final int[] a, int l, int r, final PriorityBlockingQueue<Integer> q) {
//       System.out.println("Thread "+Thread.currentThread().getName()+" started\nL: "+l+"\nR: "+r);
//       for (int i=l; i<r; i++) {
//         if (a[i] > q.peek()) {
//           q.put(a[i]);
//           q.remove();
//         }
//       }
//     }
//
// }
