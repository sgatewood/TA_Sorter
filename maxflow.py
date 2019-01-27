tas_per_shift = 2

assert(tas_per_shift > 0)

def getList():
    y = open("input.csv")
    lines = y.readlines()
    y.close()
    return lines

# class Node:
#     def __init__(self,name):
#         self.neighbors = []
#         self.name = name

#     def __str__(self):
#         return self.name

#     def __hash__(self):
#         return self.name

def failIf(test,message):
    if(test):
        print(message)
        exit()

def getGraph(lines):
    out = {}
    dogs = {}
    for line in lines:
        lst = line.strip().split(",")
        key = lst.pop(0)
        failIf("_" in key,"Sorry, but TAs cannot have underscores in their names. :(")
        # num_keys = int(lst.pop(0))
        # keys = []
        # for n in range(num_keys):
        #     keys.append(key + "_" + str(n+1))
        val = []
        for dog in lst:
            failIf("_" in dog, "Sorry, but OH names cannot have underscores :(")
            if dog not in dogs:
                dogs[dog] = 1
            elif dogs[dog] < tas_per_shift:
                dogs[dog] += 1
            for i in range(dogs[dog]):
                val.append(dog + "_" + str(i+1))
        for i in range(len(val)):
            out[key + "_" + str(i+1)] = [val[i]]
    return out

def find_aug_path(graph):
    queue = list(map(lambda i: ["SOURCE",i],graph["SOURCE"]))
    while len(queue) > 0:
        # for i in queue:
        #     print(list(map(hash,i)))
        # input()

        queue2 = []
        out = []
        for i in queue:
            # print(len(queue[0]))
            neighbors = graph[i[-1]]
            for j in neighbors:
                path = i
                if j not in path:
                    path = i + [j]
                    queue2.append(path)
                    if j == "SINK":
                        out.append(path)
        if len(out) > 0:
            return out
        queue = queue2

def ford_fulkerson(graph):
    paths = find_aug_path(graph)
    # counter = 0
    while paths != None:
        # counter += 1
        # print(counter)
        # print("PATH:",list(map(hash,path)))
        # display_graph(graph)
        # input()
        # print("\n\n\n\n\n\n\n\n")
        # print(list(map(hash,find_aug_path(graph))))
        # display_graph(graph)
        # input()
        for path in paths:
            for i in range(len(path)-1):

                node = path[i]
                next = path[i+1]

                if next in graph[node]:
                    graph[node].remove(next)
                    graph[next].append(node)
        paths = find_aug_path(graph)

def write_csv(graph):
    lines = ["ta,dog"]
    adopted = set()
    dogs = graph["SINK"]
    dogs.sort(key=lambda i: len(graph[i]))
    for dog in dogs:
        tas = graph[dog]
        ta = tas.pop(0)
        while ta in adopted:
            if(len(tas) == 0):
                ta = None
                break
            ta = tas.pop(0)
        if(ta == None):
            continue
        adopted.add(ta)
        ta = ta.split("_")[0]
        dog = dog.split("_")[0]
        lines.append(ta + "," + dog)
    
    y = open("output.csv","w")
    for line in lines:
        print(line,file=y)
    y.close()


lines = getList()
graph = getGraph(lines)
num_nodes = len(graph)

tas = set()
dogs = set()
for ta in graph:
    tas.add(ta)
    for dog in graph[ta]:
        dogs.add(dog)

graph["SOURCE"] = tas
graph["SINK"] = []
for dog in dogs:
    graph[dog] = ["SINK"]
ford_fulkerson(graph)
write_csv(graph)
