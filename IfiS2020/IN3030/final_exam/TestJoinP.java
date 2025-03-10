import java.util.concurrent.Semaphore;
class TestJoinP {
    public static void main(String[] args) {
        TestJoinP to = new TestJoinP();
        to.assertSemaphoreUpdate();
    }

    public void assertSemaphoreUpdate() {
        JoinP.sem = new Semaphore(0);
        // Run thread sequentially
        new JoinP.ExThread().run();
        int permits = JoinP.sem.availablePermits();
        System.out.print("TEST assertSemaphoreUpdate ");
        if (permits == 1) {
            System.out.println("PASSED");
        } else {
            System.out.println("FAILED");
            System.out.println("Reason: number of semaphore permits should be 1, was" + permits);
        }
    }
}
