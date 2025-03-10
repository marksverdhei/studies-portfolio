DATA_PATH=data/stanford_sentiment_binary.tsv.gz
TRAIN_PATH=data/train_set.tsv
TEST_PATH=data/dev_set.tsv
FRAC=--frac 1
CLF_PATH=bin/classifiers/lstm1
MODEL_PATH=test
# Replace this with your own

VECTORS_PATH=/cluster/shared/nlpl/data/vectors/latest

SAGA_UNAME=markuhei

setup: bin_folders data_subset

bin_folders:
	mkdir ../bin
	mkdir ../bin/classifiers
	mkdir ../bin/embeddings

embeddings_local: download_tagged_vectors download_untagged_vectors

embeddings_saga: copy_tagged_vectors copy_untagged_vectors

download_saga_classifiers:
	scp -r $(SAGA_UNAME)@saga.sigma2.no:~/IN5550/Assignment2/bin/classifiers ../bin/saga_classifiers/

download_tagged_vectors:
	scp $(SAGA_UNAME)@saga.sigma2.no:$(VECTORS_PATH)/200.zip ../bin/embeddings/word2vec_tagged_200.zip

download_untagged_vectors:
	scp $(SAGA_UNAME)@saga.sigma2.no:$(VECTORS_PATH)/12.zip../bin/embeddings/word2vec_tagged_12.zip

download_40:
	scp $(SAGA_UNAME)@saga.sigma2.no:$(VECTORS_PATH)/40.zip ../bin/embeddings/40.zip

copy_tagged_vectors:
	cp $(VECTORS_PATH)/200.zip ../bin/embeddings/word2vec_tagged_200.zip

copy_untagged_vectors:
	cp $(VECTORS_PATH)/12.zip ../bin/embeddings/word2vec_tagged_12.zip

copy_40:
	cp $(VECTORS_PATH)/40.zip ../bin/embeddings/word2vec_tagged_40.zip




data_subset:
	python3 -u data_utils.py ../$(TRAIN_PATH) ../$(TEST_PATH)

train:
	python3 -u train.py --config train_config.json

test: predict eval

eval:
	python3 evaluation.py -p predictions.tsv -g ../data/dev_set.tsv

train_test: train test

pdf:
	pandoc report.md -o report.pdf

tb:
	tensorboard --logdir ../bin/classifiers/$(MODEL_PATH)/model_logs

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
