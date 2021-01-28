def count_occurences(sentence):
    num_of_words = len(sentence.split())

    if num_of_words == 4:
        if sentence in fourgram_frequency:
            return fourgram_frequency[sentence]
        else:
            return 0
    elif num_of_words == 3:
        if sentence in trigram_frequency:
            return trigram_frequency[sentence]
        else:
            return 0
    elif num_of_words == 2:
        if sentence in bigram_frequency:
            return bigram_frequency[sentence]
        else:
            return 0
    elif num_of_words == 1:
        if sentence in unigram_frequency:
            return unigram_frequency[sentence]
        else:
            return 0
    return 0


def language_modelling(input_sentence):
    input_sentence.strip()
    words = input_sentence.split()    
    final_probability = 1

    for i in range(len(words)):
        c1 = 0
        c2 = 0

        if (i - 3) >= 0 :
            fourgram = words[i-3] + " " + words[i-2] + " " + words[i-1] + " " + words[i] #Fourgram
            trigram = words[i-3] + " " + words[i-2] + " " + words[i-1] #Trigram
            c1 = count_occurences(fourgram)
            c2 = count_occurences(trigram)
        elif (i - 2) >= 0:
            trigram = words[i-2] + " " + words[i-1] + " " + words[i] #Trigram
            bigram = words[i-2] + " " + words[i-1] #Bigram
            c1 = count_occurences(trigram)
            c2 = count_occurences(bigram)
        elif (i - 1) >= 0:
            bigram = words[i-1] + " " + words[i] #Bigram
            unigram = words[i-1] #Unigram
            c1 = count_occurences(bigram)
            c2 = count_occurences(unigram)
        else: #------------------------------------------------------------------------------------------------------------>Confirm this case and do it correctly
            unigram = words[i]
            c1 = count_occurences(unigram)
            c2 = len(unigram_frequency) #--------------------> won't be this

        # print(c1, c2)
        # print('--------------')

        if c1 == 0:
            final_probability = 0
        else:
            if c2 != 0:
                final_probability = final_probability * (c1/c2) 

    return final_probability


def preprocessing_technical_domain_corpus(corpus_file_name,tokens):
    corpus_file = open(corpus_file_name, "r")      
                   
    with corpus_file as file:
        for line in file:
            temp_str = ""
            for i in range(len(line)-1):
                if line[i] != " ":
                    if (line[i] >= 'a' and line[i] <= 'z') or (line[i] >= 'A' and line[i] <= 'Z') or (line[i] >= '0' and line[i] <= '9'):
                        # print("alpha numeric ", line[i])
                        temp_str += line[i]
                    else:
                        # print("non alpha numeric ", line[i])
                        if line[i] == 'µ' or line[i] == '+' or line[i] == '~' or line[i] == '%' or line[i] == '(' or line[i] == ')' or line[i] == 'ﬂ' or line[i] == 'ß' or line[i] == 'º' or line[i] == '{' or line[i] == '}' or line[i] == '*' or line[i] == '[' or line[i] == ']' or line[i] == 'à' or line[i] == '!' or line[i] == 'Ω' or line[i] == '”' or line[i] == ':' or line[i] == '/' or line[i] == '=':
                            if i-1 >= 0:
                                if line[i-1] != " ":
                                    temp_str += " "
                                temp_str += line[i]
                            if i+1 < len(line):
                                if line[i+1] != " ":
                                    temp_str += " "
                        elif line[i] == '‘' or line[i] == '\'' or line[i] == '’' or line[i] == 'í':
                            if i-1 >= 0:
                                if line[i-1] != " ":
                                    temp_str += " "
                                temp_str += "\'"
                            if i+1 < len(line):
                                if line[i+1] != " ":
                                    temp_str += " "
                        elif line[i] == 'ì' or line[i] == 'Î' or line[i] == '&':
                            temp_str += line[i]
                        elif line[i] == ';':
                            temp_str += '\n'
                        elif line[i] == ',':
                            pass
                        elif line[i] == '.':
                            if i == len(line)-2:
                                temp_str += '/eos'
                            else:
                                temp_str += line[i]
                                #---------------------------------------->>>> pass #do we have to add space?
                        elif line[i] == '?':
                            pass
                else:
                    temp_str += " "

            # print(temp_str)
            tokenized_str = temp_str.split()
            # print(tokenized_str)
            for unigram in tokenized_str :
                tokens.append(unigram)
        # print(tokens)
        return tokens



def preprocessing_health_domain_corpus(corpus_file_name,tokens):
    corpus_file = open(corpus_file_name, "r")  

    with corpus_file as file:
        for line in file:
            temp_str = ""
            for i in range(len(line)-1):
                if line[i] != " ":
                    if (line[i] >= 'a' and line[i] <= 'z') or (line[i] >= 'A' and line[i] <= 'Z') or (line[i] >= '0' and line[i] <= '9'):
                        temp_str += line[i]
                    else:
                        pass
                else:
                    temp_str += " "   

        tokenized_str = temp_str.split()
            for unigram in tokenized_str :
                tokens.append(unigram)

    return tokens
                  
    


