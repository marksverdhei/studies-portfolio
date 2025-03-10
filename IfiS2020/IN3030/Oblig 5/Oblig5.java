/**
 * @author: Markus Sverdvik Heiervang <markuhei@ifi.uio.no>
 * date: 25.04.2020
 * A fork of kim's reference implementation for the sequential convex hull
 *
 *
 * @author: Kim Sverre Hilton <kimsh@ifi.uio.no>
 * date: 01.04.2020
 *
 * IN3030/4330 (Spring 2020), Department of Informatics, University of Oslo
 *
 * Sequential solution to convex hull AKA Oblig 5
 *
 * Based on the algorithm described here: https://www.uio.no/studier/emner/matnat/ifi/IN3030/v19/oblig/oblig5-v19-konveks-innhyllning.pdf
 * A video recording of me coding this live is available on the IN3030 (year 2020) course page under "Group Sessions - online resources",
 * you'll find some more in-depth explanations there.
 *
 *
 * NOTE:
 * Feel free to use or take inspiration from this code as long as credit is given where credit is due (we don't want to break faculty rules), BUT
 * for you to use this code in your solution, there is one change you HAVE to make, and another you SHOULD make:
 *
 * 1) This implementation skips points on the same line, i.e. if there are multiple points with distance = 0
 * and that is the farthest distance, only one point will be chosen. Your deliviery is required to include ALL hull points.
 *
 * 2) Notice how similiar findPointsAbove() and findFarthestPoint() are. You could refactor so that you achieve both of
 * their respective functionalities in just one method call and one loop through IntList m, instead of two method calls and two loops.
 * */

import java.util.stream.IntStream;
import java.util.stream.IntStream.Builder;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.RecursiveTask;
import java.util.concurrent.RecursiveAction;
import java.util.concurrent.ForkJoinPool;

public class Oblig5 {

    NPunkter17 np;
    public int[] x;
    public int[] y;
    public int MAX_X = 0;
    public int MAX_Y = 0;
    public int MIN_X = 0;
    public int n;
    public IntList coHull;
    public IntList m;
    public IntList distances;
    public int seed;

    // Fields for parallel implementation

    ForkJoinPool threadpool;

    public Oblig5(int n) {
        this(n, 1995);
    }

    public Oblig5(int n, int seed){
        this.seed = seed;
        this.n = n;
        this.x = new int[n];
        this.y = new int[n];
        this.coHull = new IntList();
        np = new NPunkter17(n, seed);
        np.fyllArrayer(x, y);

        // For parallel solution
        threadpool = ForkJoinPool.commonPool();
    }

    public void initSeq(){

        m = new IntList();

        //  find min and max values for x and y
        for (int i = 0; i < n; i++){
            if (x[i] > x[MAX_X])
                MAX_X = i;
            if (x[i] < x[MIN_X])
                MIN_X = i;
            if (y[i] > y[MAX_Y])
                MAX_Y = i;
        }

        //  add indexes of all points except MAX_X and MIN_X to our IntList
        for (int i = 0; i < n; i++){
            if (i != MAX_X && i != MIN_X)
                m.add(i);
        }

        //  add MAX_X to coHull, because that's our starting point. Remember, we're moving counter-clockwise
        coHull.add(MAX_X);

        HullPartition left = new HullPartition(MAX_X, MIN_X, m);
        left.compute();
        HullPartition right = new HullPartition(MIN_X, MAX_X, m);
        right.compute();

        //  initiate recursion on the left-hand (upper) side of the line
        if (left.farthest > 1)
            recursive(MAX_X, MIN_X, left.farthest, left.points);

        coHull.add(MIN_X);  //  shoutout to Audun. we add MIN_X in-between our recursive calls

        //  initiate recursion on the right-hand (lower) side of the line
        if (right.farthest > 1)
            recursive(MIN_X, MAX_X, right.farthest, right.points);

    }

