public class TestMatmul {
  static final int seed = 42;
  static double[][] a, a0, aT, b, b0, bT, c, c1, c2, c3, d, d1, d2;
  public static void main(String[] args) {
    for (int i=2; i<50; i++) {
      testTranspose(i);
      testMatmul(i);
      testMatmul2(i);
      testParallelMatmul(i);
      testParallelMatmulMutation(i);
    }
  }


  public static void testTranspose(int n) {
    a = Oblig2Precode.generateMatrixA(seed, n);
    c = Matrix.copyOf(a);
    assert Matrix.equals(a, c) : "Error in testTranspose #1";
    Matrix.transpose(c);
    assert !Matrix.equals(a, c) : "Error in testTranspose #1.2";
    Matrix.transpose(a);
    assert Matrix.equals(a, c) : "Error in testTranspose #2";
    Matrix.transpose(c);
    Matrix.transpose(a);
    assert Matrix.equals(a, c) : "Error in testTranspose #3";
  }

  public static void testMatmul(int n) {
    a = Oblig2Precode.generateMatrixA(seed, n);
    a0 = Matrix.copyOf(a);
    b = Oblig2Precode.generateMatrixB(seed, n);
    b0 = Matrix.copyOf(b);
    assert Matrix.equals(a, a0) : "Error in testMatmul #1";
    assert Matrix.equals(b, b0) : "Error in testMatmul #2";
    c1 = Matrix.matmul(a, b);
    assert Matrix.equals(a, a0) : "Error in testMatmul #3";
    assert Matrix.equals(b, b0) : "Error in testMatmul #4";
    c2 = ParallelMatrix.matmul(a, b);
    assert Matrix.equals(a, a0) : "Error in testMatmul #5";
    assert Matrix.equals(b, b0) : "Error in testMatmul #6";
    assert Matrix.equals(c1, c2) : "Error in testMatmul 7";
  }

  public static void testMatmul2(int n) {
    a = Oblig2Precode.generateMatrixA(seed, n);
    aT = Matrix.copyOf(a);
    Matrix.transpose(aT);
    assert !Matrix.equals(a, aT) : "Transpose should not be equal #1";
    b = Oblig2Precode.generateMatrixB(seed, n);
    bT = Matrix.copyOf(b);
    Matrix.transpose(bT);
    assert !Matrix.equals(b, bT) : "Transpose should not be equal #2";

    c1 = Matrix.matmul(a, b);
    c2 = Matrix.matmulBTransposed(a, bT);
    c3 = Matrix.matmulATransposed(aT, b);

    assert Matrix.equals(c1, c2) : "Error in testMatmul2 #1";
    assert Matrix.equals(c1, c3) : "Error in testMatmul2 #2";
  }

  public static void testParallelMatmul(int n) {
    a = Oblig2Precode.generateMatrixA(seed, n);
    aT = Matrix.copyOf(a);
    Matrix.transpose(aT);
    b = Oblig2Precode.generateMatrixB(seed, n);
    bT = Matrix.copyOf(b);
    Matrix.transpose(bT);

    c = Matrix.matmul(a, b);
    c1 = ParallelMatrix.matmul(a, b);
    c2 = ParallelMatrix.matmulBTransposed(a, bT);
    c3 = ParallelMatrix.matmulATransposed(aT, b);

    assert Matrix.equals(c, c1) : "Error in testParallelMatmul #1";
    assert Matrix.equals(c, c2) : "Error in testParallelMatmul #2";
    assert Matrix.equals(c, c3) : "Error in testParallelMatmul #3";
  }

  public static void testParallelMatmulMutation(int n) {
    a = Oblig2Precode.generateMatrixA(seed, n);
    a0 = Matrix.copyOf(a);
    b = Oblig2Precode.generateMatrixB(seed, n);
    b0 = Matrix.copyOf(b);
    ParallelMatrix.matmul(a, b);
    ParallelMatrix.matmulATransposed(a, b);
    ParallelMatrix.matmulBTransposed(a, b);
    assert Matrix.equals(a, a0) : "Error in testParallelMatmulMutation #1";
    assert Matrix.equals(b, b0) : "Error in testParallelMatmulMutation #2";
  }

}
