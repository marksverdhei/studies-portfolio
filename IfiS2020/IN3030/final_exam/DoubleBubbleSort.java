public class DoubleBubbleSort {

    public void sort(int[] arr) {
        boolean isSorted = false;
        while (!isSorted) {
            isSorted = true;
            for (int i=0; i<arr.length-1; i += 2) {
                int swap;
                if (arr[i] > arr[i+1]) {
                    isSorted = false;
                    if (arr[i+1] > arr[i+2]) {
                        swap = arr[i];
                        arr[i] = arr[i+2];
                        arr[i+2] = swap;
                    } else {
                        swap = arr[i];
                        arr[i] = arr[i+1];
                        if (swap > arr[i+2]) {
                            arr[i+1] = arr[i+2];
                            arr[i+2] = swap;
                        } else {
                            arr[i+1] = swap;
                        }
                    }
                } else if (arr[i+1] > arr[i+2]) {
                    isSorted = false;
                    if (arr[i] < arr[i+2]) {
                        swap = arr[i+1];
                        arr[i+1] = arr[i+2];
                        arr[i+2] = swap;
                    } else {
                        swap = arr[i];
                        arr[i] = arr[i+2];
                        arr[i+2] = arr[i+1];
                        arr[i+1] = swap;
                    }
                }
                if (i+2 > arr.length-3 && i+2 < arr.length-1) i = arr.length-5;
            }
        }
    }
}
