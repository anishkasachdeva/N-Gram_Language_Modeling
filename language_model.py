corpus = input("Enter the corpus text file : ")                     #Taking the corpus input from the user
smoothing_technique = input("Enter the smoothing technique : ")     #Taking the smoothing technique input from the user
input_sentence = input("Enter the sentence : ")                     #Taking the sentence input from the user whose probability has to be calculated


corpus_file_1 = open("Health_English.txt", "r")                     #Opening the Health corpus
corpus_file_2 = open("technical_domain_corpus.txt", "r")            #Opening the Technical Domain corpus


tokens = []                                                         #List of all tokens
unigram_frequency = {}                                              #Dictionary of single tokens mapped to their frequency
bigram_frequency = {}                                               #Dictionary of double tokens mapped to their frequency
trigram_frequency = {}                                              #Dictionary of triple tokens mapped to their frequency


with corpus_file_1 as file:    
    for line in file:                                               #Reading each line 
        for word in line.split():                                   #Reading each word
            unigram = word.lower()                                  #Changing the words to lowercase       
            tokens.append(unigram)
            if unigram in unigram_frequency:
                unigram_frequency[unigram] += 1
            else:
                unigram_frequency[unigram] = 1;  


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


print(unigram_frequency)
print('-----------------------------------------------------------------')
print(bigram_frequency)
print('-----------------------------------------------------------------')
print(trigram_frequency)
print('-----------------------------------------------------------------')


def tokenize():
    pass


def language_modelling():
    pass


def perplexity():
    pass


def smoothing():
    pass