import java.util.*;

public class Main {
    static boolean testAlignment = false;
    static boolean seq = false;
    static boolean para = false;
    static int n = 100;
    static int seed = 0;

    public static void main(String[] args) {
        parseArgs(args);

        if (seq || para) {
            testRandomPoints();
        } else if (testAlignment) {
            testAlignedPointsSeq();
            testAlignedPointsPara();
        } else {
            System.out.println("Supply argument --seq, --para or --testAlignment");
        }
    }


      public static void parseArgs(String[] args)  {
        if (args.length == 0) {
            System.out.println("No arguments supplied. Run the program with -h or --help to see the list of arguments");
            // System.exit(1);
        }

        for (String s : args) {
          switch (s) {
            case "-h":
            case "--help":
              System.out.println("Main: program to test the sequential and parallel convex hull algorithm");
              System.out.println("n=[integer] | the input size of the two algorithms. Defaults to 100");
              System.out.println("seed=[integer] | the seed for the randomly generated points");
              System.out.println("--seq | run the sequential solution, draw the results if n < 1000 and write the results to file");
              System.out.println("--para | run parallel solution, draw the results if n < 1000 and write the results to file");
              System.out.println("--testAlignment | produces testcase that checks whether the hull algorithm includes points aligned with the hull");
              System.exit(0);
              break;

            case "--seq":
                seq = true;
                if (para) {
                    System.out.println("Error: arguments --seq and --para are mutually exclusive");
                    System.exit(1);
                }
                break;

            case "--para":
                para = true;
                if (seq) {
                    System.out.println("Error: arguments --seq and --para are mutually exclusive");
                    System.exit(1);
                }
                break;
            case "--testAlignment":
                testAlignment = true;
                break;

            default:
              try {
                String[] arg = s.split("=");
                int value = Integer.parseInt(arg[1]);
                if (arg[0].equals("n")) {
                  n = value;
                } else if (arg[0].equals("seed")) {
                  seed = value;
                } else {
                  throw new Exception();
                }
              } catch (Exception e) {
                System.out.println("Was not able to interpret argument: '"+s+"'");
                System.out.println("Proceeding");
              }
              break;
          }
        }
      }


    public static void testRandomPoints() {
        Oblig5 solver = new Oblig5(n, seed);
        if (seq) {
            solver.initSeq();
        } else {
            solver.initPara();
        }

        Oblig5Precode pr = new Oblig5Precode(solver, solver.coHull);
        System.out.println(Arrays.toString(solver.coHull.data));
        pr.scale = 20;
        if (n <= 1000) pr.drawGraph();
        pr.writeHullPoints();
    }



    public static void testAlignedPointsSeq() {
        Oblig5 ch = new Oblig5(10);

        int[] x = {5, 6, 7, 8, 7, 6, 5, 4, 6, 6};
        int[] y = {5, 5, 5, 6, 7, 7, 7, 6, 8, 4};
        ch.x = x;
        ch.y = y;
        ch.initSeq();
        Oblig5Precode pr = new Oblig5Precode(ch, ch.coHull);
        // make points visible
        pr.scale = 50;

        System.out.println("Sequential solution: "+Arrays.toString(ch.coHull.data));
        pr.drawGraph();
    }


    public static void testAlignedPointsPara() {
        Oblig5 ch = new Oblig5(10);

        int[] x = {5, 6, 7, 8, 7, 6, 5, 4, 6, 6};
        int[] y = {5, 5, 5, 6, 7, 7, 7, 6, 8, 4};

        ch.x = x;
        ch.y = y;
        ch.initPara();
        Oblig5Precode pr = new Oblig5Precode(ch, ch.coHull);
        // make points visible
        pr.scale = 50;

        System.out.println("Parallel solution: "+Arrays.toString(ch.coHull.data));
        pr.drawGraph();
    }
}
