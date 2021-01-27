
# corpus = input("Enter the corpus text file")
# smoothing_technique = input("Enter the smoothing technique")

corpus_file = open("technical_domain_corpus.txt", "r")
# corpus_file = open("technical_domain_corpus.txt", "r")





# from nltk import ngrams

# sentence = 'this is a foo bar sentences and i want to ngramize it'

# n = 4
# sixgrams = ngrams(sentence.split(), n)

# for grams in sixgrams:
#   print(grams)


tokens = [] #list of all tokens

unigram_frequency = {} #dictionary of single tokens mapped to their frequency
bigram_frequency = {} #dictionary of double tokens mapped to their frequency
trigram_frequency = {} #dictionary of triple tokens mapped to their frequency

# print(corpus_file.read(100))

with corpus_file as file:    
    # reading each line     
    for line in file: 
        # reading each word         
        for word in line.split(): 
            # changing the case the words 
            unigram = word.lower()           
            tokens.append(unigram)
            if unigram in unigram_frequency:
                unigram_frequency[unigram] += 1
            else:
                unigram_frequency[unigram] = 1;  


for i in range(len(tokens)):
    if (i + 1) < len(tokens):
        a = tokens[i]
        b = tokens[i+1]
        bigram = a + " " + b
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
        trigram = a + " " + b + " " + c
        if trigram in trigram_frequency:
            trigram_frequency[trigram] += 1
        else:
            trigram_frequency[trigram] = 1
    else:
        break
    i += 3

# print(tokens)


print(unigram_frequency)
print('-----------------------------------------------------------------')
print(bigram_frequency)
print('-----------------------------------------------------------------')
print(trigram_frequency)
print('-----------------------------------------------------------------')

# for index in range()

three_dict = {}

# with corpus_file as f1: 
#     data=iter(corpus_file.read().split())

# print(data)

# while True:
#     try:
#         a = next(data)
#         b = next(data)
#         c = next(data)
#         three_sentence = a + " " + b + " " + c 
#         if three_sentence in three_dict:
#             three_dict[three_sentence]+=1
#         else:
#             three_dict[three_sentence] = 1
#         # print(a,b,c)

#     except StopIteration:
#         print("No more pair")
#         break

# print(three_dict)

def tokenize():
    pass

def language_modelling():
    pass

def perplexity():
    pass

def smoothing():
    pass