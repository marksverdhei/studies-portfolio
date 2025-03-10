## Questions for Lecture 1
1. What does it mean that DNA is anti-parallel?
That one strand is in the opposite direction of the other
2. Why is it an advantage that DNA is double stranded?
robustness
3. Which 3 parts does a nucleotide consist of?
A nucleoside and a phosphate. The nucleoside consists of a deoxyribose and a base such as adenine.
4. What are complementary bases?
Bases that can form a bond. A is complementary to T, C is complementary to G.
5. What are purines?
Bases with a 2 ring structure, A and G
6. What are pyrimidines?
C, T and U with a single ring structure
7. What is the direction of DNA, and why?
From 5' to 3'
8. What do we mean by ”upstream” and ”downstream”?
Upstream: The dna in the correct direction; 5' -> 3'
Downstream: The dna in the opposite direction; 3' -> 5'
9. What are histones, chromosomes and genome?
A histone is a tyope of protein. When the DNA is tightly wound around it it forms a chromosome
A genome is the total information stored in all the chromosomes
10. What is the translation?
When a gene sequence is turned into a protein. Typically as an mRNA after being transcribed
from a DNA.
11. What is a codon?
3 consecutie nucleotides that resemble an amino acid
12. What are the differences between DNA and RNA?
DNAs are always double stranded with a double helix pattern. They use Thymine
RNAs are typically single stranded. They use Uracil in place of thymine
13. What is a protein?
A composite of amino acids
14. What do each amino acid consist of?
A codon? Carbon, hydrogen, oxygen, nitrogen
15. What are the five different groups of amino acids?
Nonpolar aliphatic, Polar uncharged, aromatic, positive, negative
16. What is a peptide bond?
A bond that forms a protein by connecting amino acids
17. What is the primary structure of a protein?
The sequence of amino acids
18. What is the secondary structure of a protein?
Local structure, alpha helices, beta sheets
19. What is the tertiary structure of a protein?
interactions of a and b due to hydrophobic effect
20. What is the quarternary structure of a protein?
The interaction of more than one protein to form protein complex
Lecture 2
1. What is the DNA alphabet? The RNA alphabet? The protein alphabet?
DNA: ATCG
RNA: AUCG
Protein: ACDEFGHIKLMNPQRSTVWY
2. Why is it interesting to look at sequence alignments?
Good way to estimate similarity
3. Why are dot plots useful when looking at sequences?
It gives a visual impression of similarity
4. How can you identify internal repeats in a dot plot?
Multiple alignments in horizontal and vertical axis
5. Show an example of a dot plot with identical sequences.
diagonal line from top left to bottom right
6. Show an example of a dot plot of an alignment with several gaps.

7. Show a dot plot showing an alignment of inverted segments?
A diagonal line from bottom left to top right
8. What is the edit distance?
The edit distance is a measurement on how many steps necessary to turn one string into another
9. What does a low edit distance indicate?
That the sequence is similar
10. What are the 4 fates for a symbol during evolution?
No chagne
Substitution
Deletion
Insertion
11. What is an ”indel”?
insertion or deletion

## Exercises  

1. Can you identify the 5’ UTR, the 3’ UTR, the coding sequence, and the encoded protein
sequence in the following mRNA sequence?
ACTTGTC**ATG** GTA ACT CCG TCG TAC CAG **TAG**GTCATG  

start codon: ATG at index 7
stop codon: index 28
5': all until index 7
3': all after index 31
The coding sequence is between 5' utr and 3' utr

Val Thr Pro Ser Tyr Gln
V T P S Y G


2. The similarity between two sequences can be visualized with a dot plot. The two most
important parameters that can be adjusted when making dot plots are the window length
and the number of mismatches allowed. In the two dot plots below, the same two
sequences are against each other using the same program. Only parameters are changed
between the left and right image.

a) In the two plots above – which one has the larger window size (assuming the number
of allowed mismatches per window is constant)?

The right one has the larger window size

b) Do you think that these sequences are homologous?

yes

c) Draw, by connecting the diagonal lines in the right plot, the best global alignment.

![alignment.png]()

d) Would a global alignment contain all significant similarities between these two
sequences?

no

3. Retrieve the sequence of the human zinc finger transcription factor gene MAZ with
accession number NM_002383 from GenBank (https://www.ncbi.nlm.nih.gov/) and save
it in FASTA format as a text file. Compare it with itself using Dotlet or dotmatcher. Try
different parameters (window size etc). Describe what you see. What are appropriate
parameters?
Dotlet JS (javascript) can be found here:
https://dotlet.vital-it.ch/
An alternative is the old Dotlet applet (requires Java):
https://myhits.isb-sib.ch/cgi-bin/dotlet
Another alternative is the Emboss Dotmatcher, here:
https://www.ebi.ac.uk/Tools/seqstats/emboss_dotmatcher/
or other Emboss tools at https://www.ebi.ac.uk/Tools/seqstats/

Window size of 1200 lets you see diagonal repitions

4. In each of the two cases below, indicate possible steps of single mutational events
(substitution, insertion and deletion of single symbols) that would transform the first
sequence into the second sequence. How many steps are necessary in each case? What
would the global alignment score be if the score for a match is 1, the score for a mismatch
is 0 and the penalty for a gap is 1?
a)
CAGGTTGCA
TAGGTCA
b)
PVALGLKEK
PVIGLKDK
