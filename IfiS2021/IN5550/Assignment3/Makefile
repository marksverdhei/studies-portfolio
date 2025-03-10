DATA_PATH?=data/norne-nb-in5550-train.conllu
TRAIN_PATH?=data/train.conllu
TEST_PATH?=data/dev.conllu
MODEL_PATH?=test

# Replace this with your own
SAGA_UNAME?=sondrewo

setup: folders download_dataset data_subset

download_dataset:
	scp -r $(SAGA_UNAME)@saga.sigma2.no:/cluster/projects/nn9851k/IN5550/norne-nb-in5550-train.conllu ./data/

folders:
	-mkdir ./data
	-mkdir ./classifiers

data_subset:
	python3 -u data_utils.py $(TRAIN_PATH) $(TEST_PATH)

train:
	python3 -u train.py

saga_train:
	sbatch saga_train.slurm

saga_pred:
	sbatch pred.slurm

pdf:
	pandoc report.md -o report.pdf

tb:
	tensorboard --logdir classifier_logs

clear_logs:
	rm *.out

download_saga_classifiers:
	scp -r $(SAGA_UNAME)@saga.sigma2.no:~/IN5550/Assignment3/classifiers ../saga_classifiers/


SHELL=bash
delete_models:
	@echo "WARNING: DOING THIS WILL DELETE ALL MODELS IN THE MODEL FOLDER"
	@echo "MAKE SURE YOU HAVE MADE A BACKUP FOR THE ONES YOU WANT TO KEEP"
	@read -p "Proceed? [Y/n] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy] ]]; \
	then \
		rm -r models/*; \
	fi
	@echo "\n"
