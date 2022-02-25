"""
Version 0.1

"""

import argparse
import os
import sys


def combine(files, outpath):
    """
    Combines two binary files with each other
    :param file0:
    :param file1:
    :return:
    """

    file0 = files[0]
    file1 = files[1]

    combined_file = str(file0[1])+"_"+str(file1[1])+".mp4"

    print("INFO - Making " + str(combined_file))

    # Check so the files aren't the same
    if file0[1] != file1[1]:

        file0 = os.path.join(file0[0], file0[1])
        file1 = os.path.join(file1[0], file1[1])



        with open(os.path.join(outpath, combined_file), "wb") as newfile, open(file0, "rb") as f0, open(file1, "rb") as f1:
            print("INFO - Adding " + str(file0))
            newfile.write(f0.read())
            print("INFO - Adding " + str(file1))
            newfile.write(f1.read())

            newfile.close()
            f0.close()
            f1.close()


def combine_multiple(files, outpath):
    """
    Combines two binary files with each other
    :param file0:
    :param file1:
    :return:
    """

    combined_file = str(files[1][1]).split("_")[0] # Get only the cache key name

    # make the combined file
    with open(os.path.join(outpath, combined_file+".mp4"), "wb") as newfile:
        print("INFO - Making " + str(combined_file))

        # Open the fragment files in order of list
        for files_to_open in files:
            file = os.path.join(files_to_open[0], files_to_open[1])
            print("INFO - Adding " + str(file))
            with open(file, "rb") as f:
                newfile.write(f.read())
                f.close()


def find_all_0_128(files):
    """
    Finds all the files that end with _0-
    :param in_path:
    :return: list of tuples to files [(path,filename)]
    """

    match = []

    for i in files:

        if "_0-" in i[1]:
            match.append(i)

    return match


def find_all_names(filename_0_128, files, outpath):
    """
    Takes one _0- filename and finds the corresponding files to be combined
    :param in_path:
    :return: list of tuples to be combined
    """

    match = [filename_0_128]

    matches = 0

    # Get only the cache key name
    filename_0_128 = filename_0_128[1].split("_0-")[0]

    # For all files in list
    for i in files:

        # Get only data files
        if filename_0_128 in i[1] and "_0-" not in i[1]:

            # Check so file is not empty
            if os.path.getsize(os.path.join(i[0], i[1])) > 1:
                matches = matches + 1
                match.append(i)

    if matches > 1:
        #print("INFO - Found multiple matches for %s" % str(filename_0_128))

        tmp = []

        path_var = match[0][0] # Get path for fragment file
        hash_var = match[1][1].split("_")[0] # Get the cache key name for fragment file

        # Sort the files in correct order
        for item in match:
            a = item[1].split("_")[1]
            b = a.split("-")
            tmp.append((int(b[0]), int(b[1])))

        tmp = sorted(tmp)
        return_list = []

        # Add the sorted files list with path and cache key name
        for item in tmp:
            return_list.append((path_var, hash_var+"_"+str(item[0])+"-"+str(item[1])))

        # Combine them in that order
        combine_multiple(return_list, outpath)

    elif matches == 1:
        print("INFO - Found only one match for %s" % str(filename_0_128))
        combine(match, outpath)




def main():
    """Main function
    :return:"""

    parser = argparse.ArgumentParser(description="""snapunscatter parser: snapchat_combine_parser.py
	-i snapchat\folder
	-o output_folder""")

    # Point to where snapchat dmp is
    parser.add_argument('-i', '--input_path', required=True, action="store", help='Path to files.')

    # Point to where snapchat dmp is
    parser.add_argument('-o', '--output_path', required=True, action="store", help='Output folder for combined files.')

    args = parser.parse_args()

    if parser.error:
        parser.print_help()
        sys.exit(0)

    print("INFO - Using arguments " + str(args))

    path = args.input_path
    output_path = args.output_path

    # Make a list of all files
    list_of = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of.append((root, file))

    # Gather all the header files
    files_128 = find_all_0_128(list_of)

    print("INFO - Combining files")

    # Combine header files and data files
    for files_names_128 in files_128:

        find_all_names(files_names_128, list_of, output_path)






if __name__ == '__main__':
    print("========================================")
    print("Starting....")
    main()
    print()
    print("Done....")
    print("========================================")