# Neural bag of words classifier  

## Report  
The assignment report can be found in [`report.md`](https://github.uio.no/markuhei/IN5550/blob/master/Assignment1/report.md)

## How to run  
* Make sure you meet the required dependencies:  
```
pip3 install -r Requirements.txt
```

### For training

* Initializing the dataset  
call the makefile to decompress the data:

```console
make extract
```

* Create train and dev subset with data_utils.py  

```console
make data_subset
```

* For training: run the script train.py. Run with help to see how it should be used

```console
python3 train.py [train_data_path] [model_folder]
```  

Model folder is not a path, but simply the name of a folder to be found, or created in the models folder

optionally, after ajusting makefile argument, simply run

```console
make train
```  

### Running eval_on_test.py
* For testing on a validation or test set, run eval_on_test

```console
python3 eval_on_test.py [test_set_path] [folder with model and feature encoders]
```

When running the optimal model on the test tsv, run the following:  

```console
python3 eval_on_test.py [test_set_tsv_path] mlp_2_hidden_seed1337
```

it is also possible to set the arguments and run   

```console
make test
```
