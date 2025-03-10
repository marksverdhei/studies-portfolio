
default: extract
extract: signal_20_obligatory1_train.tsv
signal_20_obligatory1_train.tsv:
	gzip -d data/signal_20_obligatory1_train.tsv.gz


TRAIN_PATH=data/train_set.tsv
TEST_PATH=data/dev_set.tsv
FRAC=--frac 1

data_subset:
	python3 -u data_utils.py \
		$(TRAIN_PATH) $(TEST_PATH) $(FRAC)


MODEL_FOLDER=mlp_2_hidden_seed1337
SEED=--seed 1337
EPOCHS=--epochs 50
MAX_FEATURES=--max_features 6000
VECTORIZER=--vectorizer binary
CHECKPOINT_ON_EPOCHS=--checkpoint_on_epochs 25
LEARNING_RATE=--learning_rate 0.001
BATCH_SIZE=--batch_size 128
DEV_SET=--dev_set $(TEST_PATH)
HIDDEN_LAYERS=--hidden_layers 2


train:
	python3 -u train.py \
		$(TRAIN_PATH) $(MODEL_FOLDER) $(SEED) \
		$(EPOCHS) $(MAX_FEATURES) $(VECTORIZER) \
		$(CHECKPOINT_ON_EPOCHS) $(LEARNING_RATE) \
		$(BATCH_SIZE) $(DEV_SET) $(HIDDEN_LAYERS) \
		--use_latest_checkpoint
		# --sparse_tensor


test:
	python3 -u eval_on_test.py \
		$(TEST_PATH) $(MODEL_FOLDER) --use_latest_checkpoint
		# --as_markdown

train_test: train test

pdf:
	pandoc report.md -o report.pdf

ignore_models:
	mv models/* ignored_models/

tb:
	tensorboard --logdir models/

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
