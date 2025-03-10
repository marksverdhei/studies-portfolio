import flask
import pandas as pd
from sklearn.decomposition import PCA

model_paths = {
    "bert": "bert_base_embeddings.csv",
    "roberta": "roberta_base_embeddings.csv"
}

current_model = "bert"

df = pd.read_csv(model_paths["bert"])
words = df["lemma"].unique()

def replace_df(s):
    global df
    global current_model
    df = pd.read_csv(model_paths[s])
    current_model = s


def get_pca_for_word(word):
    lemma_key = df["lemma"] == word
    if not any(lemma_key):
        return None

    df_w = df[lemma_key]
    embeddings = df_w.loc[:, "0":].to_numpy()
    model = PCA(n_components=3)
    pcs = model.fit_transform(embeddings)
    pc1, pc2, pc3 = pcs.T
    return pd.DataFrame({
        "pc1": pc1,
        "pc2": pc2,
        "pc3": pc3,
        "sentence": df_w["text"]
    })


app = flask.Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    global word
    print(flask.request.form)
    word = flask.request.form.get("word", "add")
    model = flask.request.form.get("model", "bert")
    if model != current_model:
        replace_df(model)
    return flask.render_template("./index.html", models=model_paths.keys(), words=words)

@app.route("/embeddings", methods=["GET"])
def inventory(word=words[0]):
    pcdf = get_pca_for_word(word)
    if pcdf is not None:
        return pcdf.to_csv()
    return None


if __name__ == '__main__':
    app.run(debug=True)
