from collections import deque
from timeit import default_timer as timer
import heapq

SIZE = 4
BLANK = '0'

outfile = open('output.txt', 'w')
timeComplete = timer()

def read_file(filename):
    infile = open(filename, 'r').read().splitlines()
    states = []
    for line in infile:
        goalfinish = line.split(' ')
        states.append((goalfinish[0], goalfinish[1]))
    return states;


def getChildren(state, blankIndex):
    children = []
    if blankIndex + 1 < SIZE * SIZE and blankIndex % SIZE != (SIZE - 1):
        listForm = list(state)
        listForm[blankIndex], listForm[blankIndex + 1] = listForm[blankIndex + 1], listForm[blankIndex]
        children.append(("".join(listForm), blankIndex + 1, blankIndex, listForm[blankIndex]))
    if blankIndex > -1 and blankIndex % SIZE != 0:
        listForm = list(state)
        listForm[blankIndex], listForm[blankIndex - 1] = listForm[blankIndex - 1], listForm[blankIndex]
        children.append(("".join(listForm), blankIndex - 1, blankIndex, listForm[blankIndex]))
    if blankIndex + SIZE < SIZE * SIZE:
        listForm = list(state)
        listForm[blankIndex], listForm[blankIndex + SIZE] = listForm[blankIndex + SIZE], listForm[blankIndex]
        children.append(("".join(listForm), blankIndex + SIZE, blankIndex, listForm[blankIndex]))
    if blankIndex - SIZE > -1:
        listForm = list(state)
        listForm[blankIndex], listForm[blankIndex - SIZE] = listForm[blankIndex - SIZE], listForm[blankIndex]
        children.append(("".join(listForm), blankIndex - SIZE, blankIndex, listForm[blankIndex]))
    return children


def BFS(start, goal):
    queue = deque([(start, [start])])
    seen = set()
    count = 1
    startTime = timer()
    while len(queue) > 0:
        state, ancestors = queue.popleft()
        if state == goal:
            totalTime = timer() - startTime
            printStats('BFS', count, len(ancestors) - 1, totalTime, (count / totalTime))
            return
        children = getChildren(state)
        for child in children:
            count += 1
            if child not in seen:
                queue.append((child, ancestors + [child]))
                seen.add(child)


def k_DFS(start, goal, maxDepth):
    queue = deque([(start, [start], set(start), 0)])
    count = 1
    startTime = timer()
    while len(queue) > 0:
        state, ancestors, seen, depth = queue.pop()
        if state == goal:
            totalTime = timer() - startTime
            count += nodesCounter
            printStats(name, count, len(ancestors) - 1, totalTime, (count / totalTime))
            return
        if depth + 1 > maxDepth: continue
        children = getChildren(state)
        for child in children:
            count += 1
            if child not in seen:
                seen1 = seen.copy()
                seen1.add(child)
                queue.append((child, ancestors + [child], seen1, depth + 1))
    outfile.write('Not Solved. k_DFS')
    return


def IDDFS(start, goal):
    count = 1
    startTime = timer()
    for i in range(0, 100):
        maxDepth = i
        queue = deque([(start, [start], set(start), 0)])
        while len(queue) > 0:
            state, ancestors, seen, depth = queue.pop()
            if state == goal:
                totalTime = timer() - startTime
                printStats('IDDFS', count, len(ancestors) - 1, totalTime, (count / totalTime))
                return
            if depth + 1 > maxDepth: continue
            children = getChildren(state)
            for child in children:
                count += 1
                if child not in seen:
                    seen1 = seen.copy()
                    seen1.add(child)
                    queue.append((child, ancestors + [child], seen1, depth + 1))

    return


def bi_BFS(start, goal):
    queueTop = deque([(start, [start])])
    queueBottom = deque([(goal, [goal])])
    dictTop = {start: [start]}
    dictBottom = {goal: [goal]}
    count = 1
    start = timer()
    while len(queueTop) > 0 and len(queueBottom) > 0:
        if len(queueTop) > 0:
            stateTop, ancestorsTop = queueTop.popleft()
            if stateTop in dictBottom:
                path = ancestorsTop + dictBottom[stateTop][::-1]
                totalTime = timer() - start
                printStats('bi_BFS', count, len(path) - 2, totalTime, (count / totalTime))
                return
            childrenTop = getChildren(stateTop)
            for child in childrenTop:
                count += 1
                if child not in dictTop:
                    queueTop.append((child, ancestorsTop + [child]))
                    dictTop[child] = ancestorsTop + [child]
        if len(queueBottom) > 0:
            stateBottom, ancestorsBottom = queueBottom.popleft()
            if stateBottom in dictTop:
                path = dictTop[stateBottom] + ancestorsBottom[::-1]
                totalTime = timer() - start
                printStats('bi_BFS', count, len(path) - 2, totalTime, (count / totalTime))
                return
            childrenBottom = getChildren(stateBottom)
            for child in childrenBottom:
                count += 1
                if child not in dictBottom:
                    queueBottom.append((child, ancestorsBottom + [child]))
                    dictBottom[child] = ancestorsBottom + [child]


