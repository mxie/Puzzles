import java.util.*;
import java.math.BigInteger;


public class PanelProgram {

    public static void main(String[] args) {
        // width and height given by user
        double width = Double.parseDouble(args[0]);
        double height = Double.parseDouble(args[1]);

        // available block sizes
        double size1 = 3;
        double size2 = 4.5;

        BigInteger numCombos = BigInteger.ZERO;
        if (width > 0 && height > 0) {
            // maps multiples of given block size to the number of blocks
            // required to make up that multiple (width)
            Map<Double, Double> possWidths1 = getMultiples(width, size1);
            Map<Double, Double> possWidths2 = getMultiples(width, size2);

            // maps a single row to its potential next rows
            Map<String, Set<String>> rowToPossRows =
                    new HashMap<String, Set<String>>();

            // go through each multiple of size1 (3"x1" blocks) and figure out
            // how many size2 (4.5"x1" blocks) are needed to make up the width
            for (double size1Mult : possWidths1.keySet()) {
                double remainder = width - size1Mult;

                if (possWidths2.containsKey(remainder)) {
                    double countSize1 = possWidths1.get(size1Mult);
                    double countSize2 = possWidths2.get(remainder);

                    // after getting the appropriate # of 3" and 4.5" blocks,
                    // make a list that contains that many of each size,
                    // e.g. if we need 3 3" blocks, make [3,3,3]
                    List<Double> blockCombo = makeCopies(size1, countSize1);
                    blockCombo.addAll(makeCopies(size2, countSize2));

                    // now that we have an array with the appropriate # of
                    // certain blocks, let's generate a set of all permutations
                    // of this array and dump them in a hash as keys
                    Set<List<Double>> perms = getPermutations(blockCombo);
                    for (List<Double> perm : perms) {
                        rowToPossRows.put(perm.toString(), new HashSet<String>());
                    }
                }
            }

            // used to keep track of what rows have we already seen while
            // there are some # of lines remaining and the # of combos then
            Map<String, Map<Double, BigInteger>> memo =
                    new HashMap<String, Map<Double, BigInteger>>();

            // go through each combo of blocks (key) as a possible single row
            // and set the list of all rows that you can stack on top as value;
            // also prep memo hash
            Set<String> singleRows = rowToPossRows.keySet();
            for (String row : singleRows) {
                for (String nextRow : singleRows) {
                    if (!nextRow.equals(row) && isValidStack(row, nextRow, width)) {
                        rowToPossRows.get(row).add(nextRow);
                        memo.put(row, new HashMap<Double, BigInteger>());
                    }
                }
            }

            // now let's start counting!
            numCombos = countCombos(memo, rowToPossRows, singleRows, height);
        }

        System.out.println(numCombos);
    }

    /**
     * For each row of valid rows, recursively count how many rows can be
     * stacked on top of that row
     * @param memo - lookup table for # combos for some row @ # lines remaining
     * @param rowToPossRows - lookup table for list of valid rows for some row
     * @param possRows - list of possible rows we need to deal with
     * @param linesRem - number of lines remaining
     * @return the number of ways you can stack rows
     */
    private static BigInteger countCombos(Map<String, Map<Double, BigInteger>> memo,
                                   Map<String, Set<String>> rowToPossRows,
                                   Set<String> possRows, double linesRem) {
        BigInteger count = BigInteger.ZERO;
        for (String row : possRows) {
            // check if we've seen this row at this # lines remaining first
            if (memo.get(row).containsKey(linesRem)) {
                count = count.add(memo.get(row).get(linesRem));
            } else if (linesRem == 0) {                 // calculate otherwise
                // do nothing.
            } else if (linesRem == 1) {
                count = count.add(BigInteger.ONE);
            } else {
                BigInteger newCount = countCombos(memo, rowToPossRows,
                                           rowToPossRows.get(row),
                                           linesRem-1);
                memo.get(row).put(linesRem, newCount);  // keep track now!
                count = count.add(newCount);
            }
        }
        return count;
    }

    /**
     * Given two rows, check where they might have a crack that lines up
     * @param curr - current row
     * @param next - the row we're checking against
     * @param end - the width given by user input that indicates the end of row
     * @return true if none of the cracks line up
     */
    private static boolean isValidStack(String curr, String next, double end) {
        List<Double> cCracks = getAllCracks(curr);
        List<Double> nCracks = getAllCracks(next);

        for (Double crack : nCracks) {
            if (cCracks.contains(crack) && crack != end) {
                return false;
            }
        }

        return true;
    }

    /**
     * Takes the list of blocks and computes where all the cracks are by summing
     * up each block
     * @param rowString - string representation of the row
     * @return a list of sums that indicate locations of a crack
     */
    private static List<Double> getAllCracks(String rowString) {
        double sum = 0;
        List<Double> cracks = new ArrayList<Double>();
        // get rid of the array brackets and split by comma
        String newString = rowString.substring(1,rowString.length()-1);
        String[] blocks = newString.split(", ");

        for (String blockSize : blocks) {
            sum += Double.parseDouble(blockSize);
            cracks.add(sum);
        }

        return cracks;
    }

    /**
     * Inserts the given number at different positions/indices of the given list
     * @param num - number we want to insert
     * @param list - list we want to insert the number into
     * @return a set containing copies of the given list but with the given
     * number incrementally placed in different spot
     */
    private static Set<List<Double>> putInDiffPosn(double num,
                                                   Set<List<Double>> list) {
        Set<List<Double>> results = new HashSet<List<Double>>();
        if (list.isEmpty()) {
            List<Double> f = new ArrayList<Double>();
            f.add(num);
            results.add(f);
        }
        
        for (List<Double> l : list) {
            for (int i = 0; i <= l.size(); i++) {
                List<Double> f = new ArrayList<Double>(l);
                f.add(i, num);
                results.add(f);
            }
        }

        return results;
    }

    /**
     * Given a list, generate a (unique) set of all permutations of it
     * @param list - list to generate permutations of
     * @return a unique list of all permutations
     */
    private static Set<List<Double>> getPermutations(List<Double> list) {
        if (list.isEmpty()) {
            return new HashSet<List<Double>>();
        } else {
            double first = list.get(0);
            List<Double> rest = list.subList(1,list.size());

            return putInDiffPosn(first, getPermutations(rest));
        }
    }

    /**
     * Make a list containing n copies of a block size
     * @param size - block size to make copies of
     * @param n - number of copies to make
     * @return a list of replicated block sizes
     */
    private static List<Double> makeCopies(double size, double n) {
        List<Double> copies = new ArrayList<Double>();
        for (double i = 0; i < n; i++) {
            copies.add(size);
        }
        return copies;
    }

    /**
     * Calculate the multiples the given block size up to the given width
     * and map them to the # of blocks of that size that make up the multiple
     * @param width - max multiple
     * @param bSize - block size to generate multiples of
     * @return a map of all multiples of a block size to their # of blocks
     */
    private static Map<Double,Double> getMultiples(double width, double bSize) {
        Map<Double, Double> possWidths = new HashMap<Double, Double>();

        double currWidth = 0;
        double i = 0;

        while ( (currWidth < width) && ((currWidth+bSize) <= width) ) {
            currWidth = i * bSize;
            possWidths.put(currWidth, i);
            i++;
        }

        return possWidths;
    }

}