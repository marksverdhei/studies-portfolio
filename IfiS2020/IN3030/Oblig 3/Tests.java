import java.util.*;
public class Tests {
  public static void measureSieving() {
    System.out.println("Measuring speedup for sieving");
    ParallelSieve ps = new ParallelSieve(200000000);
    SequentialSieve ss = new SequentialSieve(200000000);

    long a,b,c,d,e,f,g;
    double h,i,j,k,l,m,n,o;
    a = System.nanoTime();
    ps.sieveUpToSquared();
    b = System.nanoTime();
    ps.countPrimesAfterSquared();
    c = System.nanoTime();
    ps.collectPrimes();
    d = System.nanoTime();
    ss.sieveUpToSquared();
    e = System.nanoTime();
    ss.countPrimesAfterSquared();
    f = System.nanoTime();
    ss.collectPrimes();
    g = System.nanoTime();

    h = b-a;
    i = c-b;
    j = d-c;

    k = e-d;
    l = f-e;
    m = g-f;

    n = d-a;
    o = g-d;
    System.out.println("Speedup on sieveUpToSquared: "+(k/h));
    System.out.println("Speedup on countPrimesAfterSquared: "+(l/i));
    System.out.println("Speedup on collectPrimes: "+(m/j));
    System.out.println("Total speedup: "+(o/n));
    System.out.println();
  }

  public static void main(String[] args) {
    ParallelSieve ps = new ParallelSieve(100);
    // ps.startPrimeFinding();
    int[] z2 = ps.startPrimeFinding();
    SequentialSieve ss = new SequentialSieve(100);

    int[] sz = ss.startPrimeFinding();
    if (Arrays.equals(z2, sz)) {
      System.out.println("The arrays are equal!!");
    } else {
      System.out.println("THE ARRAYS ARE NOT EQUAL");
      System.out.println("Correct array:");
      System.out.println(Arrays.toString(sz));
      System.out.println("Incorrect array:");
      System.out.println(Arrays.toString(z2));
    }
    measureSieving();
  }
}
