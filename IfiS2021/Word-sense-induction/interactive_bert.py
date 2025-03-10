from transformers import BertTokenizer, BertForMaskedLM
import torch


def main():
    path = "bert-base-uncased"

    n = 15
    tokenizer = BertTokenizer.from_pretrained(path)
    model = BertForMaskedLM.from_pretrained(path)

    with torch.no_grad():
        while True:
            input_str = input(">")
            tokens = tokenizer(input_str, return_tensors="pt")
            mask_pos = torch.where(tokens.input_ids[0] == 103)[0].item()
            # print(mask_pos)
            predictions, = model(**tokens)[0]
            topn = (-predictions[mask_pos]).argsort()[:n]
            # import IPython; IPython.embed()
            print(
                tokenizer.convert_ids_to_tokens(topn)
            )

if __name__ == '__main__':
    main()
