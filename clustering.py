import input
import output
import two_level_infomap

def clustering(input_filename, output_filename=None, console_out=None, file_output=True):
    graph = {}
    input.input_main(input_filename, graph)

    infomap = two_level_infomap.Infomap(graph)
    infomap.core_algorithm()

    clusters_partition = infomap.get_clusters_partition()
    number_clusters = infomap.get_number_clusters()
    codelength = infomap.get_codelength()

    if console_out:
        output.output_console(graph, clusters_partition, number_clusters, codelength)

    if file_output:
        if output_filename:
            output.output_main(clusters_partition, codelength, number_clusters, output_filename)
            output.check_output(clusters_partition, codelength, number_clusters, output_filename)
        else:
            output.output_main(clusters_partition, codelength, number_clusters)
            output.check_output(clusters_partition, codelength, number_clusters)

    return clusters_partition
