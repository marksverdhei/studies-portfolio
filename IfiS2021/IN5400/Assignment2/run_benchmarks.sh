FILES= "src/configs/*"
for f in $FILES
do
    TMP=./tmp nohup python yourscript.py > $f.log1 2> $f.log2 &
done
