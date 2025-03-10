import java.util.Arrays;
import java.util.Random;
class TestDoubleBubbleSort {
    public static void main(String[] args) {
        int[] arr = new int[]{10, 9, 8, 7, 6, 5, 4, 3, 2, 1};

        DoubleBubbleSort sorter = new DoubleBubbleSort();
        System.out.println("Input array: " + Arrays.toString(arr));
        System.out.println("Sorting...");
        sorter.sort(arr);
        System.out.println("Output array: " + Arrays.toString(arr));

        testLargeArray();

    }

    public static boolean isSorted(int[] arr) {
        for (int i=0; i<arr.length-1; i++) {
            if (arr[i] > arr[i+1]) return false;
        }
        return true;
    }

    public static void testLargeArray() {
        Random r = new Random();
        int n = 100000;
        int[] arr = new int[n];
        for (int i=0; i<n; i++) {
            arr[i] = r.nextInt();
        }

        new DoubleBubbleSort().sort(arr);

        if (isSorted(arr)) {
            System.out.println("LARGE ARRAY IS SORTED");
        } else {
            System.out.println("NOT SORTED");
        }

    }
}