    public void recursive(int p1, int p2, int p3, IntList m){

        HullPartition left = new HullPartition(p1, p3, m);
        HullPartition right = new HullPartition(p3, p2, m);

        left.compute();
        if (left.farthest > -1) {
            recursive(p1, p3, left.farthest, left.points);
        } else {
            left.zeroDist.forEach(coHull::add);
        }

        coHull.add(p3);

        right.compute();
        if (right.farthest > -1) {
            recursive(p3, p2, right.farthest, right.points);
        } else {
            right.zeroDist.forEach(coHull::add);
        }
    }

    class HullPartition extends RecursiveAction {
      IntList points, m;
      IntStream zeroDist;
      int farthest;
      int p1, p2;

      HullPartition(int p1, int p2, IntList m) {
        points = new IntList();
        farthest = -1;
        zeroDist = null;
        this.p1 = p1;
        this.p2 = p2;
        this.m = m;
      }

      public void compute() {

        IntStream.Builder zeroes = IntStream.builder();

        int distance;
        int farthestDistance = 0;

        int a = y[p1] - y[p2];
        int b = x[p2] - x[p1];
        int c = (y[p2] * x[p1]) - (y[p1] * x[p2]);

        for (int i = 0; i < m.size(); i++) {
            int index = m.get(i);
            distance = (((a * x[index]) + (b * y[index]) + c));

            if (p1 == index || p2 == index)
            continue;

            if (distance > 0) {
                if (distance > farthestDistance) {
                  farthest = index;
                  farthestDistance = distance;
                }
                points.add(index);
            } else if (distance == 0 && farthest == -1) {
                zeroes.add(index);
            }
        }
        zeroDist = zeroes.build();
      }
    }

    public void initPara() {
      m = new IntList();

      int[] minMax = parallelArgMinMax(x);
      MIN_X = minMax[0];
      MAX_X = minMax[1];
      MAX_Y = minMax[2];

      for (int i = 0; i < n; i++){
          if (i != MAX_X && i != MIN_X)
              m.add(i);
      }


      // I have to create a new recursive task for the single reason
      // that we also want MAX_X on the front of the hull.
      // With sufficiently large arrays, we only want to call merge once.
      int[] hull = threadpool.invoke(new RecursiveTask<int[]>() {
          @Override
          protected int[] compute() {
              HullPartition left = new HullPartition(MAX_X, MIN_X, m);
              HullPartition right = new HullPartition(MIN_X, MAX_X, m);
              left.fork();
              right.fork();
              FindHull leftSearch = null;
              FindHull rightSearch = null;

              left.join();
              if (left.farthest > -1) {
                  leftSearch = new FindHull(MAX_X, MIN_X, left.farthest, left.points);
                  leftSearch.fork();
              }

              right.join();
              if (right.farthest > -1) {
                  rightSearch = new FindHull(MIN_X, MAX_X, right.farthest, right.points);
                  rightSearch.fork();
              }

              if (leftSearch != null && rightSearch != null) {
                  return merge(new int[]{MAX_X}, leftSearch.join(), new int[]{MIN_X}, rightSearch.join());
              } else if (leftSearch != null) {
                  return merge(new int[]{MAX_X}, leftSearch.join(), new int[]{MIN_X}, right.zeroDist.toArray());
              } else if (rightSearch != null) {
                  return merge(new int[]{MAX_X}, left.zeroDist.toArray(), new int[]{MIN_X}, rightSearch.join());
              } else {
                  return merge(new int[]{MAX_X}, left.zeroDist.toArray(), new int[]{MIN_X}, right.zeroDist.toArray());
              }
          }
        });

        // We cheat the IntList class by inserting our array along with
        // its length
        coHull.data = hull;
        coHull.len = hull.length;
        // the ForkJoinPool doesnt need to shut down
        // threadpool.shutdown();
        }

