import java.util.concurrent.*;
class JoinP {

    static Semaphore sem;

    public static void main(String[] args) {
        int numberofthreads = 10;
        sem = new Semaphore(-numberofthreads+1);
        Thread[] t = new Thread[numberofthreads];

        for (int j = 0; j < numberofthreads; j++) {
            (t[j] = new Thread( new ExThread() )).start();
        }

        try {
            System.out.println("Acquiring semaphore permit");
            sem.acquire();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    static class ExThread implements Runnable {
        public void run() {
            try {
                TimeUnit.SECONDS.sleep(10);
            } catch (Exception e) {
                return;
            } finally {
                System.out.println("Releasing semaphore permit");
                sem.release();
            }
        }
    }
}
