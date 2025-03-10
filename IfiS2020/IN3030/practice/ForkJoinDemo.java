import java.util.*;
import java.util.concurrent.*;

public class ForkJoinDemo {
  public static void main(String[] args) {
    ForkJoinPool pool = ForkJoinPool.commonPool();
    System.out.println(pool.invoke(new Fibbonacci(40)));
    System.out.println(fib(40));
    pool.shutdown();
  }

  public static Integer fib(int n) {
    if (n <= 1) {
      return n;
    } else {
      return fib(n-1) + fib(n-2);
    }
  }
}

class Fibbonacci extends RecursiveTask<Integer> {
  Integer n;

  public Fibbonacci(int n) {
    this.n = n;
  }

  @Override
  protected Integer compute() {
    if (n <= 1) {
      return n;
    } else {
      Fibbonacci f1 = new Fibbonacci(n-1);
      Fibbonacci f2 = new Fibbonacci(n-2);
      f1.fork();
      f2.fork();
      return f1.join() + f2.join();
    }
  }
}
