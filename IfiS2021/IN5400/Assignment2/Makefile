usr?=markuhei
cluster?=ml7
cluster_domain=$(cluster).hpc.uio.no
cluster_addr=$(usr)@$(cluster_domain)


FILENAME=report

pdf:
	pandoc $(FILENAME).md \
	--filter pandoc-citeproc \
	--from=markdown+tex_math_single_backslash+tex_math_dollars+raw_tex \
	--to=latex \
	--output=$(FILENAME).pdf

clean_delivery:
	-rm -rf delivery

delivery: pdf clean_delivery
	mkdir delivery
	cp -r src delivery/src
	cp report.pdf delivery/report.pdf
	zip -r delivery.zip delivery/

get_data:
	scp -r $(cluster_addr):/itf-fi-ml/shared/IN5400/dataforall/mandatory2/data ./remote_data

device?=0
config?=src/configs/gru_1layer.json
logfile?=out
train:
	CUDA_VISIBLE_DEVICES=$(device) TMP=./tmp nohup python src/runner.py --config $(config) > $(logfile).log1 2> $(logfile).log2 &
