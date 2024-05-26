from collections import defaultdict

def compute_first(N, index, G, First):
    for i in range(len(G[N])):
        #If the index is the length of the production, then epsilon is added to First
        #because there is no other character to be read
        if index == len(G[N][i]):
            #If epsilon is not in First, then it is added to the set
            if G[N][i][index] not in First[N]:
                First[N].append("e")
        #If the character is epsilon, then epsilon is added to First if it is not already there
        elif "e" == G[N][i][index]:
            if G[N][i][index] not in First[N]:
                First[N].append("e")
        #If the character is a terminal, then the terminal is added to First if it is not already there
        elif G[N][i][index].islower():
            if G[N][i][index] not in First[N]:
                First[N].append(G[N][i][index])
        #If the character is an upper case letter and is different from the non-terminal symbol we are using, then First is computed
        elif G[N][i][index].isupper() and (G[N][i][index] != N):
            compute_first(G[N][i][index], index, G, First)
            for j in First[G[N][i][index]]:
                #If the character is not epsilon, then the character is added to First if it is not already there
                if (j != "e") and (j not in First[N]):
                    First[N].append(j)
            #If epsilon is in First, then the next character is read
            if "e" in First[G[N][i][index]]:
                #If the next character is the length of the production, then epsilon is added to First
                if index + 1 == len(G[N][i]):
                    if G[N][i][index] not in First[N]:
                        First[N].append("e")
                #If the next character is a terminal, then the terminal is added to First
                elif G[N][i][index+1].islower():
                    if G[N][i][index+1] not in First[N]:
                        First[N].append(G[N][i][index+1])
                #If the next character is an upper case letter, then First is computed with the next character
                else:
                    compute_first(G[N][i][index+1], index + 1, G, First)
    return First

def compute_follow(N, G, First, Follow, flag):
    if N == "S":
        if "$" not in Follow[N]:
            Follow[N].append("$")
    for key in G:
        for i in range(len(G[key])):
            for j in range(len(G[key][i])):
                if (G[key][i][j] == N and key != N) or (G[key][i][j] == N and j != len(G[key][i]) - 1):
                    if j == len(G[key][i]) - 1:
                        compute_follow(key, G, First, Follow, flag)
                        for k in Follow[key]:
                            if k not in Follow[N]:
                                Follow[N].append(k)
                    else:
                        if G[key][i][j+1].islower():
                            if G[key][i][j+1] not in Follow[N]:
                                Follow[N].append(G[key][i][j+1])
                        else:
                            for k in First[G[key][i][j+1]]:
                                if k != "e" and k not in Follow[N]:
                                    Follow[N].append(k)
                            if "e" in First[G[key][i][j+1]]:
                                compute_follow(key, G, First, Follow, flag)
    return Follow



#The string with the number of cases to be recieved
cases = int(input())
for _ in range(cases):
    #The string with the number of non-terminals to be recieved
    n = int(input())
    #The dictionary that will store the non-terminals and their respective productions
    G = defaultdict(list)
    j = 0
    while j < n:
        #The user enters the non-terminal and its respective productions separated by spaces
        l = input()
        l = l.split()
        for i in range(1,len(l)):
            #The productions are stored in the list
            G[l[0]].append(l[i])
        j+=1
    #The dictionary that will store the non-terminals and their respective first sets
    First = defaultdict(list)
    for key in G:
        #The function that computes the first set of the non-terminal
        First = compute_first(key, 0, G, First)
        print(f"First({key}) = " + "{", end="")
        for i in range(len(First[key])):
            if i < len(First[key]) - 1:
                print(First[key][i], end=", ")
            else:
                print(First[key][i], end="")
        print("}")

    Follow = defaultdict(list)
    for key in G:
        Follow = compute_follow(key, G, First, Follow, False)
        print(f"Follow({key}) = " + "{", end="")
        for i in range(len(Follow[key])):
            if i < len(Follow[key]) - 1:
                print(Follow[key][i], end=", ")
            else:
                print(Follow[key][i], end="")
        print("}")