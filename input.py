import sys
import re
import os

class GraphWrongError(Exception):
    def __init__(self, message="wrong input graph format"):
        self.message = "Error: {0}".format(message)

    def __str__(self):
        return self.message

def input_main(filename, graph):
    try:
        read_file(filename, graph)
        check_graph(graph)
    except GraphWrongError as err:
        print(str(err))
        sys.exit()

def read_file(filename, graph):
    try:
        with open(filename, encoding="utf8") as file:
            if os.stat(filename).st_size == 0:
                raise GraphWrongError("file is empty")
            for line in file:
                if line.rstrip():
                    check_line(line)
                    update_graph(graph, line)

    except EnvironmentError as err:
        print(err)
        sys.exit()

def check_line(line):
    fields = line.split(":")
    regex = re.compile('^[a-zA-Z0-9]+$')

    if len(fields) != 2:
        raise GraphWrongError("file does not contain exactly one character ':'")
    if not regex.findall(fields[0]):
        raise GraphWrongError("file contains an incorrect name of vertex")
    for i in fields[1].split(","):
        i = i.rstrip()
        if i == None or not regex.findall(i):
            raise GraphWrongError("file contains an incorrect description of neighbors")

def update_graph(graph, line):
    fields = line.split(":")
    if fields[0] in graph:
        raise GraphWrongError("file contains two or more lines describing the same vertex")
    vertexes = tuple(fields[1].rstrip().split(","))
    graph[fields[0]] = vertexes

def check_graph(graph):
    for key in graph:
        if graph[key].count(key) > 0:
            raise GraphWrongError("graph should not contain self-loops")
        for vertex in graph[key]:
            if graph[key].count(vertex) != 1:
                raise GraphWrongError("graph should not contain parallel edges")
            if not vertex in graph or graph[vertex].count(key) != 1:
                raise GraphWrongError("graph must be undirected")
