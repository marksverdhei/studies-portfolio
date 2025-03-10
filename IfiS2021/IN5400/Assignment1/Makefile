
config?=configs/default_cluster_config.json

device?=1

outfile?=error1.log

usr?=markuhei
cluster?=ml7
cluster_domain=$(cluster).hpc.uio.no
cluster_addr=$(usr)@$(cluster_domain)

scripts=src/scripts

model?=bin/bin/default_model_adam/model_epoch11.pt

cluster_root_dir=/itf-fi-ml/shared/IN5400/dataforall/mandatory1/VOCdevkit/VOC2012/

root_dir?=data/cluster_data/VOCdevkit/VOC2012/JPEGImages/

gui:
	python3 src/app.py --file_path $(root_dir)

track_output:
	tail -f $(outfile)

train_cluster:
	CUDA_VISIBLE_DEVICES=$(device) nohup python $(scripts)/train.py --config $(config) > out1.log 2> $(outfile) &

train_cluster_direct:
	CUDA_VISIBLE_DEVICES=$(device) python $(scripts)/train.py --config $(config)

train:
	python3 $(scripts)/train.py --config $(config)

eval:
	python3 $(scripts)/eval.py $(model) --val

eval_cluster:
	CUDA_VISIBLE_DEVICES=$(device) nohup python $(scripts)/eval.py $(model) --root_dir $(cluster_root_dir) \
	 > out1.log 2> $(outfile) &

eval_cluster_direct:
	CUDA_VISIBLE_DEVICES=$(device) python $(scripts)/eval.py $(model) --root_dir $(cluster_root_dir)

get_data:
	scp -r $(cluster_addr):/itf-fi-ml/shared/IN5400/dataforall/mandatory1/ ./remote_data

get_models:
	scp -r $(cluster_addr):/itf-fi-ml/home/$(usr)/IN5400/Assignment1/bin bin/

get_predictions:
	scp $(cluster_addr):/itf-fi-ml/home/$(usr)/IN5400/Assignment1/image_preds.csv ./

clean_delivery:
	-rm delivery.zip
	-rm -r delivery/

setup:
	-mkdir bin
	-mkdir configs

pdf:
	pandoc README.md -o report.pdf

delivery: clean_delivery pdf
	mkdir delivery
	cp Makefile delivery/Makefile
	cp -r src delivery/src
	cp report.pdf delivery/
	cp image_preds.csv delivery/
	cp $(model) delivery/best_model.pt
	cp requirements.txt delivery/
	cp -r configs/ delivery/configs
	zip -r delivery.zip delivery/

delete_models:
	rm -rf bin/*
