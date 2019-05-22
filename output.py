import sys

def output_main(clusters_partition, codelength, number_clusters, filename="output.txt"):
    try:
        with open(filename, "w", encoding="utf8") as file:
                file.write("{0} clusters with code length: {1}\n".format(number_clusters, codelength))
                file.write("Vertex    Cluster\n")
                for key in clusters_partition:
                    file.write("{0}: {1}\n".format(key, clusters_partition[key]))
    except EnvironmentError as err:
        print(err)
        sys.exit()

def output_console(graph, clusters_partition, number_clusters, codelength):
    print("Graph:")
    for key in graph:
        print("{0}: {1}".format(key, graph[key]))
    print("{0} clusters with codelength: {1}".format(number_clusters, codelength))
    print("Vertex Cluster")
    for key in sorted(clusters_partition, key=clusters_partition.get, reverse=False):
        print("{0}: {1}".format(key, clusters_partition[key]))

def check_output(clusters_partition, codelength, number_clusters, filename="output.txt"):
    try:
        with open(filename, encoding="utf8") as file:
            result = True

            first_line = file.readline()
            first_word = first_line.split(" ")[0]
            if first_word != str(number_clusters):
                result = False

            line_split = first_line.split(" ")
            last_word = line_split[len(line_split) - 1].rstrip()
            if last_word != str(codelength):
                result = False

            if file.readline() != "Vertex    Cluster\n":
                result = False

            for key in clusters_partition:
                line = file.readline()
                fields = line.split(":")
                if fields[0] != str(key) or fields[1].strip() != str(clusters_partition[key]):
                    result = False

            if not result:
                print("function output_main(..) works incorrectly")
                os.remove(filename)
                sys.exit()
    except FileNotFoundError as err:
        print("test_output:", err)
        sys.exit()