def best_FS(start, goal):
    fringe = list()
    heapq.heapify(fringe)
    heapq.heappush(fringe, (manhatten_distance(start, goal), start, 0))
    start = timer()
    count = 1
    seen = set()
    while len(fringe) > 0:
        heapq.heapify(fringe)
        distance, state, depth = heapq.heappop(fringe)
        if state in seen: continue
        if state == goal:
            totalTime = timer() - start
            printStats('best_FS', count, depth, totalTime, (count / totalTime))
            return
        children = getChildren(state)
        for child in children:
            if child not in seen:
                count += 1
                heapq.heappush(fringe, (manhatten_distance(child, goal), child, depth + 1))
                seen.add(child)


def AStar(start, goal):
    fringe = list()
    heapq.heappush(fringe, (manhattan_distance(start, goal), start, 0, start.index(BLANK)))
    start = timer()
    count = 1
    seen = set()
    while fringe:
        distance, state, depth, blank = heapq.heappop(fringe)
        if state in seen: continue
        seen.add(state)
        if state == goal:
            totalTime = timer() - start
            printStats('AStar', count, depth, totalTime, (count / totalTime))
            return
        children = getChildren(state, blank)
        for tuples in children:
            child, oldPos, newPos, charChanged = tuples
            count += 1
            if child not in seen:
                heapq.heappush(fringe, (
                (const_hattan(oldPos, newPos, charChanged, distance) + 1) , child, depth + 1, oldPos))

def solve_bucket(start, goal):
    time1 = timer()
    f = manhattan_distance(start,goal)
    openSet= [[] for i in range(82)]
    openSet[f].append((f,0,start,start.index(BLANK)))
    closedSet = set()
    pos = f
    count = 1
    while openSet:
        while not openSet[pos]:
            pos+=1
        distance, depth, state, blank = openSet[pos].pop()
        if state in closedSet:
            continue
        closedSet.add(state)
        if state == goal:
            time2 = timer() - time1
            printStats('Buckets', count, depth, time2, count / time2)
            return
        children = getChildren(state,blank)
        for tuples in children:
            child, oldPos, newPos, charChanged = tuples
            count += 1
            if child in closedSet:
                continue
            g = depth + 1
            h = const_hattan(oldPos,newPos,charChanged,distance) + 1
            openSet[h].append((h,g,child,oldPos))
            if h < pos:
                pos = h

def get_row_col(lis, char):
    index = lis.index(char)
    row = index // SIZE
    col = index % SIZE
    return (row, col)


def manhattan_distance(start, goal):
    pzl = list(start)
    pzlEnd = list(goal)
    distance = 0
    for pos in pzl:
        if pos != BLANK:
            row, col = get_row_col(pzl, pos)
            rowF, colF = get_row_col(pzlEnd, pos)
            distance += abs(row - rowF) + abs(col - colF)
    return distance


def const_hattan(oldPos, newPos, char, distance):
    rowOld = oldPos // SIZE
    colOld = oldPos % SIZE
    rowNew = newPos // SIZE
    colNew = newPos % SIZE
    indexF = look_up_table[char]
    rowF = indexF // SIZE
    colF = indexF % SIZE
    if abs(rowF - rowNew) + abs(colF - colNew) < abs(rowF - rowOld) + abs(colF - colOld):
        return distance - 1
    return distance + 1


def linear_conflict(start,goal):
    conflicts = 0
    both = set(start).intersection(set(goal))
    if BLANK in both:
        both.remove(BLANK)
    for check in both:
        for check2 in both:
            if check == check2: continue
            row,col = get_row_col(start,check)
            row2,col2 = get_row_col(start,check2)
            rowF,colF = get_row_col(goal,check)
            rowF2,colF2 = get_row_col(goal,check2)
            if (row == row2 and row == rowF and row2 == rowF2 and col > col2 and colF < col2):
                conflicts += 1
            if (col == col2 and col == colF and col2 == colF2 and row > row2 and rowF < row2):
                conflicts += 1

    return conflicts



def printStats(sort, totalNodes, steps, time, nodespersec):
    printOut = ''
    printOut += 'Solved.'
    printOut += '%8s' % sort
    printOut += '%8i' % totalNodes + ' Nodes'
    printOut += '%8i' % steps + ' Steps'
    printOut += '%15f' % time + ' secs'
    printOut += '%8i' % int(nodespersec) + ' Nodes/s'
    print(printOut)
    outfile.write(printOut + '\n')


myStates = read_file('states.txt')
outfile.write("Name: Nitin Maddi \n")
for touples in myStates:
    start, end = touples
    print('----> ' + start)
    look_up_table = {}
    letterPos = 1
    for letter in end:
        if letter == BLANK: continue
        look_up_table[letter] = letterPos
        letterPos += 1
    AStar(start,end)
    solve_bucket(start, end)
print("Time Total: " + str(timer() - timeComplete))