    // we want to use this function as little as possible
    // when the arrays get large
    public int[] merge(int[] ... arrays) {
        int totalLength = 0;
        for (int i=0; i<arrays.length; i++) {
            totalLength += arrays[i].length;
        }
        int[] c = new int[totalLength];
        int offset = 0;
        for (int i=0; i<arrays.length; i++) {
            int[] arr = arrays[i];
            System.arraycopy(arr, 0, c, offset, arr.length);
            offset += arr.length;
        }
        return c;
    }

    // class FindHull extends ForkJoinTask<int[]> {
    class FindHull extends RecursiveTask<int[]> {
      int p1, p2, p3;
      IntList m;
      public FindHull(int p1, int p2, int p3, IntList m) {
          this.p1 = p1;
          this.p2 = p2;
          this.p3 = p3;
          this.m = m;
      }

      @Override
      protected int[] compute() {
          // TODO: Parallelize HullPartition
          HullPartition left = new HullPartition(p1, p3, m);
          HullPartition right = new HullPartition(p3, p2, m);
          left.fork();
          right.fork();
          FindHull leftSearch = null;
          FindHull rightSearch = null;

          int[] p3array = new int[]{p3};

          left.join();
          if (left.farthest > -1) {
              leftSearch = new FindHull(p1, p3, left.farthest, left.points);
              leftSearch.fork();
          }

          right.join();
          if (right.farthest > -1) {
              rightSearch = new FindHull(p3, p2, right.farthest, right.points);
              rightSearch.fork();
          }

          if (leftSearch != null && rightSearch != null) {
              return merge(leftSearch.join(), p3array, rightSearch.join());
          } else if (leftSearch != null) {
              return merge(leftSearch.join(), p3array, right.zeroDist.toArray());
          } else if (rightSearch != null) {
              return merge(left.zeroDist.toArray(), p3array, rightSearch.join());
          } else {
              return merge(left.zeroDist.toArray(), p3array, right.zeroDist.toArray());
          }
    }
  }

  public int[] arrayArgMinMax(int[] a) {
      return arrayArgMinMax(a, 0, a.length);
  }

  public int[] arrayArgMinMax(int[] a, int lo, int hi) {
      int argmin = lo;
      int argmax = lo;
      int argYmax = lo;
      for (int i=lo+1; i<hi; i++) {
          if (a[i] < a[argmin]) {
              argmin = i;
          } else if (a[i] > a[argmax]) {
              argmax = i;
          }

          if (a[i] > a[argYmax]) {
              argYmax = i;
          }
      }
      return new int[]{argmin, argmax, argYmax};
  }

  public int[] parallelArgMinMax(int[] a) {
      return parallelArgMinMax(a, Runtime.getRuntime().availableProcessors() * 2);
  }

  public int[] parallelArgMinMax(int[] a, int t) {
      CountDownLatch latch = new CountDownLatch(t);
      int[][] triples = new int[t][3];
      int partitionSize = a.length/t;
      int finalPartition = a.length - partitionSize*(t-1);

      threadpool.submit(() -> {
          triples[0] = arrayArgMinMax(a, 0, finalPartition);
          latch.countDown();
      });

      for (int i=1; i<t; i++) {
          int idx = i;
          threadpool.submit(() -> {
              triples[idx] = arrayArgMinMax(a, finalPartition+(idx-1)*partitionSize, finalPartition+idx*partitionSize);
              latch.countDown();
          });
      }

      try {
          latch.await();
      } catch (InterruptedException e) {}

      int argmin = 0;
      int argmax = 0;
      int argYmax = 0;
      for (int[] triple : triples) {
          int curmin = triple[0];
          int curmax = triple[1];
          int curYmax = triple[2];
          if (a[curmin] < a[argmin]) {
              argmin = curmin;
          }
          if (a[curmax] > a[argmax]) {
              argmax = curmax;
          }
          if (a[curYmax] > a[argYmax]) {
              argYmax = curYmax;
          }

      }
      return new int[]{argmin, argmax, argYmax};
  }
}
