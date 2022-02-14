"""This file is responsible for running the compiler.
    It contains the main method and all the various flags that can be used."""

"""
Multiple files can be compiled at once. Any argument with <filename>.sq will be compiled.

Flags:
1. -p : To save the preprocessed file as preprocessed_<filename>.sq
2. -i : To save the intermediate code as intermediate_<filename>.sq
3. -O1 : To optimize compilation on level 1
4. -O2 : To optimize compilation on level 2
5. -O3 : To optimize compilation on level 3 (default)"""




import sys
import re
from LexicalAnalysis import lexer
from Preprocessing import preprocessor
def compile(filename, optimization_level, save_preprocessed_file, save_intermediate_code):
    print("Compiling", filename, optimization_level)
    try:
        # open .sq code file in read mode
        file_handle = open("./TestSuites/"+filename, "r")
        # read whole file to a string
        file = file_handle.read()
        # close file
        file_handle.close()
        # print(data)
        pre = preprocessor.Preprocessor()
        file = pre.preprocess(filename, file, save=save_preprocessed_file)
    except:
        print("Error reading file")


def main(*argv):
    print('Arguments:', argv[0])
    argv = argv[0]
    optimization_level = 3
    if '-O1' in argv:
        optimization_level = 1
    elif '-O2' in argv:
        optimization_level = 2
    elif '-O3' in argv:
        optimization_level = 3
    print("Optimizatioin level = ", optimization_level)

    save_preprocessed_file = False
    save_intermediate_code = False
    if '-p' in argv:
        save_preprocessed_file = True
        print("Need to save preprocessed file.")
    if '-i' in argv:
        save_intermediate_code = True
        print("Need to save intermediate code file.")

    for arg in argv:
        if arg.endswith('.sq'):
            filename = arg
            print("Name of the file being compiled = ", filename)
            # print("Compiling...")
            compile(filename, optimization_level,
                    save_preprocessed_file, save_intermediate_code)


if __name__ == "__main__":
    #print("printing sys.argv", sys.argv)
    main(sys.argv)