def tokenization(tokens, unigram_frequency, bigram_frequency, trigram_frequency, fourgram_frequency):
    for i in range(len(tokens)):
        unigram = tokens[i]
        if unigram in unigram_frequency:
            unigram_frequency[unigram] += 1
        else:
            unigram_frequency[unigram] = 1
        i += 1
    
    for i in range(len(tokens)):
        if (i + 1) < len(tokens):
            bigram = tokens[i] + " " + tokens[i+1]                                       #Creating a bigram
            if bigram in bigram_frequency:
                bigram_frequency[bigram] += 1
            else:
                bigram_frequency[bigram] = 1
        else:
            break
        i += 2


    for i in range(len(tokens)):
        if (i + 2) < len(tokens):
            trigram = tokens[i] + " " + tokens[i+1] + " " + tokens[i+2]                             #Creating a trigram
            if trigram in trigram_frequency:
                trigram_frequency[trigram] += 1
            else:
                trigram_frequency[trigram] = 1
        else:
            break
        i += 3


    for i in range(len(tokens)):
        if (i + 3) < len(tokens):
            fourgram = tokens[i] + " " + tokens[i+1] + " " + tokens[i+2] + " " + tokens[i+3]                           #Creating a fourgram
            if fourgram in fourgram_frequency:
                fourgram_frequency[fourgram] += 1
            else:
                fourgram_frequency[fourgram] = 1
        else:
            break
        i += 4



correct_notation = False
while True:
    if correct_notation == True:
        break

    corpus = input("Enter the corpus text file : ")                     #Taking the corpus input from the user
    smoothing_technique = input("Enter the smoothing technique : ")     #Taking the smoothing technique input from the user
    input_sentence = input("Enter the sentence : ")                     #Taking the sentence input from the user whose probability has to be calculated

    if corpus != 't' and corpus != 'h':
        correct_notation = False
    elif smoothing_technique != 'k' and smoothing_technique != 'w':
        correct_notation = False
    else:
        correct_notation = True


# corpus_file_1 = open("Health_English.txt", "r")                     #Opening the Health corpus
# corpus_file_2 = open("eg1.txt", "r")                                  #Opening the Health corpus
# corpus_file_2 = open("technical_domain_corpus.txt", "r")            #Opening the Technical Domain corpus


tokens = []                                                         #List of all tokens
unigram_frequency = {}                                              #Dictionary of single tokens mapped to their frequency
bigram_frequency = {}                                               #Dictionary of double tokens mapped to their frequency
trigram_frequency = {}                                              #Dictionary of triple tokens mapped to their frequency
fourgram_frequency = {}
corpus_file_name = ""


if corpus == 't':
    # corpus_file_name = "technical_domain_corpus.txt"
    corpus_file_name = "eg1.txt"
    preprocessing_technical_domain_corpus(corpus_file_name,tokens)
elif corpus == 'h':
    corpus_file_name = "Health_English.txt"
    preprocessing_health_domain_corpus(corpus_file_name,tokens)
print(tokens)

tokenization(tokens, unigram_frequency,bigram_frequency,trigram_frequency,fourgram_frequency)
#-------------------------------------------------> process the input sentence first
print(language_modelling(input_sentence))


    # pass
# with corpus_file_1 as file:    
#     for line in file:
#         line_split = line.split()
#         for i in range(len(line_split)):
#             unigram = line_split[i]                      
#             unigram = unigram.lower()

#             if i == len(line_split) - 1:
#                 unigram = unigram[:len(unigram)-1]                            #To remove the full stop

#             tokens.append(unigram)
            
#             if i == len(line_split) - 1:
#                 tokens.append('\n')                                           #Representing '\n' as end of sentence
            
#             if unigram in unigram_frequency:
#                 unigram_frequency[unigram] += 1
#             else:
#                 unigram_frequency[unigram] = 1;  

#             for char in unigram:
#                 if char.isalnum() == False:
#                     special_characters.add(char)



# finatokens = []

