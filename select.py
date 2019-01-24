"""Select files randomly from corpus."""
import argparse
import os

def select_from_corpus(Language, partition):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool for analysing DLI corpus")
    parser.add_argument('-lan', type=str, required=True,
                        choices=["Hindi", "Telugu", "Tamil", "Kannada", "Sanskrit"],
                        help='Language')
    parser.add_argument('--partition', type=str, required=True,
                        choices=['hd1', 'hd2', 'hd3', 'hd4', 'hd5'],
                        help='Partition name')
    args = parser.parse_args()

    corpus_path = "/home/chris-andrew/dli-corpus/DLI_LanguageWise"
    files = select_from_corpus(args.lan, args.partition)
    print("Following files have been created for {}, in Partition {}".format(args.lan, args.partition))
