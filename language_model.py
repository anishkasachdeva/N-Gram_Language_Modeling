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




corpus = input("Enter the corpus text file : ")                     #Taking the corpus input from the user
smoothing_technique = input("Enter the smoothing technique : ")     #Taking the smoothing technique input from the user
input_sentence = input("Enter the sentence : ")                     #Taking the sentence input from the user whose probability has to be calculated


# corpus_file_1 = open("Health_English.txt", "r")                     #Opening the Health corpus
corpus_file_1 = open("eg.txt", "r")                     #Opening the Health corpus
# corpus_file_1 = open("technical_domain_corpus.txt", "r")            #Opening the Technical Domain corpus


tokens = []                                                         #List of all tokens
unigram_frequency = {}                                              #Dictionary of single tokens mapped to their frequency
bigram_frequency = {}                                               #Dictionary of double tokens mapped to their frequency
trigram_frequency = {}                                              #Dictionary of triple tokens mapped to their frequency
fourgram_frequency = {}

special_characters = set()

with corpus_file_1 as file:    
    for line in file:
        line_split = line.split()
        # print("length ", len(line_split))                                               #Reading each line 
        # for unigram in line.split():   
        for i in range(len(line_split)):
            unigram = line_split[i]                           
            unigram = unigram.lower()
            if i == len(line_split) - 1:
                unigram = unigram[:len(unigram)-1]                            #To remove the full stop

            tokens.append(unigram)
            
            if i == len(line_split) - 1:
                tokens.append('\n')                                           #Representing '\n' as end of sentence
            
            if unigram in unigram_frequency:
                unigram_frequency[unigram] += 1
            else:
                unigram_frequency[unigram] = 1;  

            for char in unigram:
                if char.isalnum() == False:
                    special_characters.add(char)


special_characters.remove('.') #----------------------------------------------> Just testing something



token_indices_to_delete = []
for i in range(len(tokens)):
    token = tokens[i]
    for character in token:
        print(character)
        if character in special_characters:
            token_indices_to_delete.append(i)
            break

new_tokens = []
for i in range(len(tokens)):
    if i not in token_indices_to_delete:
        new_tokens.append(tokens[i])

print(new_tokens)

for i in range(len(tokens)):
    if (i + 1) < len(tokens):
        a = tokens[i]
        b = tokens[i+1]
        bigram = a + " " + b                                        #Creating a bigram
        if bigram in bigram_frequency:
            bigram_frequency[bigram] += 1
        else:
            bigram_frequency[bigram] = 1
    else:
        break
    i += 2


for i in range(len(tokens)):
    if (i + 2) < len(tokens):
        a = tokens[i]
        b = tokens[i+1]
        c = tokens[i+2]
        trigram = a + " " + b + " " + c                             #Creating a trigram
        if trigram in trigram_frequency:
            trigram_frequency[trigram] += 1
        else:
            trigram_frequency[trigram] = 1
    else:
        break
    i += 3


for i in range(len(tokens)):
    if (i + 3) < len(tokens):
        a = tokens[i]
        b = tokens[i+1]
        c = tokens[i+2]
        d = tokens[i+3]
        fourgram = a + " " + b + " " + c + " " + d                            #Creating a trigram
        if fourgram in fourgram_frequency:
            fourgram_frequency[fourgram] += 1
        else:
            fourgram_frequency[fourgram] = 1
    else:
        break
    i += 4


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

print(language_modelling(input_sentence))