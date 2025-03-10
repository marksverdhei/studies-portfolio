IN2110_RC=$IN2110_PATH/.in2110rc

echo "Launching IN2110 environment..."

# Setup env
source ~/.bashrc
source $IN2110_PATH/in2110-env/bin/activate

if [ -f "$IN2110_RC" ]; then
    source $IN2110_RC
fi

if [ ! -z $IN2110_DEBUG ]; then
    # Find installed packages
    PIP_LIST=$(pip freeze)
    declare -a PACKAGES=("spacy" "gensim" "scikit-learn" "nltk" "jupyter")

    PACKAGE_STR=""

    for i in "${PACKAGES[@]}"
    do
	PACKAGE=$(echo "$PIP_LIST" | grep "$i==")
	PACKAGE_STR="$PACKAGE_STR ${PACKAGE/==/-}"
    done

    # Print python version and packages
    echo "Python: $(python -c 'import platform; print(platform.python_version())')"
    echo "Packages:$PACKAGE_STR"
fi

