import java.util.*;
import java.util.concurrent.*;
public class Sandbox {
  static Random random = new Random(0);
  public static void main(String[] args) {
    testa3();
  }

  public static void testa3() {
    int kjerner = Runtime.getRuntime().availableProcessors();
    System.out.println("Antall kjerner tilgjengelige: "+kjerner);

    final int[] a = new int[]{1,2,3,4,5,6,7,8,9};
    // System.out.println(Arrays.toString(Oblig1.a3parallel(a, 3, 2)));
  }
}
