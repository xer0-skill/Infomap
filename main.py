import sys
import clustering

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Wrong number of arguments, usage: {0} input_file [output_file] \
                (\"output.txt\" by default)".format(sys.argv[0]))
        sys.exit()

    input_filename = sys.argv[1]
    if len(sys.argv) == 3:
        clustering.clustering(input_filename, sys.argv[2], console_out=True)
    else:
        clustering.clustering(input_filename, console_out=True)

if __name__ == "__main__":
    main()
