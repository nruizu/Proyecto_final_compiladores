from collections import defaultdict

#The function that computes the first set of the non-terminal symbol, where N is the non-terminal symbol we are computing, 
#index is the character of the production to be read, G is the dictionary that stores the non-terminals 
#and their respective productions, and First is the dictionary that stores the non-terminals and their respective first sets
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


#The function that computes the follow set of the non-terminal symbol, where N is the non-terminal symbol we are computing, 
#G is the dictionary that stores the non-terminals and their respective productions, First is the dictionary that stores the non-terminals
#and their respective first sets, and Follow is the dictionary that stores the non-terminals and their respective follow sets
def compute_follow(N, G, First, Follow):
    #If the non-terminal is the starting symbol, then $ is added to Follow if it is not already there
    if N == "S":
        if "$" not in Follow[N]:
            Follow[N].append("$")
    #We iterate all the non_terminal symbols
    for key in G:
        #We iterate all the productions of the non-terminal symbol
        for i in range(len(G[key])):
            #We iterate all the characters of the production
            for j in range(len(G[key][i])):
                #If the character is the non-terminal symbol we are using, and the key is different from the non-terminal symbol we are using
                #or the character is not the last character of the production then we compute the follow set
                if (G[key][i][j] == N and key != N) or (G[key][i][j] == N and j != len(G[key][i]) - 1):
                    #If the character is the last character of the production, then we compute the follow set of the non-terminal symbol we are using
                    if j == len(G[key][i]) - 1:
                        compute_follow(key, G, First, Follow)
                        #We iterate all the characters of the follow set of the non-terminal symbol we are using
                        #and we add them to the follow set of the non-terminal symbol we are using
                        for k in Follow[key]:
                            if k not in Follow[N]:
                                Follow[N].append(k)
                    else:
                        #If the next character is a terminal, then the terminal is added 
                        #to the follow set of the non-terminal symbol we are using if it is not already there
                        if G[key][i][j+1].islower():
                            if G[key][i][j+1] not in Follow[N]:
                                Follow[N].append(G[key][i][j+1])
                        else:
                            #If the next character is a non-terminal symbol, then we add First of the next character to the Follow
                            for k in First[G[key][i][j+1]]:
                                if k != "e" and k not in Follow[N]:
                                    Follow[N].append(k)
                            #If epsilon is in First of the next character, then we add the follow set of the non-terminal symbol we are using
                            if "e" in First[G[key][i][j+1]]:
                                compute_follow(key, G, First, Follow)
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
        #The first set of the non-terminal is printed in the output format given
        print(f"First({key}) = " + "{", end="")
        for i in range(len(First[key])):
            if i < len(First[key]) - 1:
                print(First[key][i], end=", ")
            else:
                print(First[key][i], end="")
        print("}")
    #The dictionary that will store the non-terminals and their respective follow sets
    Follow = defaultdict(list)
    for key in G:
        #The function that computes the follow set of the non-terminal
        Follow = compute_follow(key, G, First, Follow)
        #The follow set of the non-terminal is printed in the output format given
        print(f"Follow({key}) = " + "{", end="")
        for i in range(len(Follow[key])):
            if i < len(Follow[key]) - 1:
                print(Follow[key][i], end=", ")
            else:
                print(Follow[key][i], end="")
        print("}")