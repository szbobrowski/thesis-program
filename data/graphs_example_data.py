def main():
    vertices, edges = get_example_4()
    return vertices, edges

def get_example_1():
    vertices = ['S', 'A', 'B', 'C', 'D', 'E']
    edges = [['S', 'A', 10], ['S', 'E', 8], ['E', 'D', 1], ['B', 'A', 1], ['A', 'C', 2], ['D', 'A', -4], ['D', 'C', -1], ['C', 'B', -2]]
    return vertices, edges

def get_example_2():
    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    edges = [['A', 'B', 7], ['A', 'C', 12], ['B', 'C', 2], ['B', 'D', 9], ['C', 'E', 10], ['E', 'D', 4], ['D', 'F', 1], ['E', 'F', 5]]
    return vertices, edges

def get_example_3():
    vertices = ['1', '2', '3', '4']
    edges = [['1', '2', 3], ['1', '4', 7], ['2', '1', 8], ['2', '3', 2], ['3', '1', 5], ['3', '4', 1], ['4', '1', 2]]
    return vertices, edges

def get_example_4():
    vertices = ['a', 'b', 'c', 'd']
    edges = [['a', 'b', -3], ['a', 'd', 2], ['b', 'a', 5], ['b', 'c', 3], ['c', 'a', 1], \
         ['d', 'c', 4], ['d', 'a', -1]]
    return vertices, edges