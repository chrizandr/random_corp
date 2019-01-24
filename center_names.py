"""Cluster center names together."""
from bs4 import BeautifulSoup
import distance
import json
import numpy as np
import os
import pdb
import sklearn.cluster


def get_center_names():
    """Get all center names from all books."""
    center_names = list()
    book_count = 0
    for partition in partitions:
        for language in languages:
            search_dir = os.path.join(main_path, partition, language)
            folder_list = [i for i in os.listdir(search_dir) if not os.path.isfile(search_dir + '/' + i)]
            print("Processing {} from partition {}".format(language, partition))
            for book in folder_list:
                book_count += 1
                # Read the book's META.XML file and build a tree using BeautifulSoup
                book_folder_path = os.path.join(main_path, partition, language, book)
                xml_path = os.path.join(book_folder_path, 'META.XML')
                xml_content = open(xml_path).read()
                xml_tree = BeautifulSoup(xml_content)

                # Try checking if the meta.xml file has scanningcentre tag
                try:
                    sc_book = xml_tree.find('scanningcentre').text
                except AttributeError:
                    try:
                        sc_book = xml_tree.find('scanningcentrename').text
                    except AttributeError:
                        try:
                            sc_book = xml_tree.find('SCANNING_CENTER').text
                        except AttributeError:
                            sc_book = "Empty"
                if len(sc_book) == 0:
                    sc_book = "Empty"
                center_names.append(sc_book)
    total_names = len(center_names)
    center_names = set(center_names)
    print("Got a total of {} books".format(book_count))
    print("{} book had center names with {} unique center names in total".format(total_names, len(center_names)))
    print("Saving unique names to {}".format(name_file))
    with open(name_file, "w") as f:
        f.write("\n".join(list(center_names)))

    return list(center_names)


def cluster_names(center_names):
    """Cluster similar names together."""
    names = np.asarray(center_names)

    print("Clustering names.")
    lev_similarity = -1*np.array([[distance.levenshtein(w1, w2) for w1 in names] for w2 in names])
    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)

    print("Writing clusters to file.")
    with open(output_file, "w") as f:
        for cluster_id in np.unique(affprop.labels_):
            cluster = np.unique(names[np.nonzero(affprop.labels_ == cluster_id)])
            cluster_dict = {"cluster": list(cluster)}
            f.write(json.dumps(cluster_dict, indent=2))


if __name__ == "__main__":
    main_path = "/home/chris-andrew/dli-corpus/DLI_LanguageWise"
    languages = ["Hindi", "Telugu", "Kannada", "Tamil", "Sanskrit"]
    partitions = ["hd1", "hd2", "hd3", "hd4", "hd5"]

    name_file = "center_names.txt"
    output_file = "clusters.py"

    names = get_center_names()
    cluster_names(names)
