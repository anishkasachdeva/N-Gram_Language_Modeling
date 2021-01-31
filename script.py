corpus_file = open("Health_English.txt", "r")  
special_characters = set()

with corpus_file as file:
    for line in file:
        for i in range(len(line)-1):
            if line[i] != " ":
                if (line[i] >= 'a' and line[i] <= 'z') or (line[i] >= 'A' and line[i] <= 'Z') or (line[i] >= '0' and line[i] <= '9'):
                    pass
                else:
                    special_characters.add(line[i])
                    # print(line[i])
                    
                    

for i in special_characters:
    print(i)

# 1. Pseudo add
# 2. ckn(count of four gram word)
# d = discounting factor 0.75
# 
# 4/3
# 
# lambda = 
# 
# a b c d           a b c d/ a b c
# 
# b c d             b c d/ b c
#
# c d               c d / c
#
# d                 d / nothing (Termination Condition)

