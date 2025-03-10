import xml.etree.ElementTree as ET
import pandas as pd
import os


data_path = "data/SemEval-2013-Task-13-test-data/contexts/xml-format/"


def tree_to_dataframe(tree):
    data = []
    for node in tree.getroot():
        context = dict(node.attrib)
        context["text"] = node.text
        data.append(context)
    df = pd.DataFrame(data)
    df.set_index("id", inplace=True)
    return df


def main():
    files = os.listdir(data_path)
    dataframes = [tree_to_dataframe(ET.parse(f"{data_path}/{f}")) for f in files]
    df = pd.concat(dataframes)
    df.to_csv("all.csv")

if __name__ == '__main__':
    main()