# with corpus_file_2 as file:
#     for line in file:
#         temp_str = ""
#         for i in range(len(line)-1):
#             if line[i] != " ":
#                 if (line[i] >= 'a' and line[i] <= 'z') or (line[i] >= 'A' and line[i] <= 'Z') or (line[i] >= '0' and line[i] <= '9'):
#                     # print("alpha numeric ", line[i])
#                     temp_str += line[i]
#                 else:
#                     # print("non alpha numeric ", line[i])
#                     if line[i] == 'µ' or line[i] == '+' or line[i] == '~' or line[i] == '%' or line[i] == '(' or line[i] == ')' or line[i] == 'ﬂ' or line[i] == 'ß' or line[i] == 'º' or line[i] == '{' or line[i] == '}' or line[i] == '*' or line[i] == '[' or line[i] == ']' or line[i] == 'à' or line[i] == '!' or line[i] == 'Ω' or line[i] == '”' or line[i] == ':' or line[i] == '/' or line[i] == '=':
#                         if i-1 >= 0:
#                             if line[i-1] != " ":
#                                 temp_str += " "
#                             temp_str += line[i]
#                         if i+1 < len(line):
#                             if line[i+1] != " ":
#                                 temp_str += " "
#                     elif line[i] == '‘' or line[i] == '\'' or line[i] == '’' or line[i] == 'í':
#                         # print(line[i])
#                         if i-1 >= 0:
#                             if line[i-1] != " ":
#                                 temp_str += " "
#                             temp_str += "\'"
#                         if i+1 < len(line):
#                             if line[i+1] != " ":
#                                 temp_str += " "
#                     elif line[i] == 'ì' or line[i] == 'Î' or line[i] == '&':
#                         temp_str += line[i]
#                     elif line[i] == ';':
#                         temp_str += '\n'
#                     elif line[i] == ',':
#                         pass
#                     elif line[i] == '.':
#                         # print("came", line[8])
#                         if i == len(line)-2:
#                             temp_str += '/eos'
#                         else:
#                             temp_str += line[i]
#                             #---------------------------------------->>>> pass #do we have to add space?
#                     elif line[i] == '?':
#                         pass
#             else:
#                 temp_str += " "

#         print(temp_str)
#         tokenized_str = temp_str.split()
#         print(tokenized_str)
#         for unigram in tokenized_str :
#             tokens.append(unigram)
#             if unigram in unigram_frequency:
#                 unigram_frequency[unigram] += 1
#             else:
#                 unigram_frequency[unigram] = 1

            
# print(tokens)




        # print(line, type(line))
        # print(type(line))
        # line_split = line.split()
        # for i in range(len(line_split)):
        #     for j in range(len(line_split[i])):
        #         unigram_a = ""
        #         unigram_b = ""
        #         unigram_c = ""
        #         # print(line_split[i][j].isalnum())
        #         if line_split[i][j].isalnum() == False:
        #             # print("first")
        #             if line_split[i][j] == '+' or line_split[i][j] == '%':
        #                 # print("second")
        #                 if len(line_split[i]) == 1:
        #                     unigram_a = line_split[i][j]
        #                 else :
        #                     unigram_a = line_split[i][:j]
        #                     unigram_b = line_split[i][j]
        #                     unigram_c = line_split[i][j+1:len(line_split[i])]
        #                     print(unigram_a)
        #                     print(unigram_b)
        #                     print(unigram_c)
                








# special_characters.remove('.') #----------------------------------------------> Just testing something



# token_indices_to_delete = []
# for i in range(len(tokens)):
#     token = tokens[i]
#     for character in token:
#         if character in special_characters:
#             token_indices_to_delete.append(i)
#             break


# print(len(tokens))


# j = 0
# new_tokens = []
# for i in range(len(tokens)):
#     if j < len(token_indices_to_delete):
#         if i != token_indices_to_delete[j]:
#             new_tokens.append(tokens[i])
#         else:
#             j+=1
#     else:
#         new_tokens.append(tokens[i])

# print(len(new_tokens))
# tokens = new_tokens

# print(len(tokens))

















# for i in range(len(tokens)):
#     if (i + 1) < len(tokens):
#         a = tokens[i]
#         b = tokens[i+1]
#         bigram = a + " " + b                                        #Creating a bigram
#         if bigram in bigram_frequency:
#             bigram_frequency[bigram] += 1
#         else:
#             bigram_frequency[bigram] = 1
#     else:
#         break
#     i += 2


# for i in range(len(tokens)):
#     if (i + 2) < len(tokens):
#         a = tokens[i]
#         b = tokens[i+1]
#         c = tokens[i+2]
#         trigram = a + " " + b + " " + c                             #Creating a trigram
#         if trigram in trigram_frequency:
#             trigram_frequency[trigram] += 1
#         else:
#             trigram_frequency[trigram] = 1
#     else:
#         break
#     i += 3


# for i in range(len(tokens)):
#     if (i + 3) < len(tokens):
#         a = tokens[i]
#         b = tokens[i+1]
#         c = tokens[i+2]
#         d = tokens[i+3]
#         fourgram = a + " " + b + " " + c + " " + d                            #Creating a fourgram
#         if fourgram in fourgram_frequency:
#             fourgram_frequency[fourgram] += 1
#         else:
#             fourgram_frequency[fourgram] = 1
#     else:
#         break
#     i += 4


# print('-----------------------------------------------------------------')
# print(unigram_frequency)
# print('-----------------------------------------------------------------')
# print(bigram_frequency)
# print('-----------------------------------------------------------------')
# print(trigram_frequency)
# print('-----------------------------------------------------------------')
# print(fourgram_frequency)
# print('-----------------------------------------------------------------')
# print()

# print(language_modelling(input_sentence))