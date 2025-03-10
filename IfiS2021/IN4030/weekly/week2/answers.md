1. What does one mean by ”similarity”?  
An objective closeness in information, or pattern
2. What does one mean by ”homology”?
Equality or similiarty.
3. What does a high degree of similarity imply?  
relatedness
4. What is the ”safe zone” in protein sequence alignment? Twilight zone? Midnight
zone?  
Areas regarding uncertainty in whether to conclude in homology of two protiein sequences.
5. What is a scoring matrix?  
A parameter for scoring an alignment. A different scoring matrix might yield a different optimal alignment   
6. What is a substitution score matrix?  
A scoring matrix containing likelihoods of mutations from one amino acid to another one (or nucleotide).
7. What is a gap penalty, and gap function?  
a gap penalty is what you subtract from an alignment score with
gaps in the alignment  
8. What are the different penalty functions?  
Constant, linear, affine, logarithmic, concave  
9. What is a concave gap penalty?
g_x = penalty of gap of length x
g_x <= g_{x-y} + g_y for all y where 0 < y < x  
10. Why are concave gap penalties biologically meaningful?  
Concave gap penalties are biologically meaningful because it gives less (or
equal) penalty for one long gap than for two or more gaps of the same total
length  
11. What is the definition of global alignment?  
Global alignment means alligning entire sequences, usually based on the sequences being similar length
and the hypothesis of them being related  
12. What is the definition of a local alignment?  
Aligning parts of the sequences
13. What is the difference between pairwise and multiple alignment?  
Pairwise alignment means alignment between two sequences. Multiple is the same but with more than two sequences  
14. Can 2 blank symbols (gaps) be aligned?  
no  
15. What is the definition of optimal global alignment?  
The alignmnet that maximizes the scoring function  
16. What is a brute force algorithm?  
An algorithm that tries every possible solution until it succeeds  
17. What is dynamic programming?  
A method in programming that caches/memoizes computations to shorten the execution time  
and overall computational expense  
