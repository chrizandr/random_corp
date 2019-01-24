"""Select files randomly from corpus."""
import argparse
import glob
import numpy as np
import os

from center_names import get_sc_name
from clustered_names import SC_Tags
from stats import hd_distribution
from stats import language_distribution as ld


def find_sc(name):
    """Find the SC code for center name."""
    for k in SC_Tags:
        if name in SC_Tags[k]:
            return k


def select_from_corpus(language, sc_stats):
    """Select pages randomly from corpus."""
    for i, partition in enumerate(["hd1", "hd2", "hd3", "hd4", "hd5"]):
        pages_needed = int(1.5e5 * ((1.0*hd_distribution[language][i]) / sum(hd_distribution[language])))
        search_dir = os.path.join(corpus_path, partition, language)
        folder_list = [i for i in os.listdir(search_dir) if not os.path.isfile(search_dir + '/' + i)]
        print("Processing {} from partition {}".format(language, partition))

        sc_pages = dict()
        for book in folder_list:
            book_folder_path = os.path.join(corpus_path, partition, language, book)
            sc_book = get_sc_name(book_folder_path)
            sc_tag = find_sc(sc_book)

            pages = list()
            ptiff_path = os.path.join(book_folder_path, 'PTIFF')
            pages += glob.glob1(ptiff_path, "*.TIF")
            pages += glob.glob1(ptiff_path, "*.tif")
            pages += glob.glob1(ptiff_path, "*.tiff")
            pages = [os.path.join(book_folder_path, x) for x in pages]

            if sc_tag in sc_pages:
                sc_pages[sc_tag] += pages
            else:
                sc_pages[sc_tag] = pages

        final_pages = []
        for sc in sc_pages:
            sc_index = int(sc.strip("SC")) - 1
            sc_pages_needed = int(pages_needed * ((1.0*ld[language][partition][sc_index]) / sum(ld[language][partition])))
            page_indices = np.random.permutation(len(sc_pages[sc]))[0:sc_pages_needed]
            page_names = [sc_pages[sc][x] for x in page_indices]
            final_pages.extend(page_names)
            with open(os.path.join("output/", language + "_" + partition + "_" + sc + ".txt")) as f:
                f.write("\n".join(final_pages))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Select 1.5L pages from corpus for a language randomly")
    parser.add_argument('-lan', type=str, required=True,
                        choices=["Hindi", "Telugu", "Tamil", "Kannada", "Sanskrit"],
                        help='Language')
    args = parser.parse_args()

    corpus_path = "/home/chris-andrew/dli-corpus/DLI_LanguageWise"
    files = select_from_corpus(args.lan, args.partition)
    print("Following files have been created for {}, in Partition {}".format(args.lan, args.partition))
