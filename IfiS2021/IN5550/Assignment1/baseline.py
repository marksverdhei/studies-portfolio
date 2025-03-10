from data_utils import load_signal_data
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

DEFAULT_DATA_PATH = "data/signal_20_obligatory1_train.tsv"


class BaselineModel():

    def __init__(self, model=LogisticRegression(max_iter=1300), n_features=5000) -> None:
        print("Initialized new BaselineModel.")

        self.feature_encoder = CountVectorizer(max_features=n_features)
        self.label_encoder = LabelEncoder()
        df = pd.read_csv(DEFAULT_DATA_PATH, sep="\t")

        self.labels, features = df.values.T

        self.feature_encoder.fit(features)
        self.label_encoder.fit(self.labels)

        feature_matrix = self.feature_encoder.transform(features)
        self.label_vector = self.label_encoder.transform(self.labels)

        self.model = model
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            feature_matrix, self.label_vector, test_size=0.2, random_state=42)

    def train(self) -> None:
        print("Training model...")
        self.model.fit(self.X_train, self.y_train)

    def evaluate_classifier(self) -> None:
        print("Evaluating...")
        print(self.model.score(self.X_test, self.y_test))
        y_pred = self.model.predict(self.X_test)
        print(self.label_encoder.classes_)
        print(self.labels)
        print(self.label_encoder.inverse_transform(self.label_vector))

        cr = (classification_report(self.y_test, y_pred,
                                    target_names=self.label_encoder.classes_, output_dict=True))
        df = pd.DataFrame(cr)
        print(df.transpose().to_markdown())


if __name__ == '__main__':
    BaselineModel = BaselineModel(n_features=5000)
    BaselineModel.train()
    BaselineModel.evaluate_classifier()
