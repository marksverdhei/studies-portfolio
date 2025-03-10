#include <stdio.h>
#include <stdlib.h>

/*
Modify the sort function such that instead of directly sorting the array arr,
we keep it as is but produce a so-called permutation vector perm.
The purpose is that arr[perm[0]], arr[perm[1]], . . .,
arr[perm[n-1]] is an ordered series.
*/

void swap(int *a, int *b) {
    int t=*a; *a=*b; *b=t;
}

void sort(int arr[], int beg, int end) {
    if (end > beg + 1) {
        int piv = arr[beg], l = beg + 1, r = end;
        while (l < r) {
          if (arr[l] <= piv)
            l++;
          else
            swap(&arr[l], &arr[--r]);
        }
        swap(&arr[--l], &arr[beg]);
        sort(arr, beg, l);
        sort(arr, r, end);
    }
}

void sort_perm(int arr[], int perm[], int beg, int end) {
    // TODO
    if (end > beg + 1) {
        int piv = arr[perm[beg]], l = beg + 1, r = end;
        while (l < r) {
            if (arr[perm[l]] <= piv)
                l++;
            else
                swap(&perm[l], &perm[--r]);
        }
        swap(&perm[--l], &perm[beg]);
        sort_perm(arr, perm, beg, l);
        sort_perm(arr, perm, r, end);
    }
}

int* sorted_permutation(int src[], int len) {
    int* perm_arr = malloc(len*sizeof(int));
    for (int i=0; i<len; i++) perm_arr[i] = i;
    sort_perm(src, perm_arr, 0, len);
    return perm_arr;
}


int* map_permutation_array(int* src, int* perm, int len) {
    int* sorted = malloc(len*sizeof(int));
    for (int i=0; i<len; i++) sorted[i] = src[perm[i]];
    return sorted;
}

void display_array(int* arr, int len) {
    printf("[");
    for (int i=0; i<len-1; i++)
        printf("%d, ", arr[i]);
    printf("%d", arr[len-1]);
    printf("]");
}

int main() {
    int size = 10;
    int* arr = malloc(size*sizeof(int));
    for (int i=0; i<size; i++) arr[i] = rand();
    printf("Unsorted: ");
    display_array(arr, size);
    int* perm = sorted_permutation(arr, size);
    printf("\n\nPerm array: ");
    display_array(perm, size);
    int* sorted = map_permutation_array(arr, perm, size);
    printf("\n\nSorted: ");
    display_array(sorted, size);
    puts("\n");

    free(sorted);
    free(perm);
    free(arr);
    return 0;
}
