main_sequqence_gallus=data/original_sequence.fasta
result_sequence_human=data/best_human_sequence.fasta

ogg_test_human=data/OGG1_HUMAN.fasta
ogg_test_yeast=data/OGG1_YEAST.fasta

open_penalty=9
extend_penalty=1

main:
	python3 protein_diff.py $(main_sequqence_gallus) $(result_sequence_human)

main2:
	python3 protein_diff.py $(main_sequqence_gallus) $(result_sequence_human) -o 9 -e 1

ogg_test:
	python3 protein_diff.py $(ogg_test_human) $(ogg_test_yeast)

ogg_test2:
	python3 protein_diff.py $(ogg_test_human) $(ogg_test_yeast) -o 9 -e 1

pdf:
	pandoc Exam1.md -o Exam1.pdf
