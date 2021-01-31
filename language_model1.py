import pprint
import os
import sys
import pprint
import math
import re

def tokenize(ip_text) :
    start_tag = "<"
    end_tag = ">"
    ret = []
    lines = ip_text.split("\n")
    for i in range(len(lines)):
        temp = []
        words = lines[i].split(" ")
        for word in words:
            token = ""
            for ch in word:
                if (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z'):
                    token=token+ch
                    token=token.lower()
            if len(token)>0 :
                temp.append(token)
        if len(temp)>0:
            temp = ["<", "<", "<"] + temp
            temp.append(">")
            ret.append(temp)
    return ret

# def tokenize(ip_text):
#     text = []
#     for line in ip_text:
#         if line.strip():
#             line = re.sub(r'[^a-zA-Z ]',r'',line)
#             line = line.lower()
#             tokens = re.split(r"\s+", line)
#             tokens.append('>')
#             tokens =  ['<', '<', '<'] + tokens
#             text.append(tokens)
#     return text


def mapsFormatation(tokens):
    unigram_map = {}
    bigram_map = {}
    trigram_map = {}
    fourgram_map = {}

    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            a = tokens[i][j]
            if a in unigram_map:
                unigram_map[a] += 1
            else:
                unigram_map[a] = 1


    for i in range(len(tokens)):
        for j in range(len(tokens[i]) - 1):
            a = tokens[i][j]
            b = tokens[i][j+1]

            if a in bigram_map:
                if b in bigram_map[a]:
                    bigram_map[a][b] += 1
                else:
                    bigram_map[a][b] = 1
            else:
                bigram_map[a] = {}
                bigram_map[a][b] = 1


    for i in range(len(tokens)):
        for j in range(len(tokens[i]) - 2):
            a = tokens[i][j]
            b = tokens[i][j+1]
            c = tokens[i][j+2]

            if a in trigram_map:
                if b in trigram_map[a]:
                    if c in trigram_map[a][b]:
                        trigram_map[a][b][c] += 1
                    else:
                        trigram_map[a][b][c] = 1
                else:
                    trigram_map[a][b] = {}
                    trigram_map[a][b][c] = 1
            else:
                trigram_map[a] = {}
                trigram_map[a][b] = {}
                trigram_map[a][b][c] = 1



    for i in range(len(tokens) - 3):
        for j in range(len(tokens[i]) - 3):
            a = tokens[i][j]
            b = tokens[i][j+1]
            c = tokens[i][j+2]
            d = tokens[i][j+3]

            if a in fourgram_map:
                if b in fourgram_map[a]:
                    if c in fourgram_map[a][b]:
                        if d in fourgram_map[a][b][c]:
                            fourgram_map[a][b][c][d] +=1
                        else:
                            fourgram_map[a][b][c][d] = 1
                    else:
                        fourgram_map[a][b][c] = {}
                        fourgram_map[a][b][c][d] = 1
                else:
                    fourgram_map[a][b] = {}
                    fourgram_map[a][b][c] = {}
                    fourgram_map[a][b][c][d] = 1
            else:
                fourgram_map[a] = {}
                fourgram_map[a][b] = {}
                fourgram_map[a][b][c] = {}
                fourgram_map[a][b][c][d] = 1

    return unigram_map,bigram_map,trigram_map,fourgram_map


def kneser_ney_smoothing(a, b, c, d, unigram_map, bigram_map, trigram_map, fourgram_map):

    # print(a + "  " + b + "  " + c + "  " + d)
    discounting_factor = 0.75
    partial_probability = 0

    if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:

    #-------------------------------------------------Calculation of P(d|abc)
        Ckn_abcd = 0
        Ckn_abc = 0
        
        if a in fourgram_map:
            if b in fourgram_map[a]:
                if c in fourgram_map[a][b]:
                    if d in fourgram_map[a][b][c]:
                        Ckn_abcd = fourgram_map[a][b][c][d]
        
        # print(Ckn_abcd)
        if a in trigram_map:
            if b in trigram_map[a]:
                if c in trigram_map[a][b]:
                    Ckn_abc = trigram_map[a][b][c]

        # print(Ckn_abc)

        first_term_1 = float(max(Ckn_abcd - discounting_factor, 0))/float(Ckn_abc)
        
        # print(first_term_1)

        num_1 = 0
        deno_1 = 0

        if a in fourgram_map:
            if b in fourgram_map[a]:
                if c in fourgram_map[a][b]:
                    num_1 = len(fourgram_map[a][b][c])

        if a in trigram_map:
            if b in trigram_map[a]:
                if c in trigram_map[a][b]:
                    deno_1 = trigram_map[a][b][c]

        lambda_abc = float(discounting_factor * num_1)/float(deno_1)

        # print(lambda_abc)
        #-------------------------------------------------Calculation of P(d|bc)

        Ccn_bcd = 0
        CCn_bc = 0

        for i in fourgram_map:
            if b in fourgram_map[i]:
                if c in fourgram_map[i][b]:
                    if d in fourgram_map[i][b][c]:
                        Ccn_bcd += 1

        for i in fourgram_map:
            if b in fourgram_map[i]:
                if c in fourgram_map[i][b]:
                    CCn_bc += len(fourgram_map[i][b][c])


        first_term_2 = float(max(Ccn_bcd - discounting_factor,0))/float(CCn_bc)

        num_2 = 0
        deno_2 = 0

        if b in trigram_map:
            if c in trigram_map[b]:
                num_2 = len(trigram_map[b][c])

        if b in bigram_map:
            if c in bigram_map[b]:
                deno_2 = bigram_map[b][c]


        lambda_bc = float(discounting_factor * num_2)/float(deno_2)

        # print(lambda_bc)
        #-------------------------------------------------Calculation of P(d|c)

        CCn_cd = 0
        CCn_c = 0

        for i in trigram_map:
            if c in trigram_map[i]:
                if d in trigram_map[i][c]:
                    CCn_cd += 1

        for i in trigram_map:
            if c in trigram_map[i]:
                CCn_c += len(trigram_map[i][c])

        first_term_3 = float(max(CCn_cd - discounting_factor,0))/float(CCn_c)

        num_3 = 0
        deno_3 = 0

        if c in bigram_map:
            num_3 = len(bigram_map[c])

        if c in unigram_map:
            deno_3 = unigram_map[c]

        lambda_c = float(discounting_factor * num_3)/float(deno_3)

        # print(lambda_c)
        #-------------------------------------------------Calculation of P(d|phi)

        CCn_phi_d = 0
        CCn_phi = 0

        for i in bigram_map:
            if d in bigram_map[i]:
                CCn_phi_d += 1
        
        CCn_phi = len(bigram_map)

        # print(CCn_phi_d)
        # print(CCn_phi)
        first_term_4 = float(max(CCn_phi_d - discounting_factor,0))/float(CCn_phi)
        
        num_4 = 0
        deno_4 = 0

        num_4 = len(unigram_map)

        for i in unigram_map:
            deno_4 = unigram_map[i]
        
        lambda_phi = float(discounting_factor * num_4) / float(deno_4)
        

        last_term = float(1) / float(len(unigram_map))

        # print(lambda_phi * last_term)
        
        # print(last_term)
        #-------------------------------------------------Calculation of Partial Probability

        partial_probability = (first_term_1 + lambda_abc * (first_term_2 + lambda_bc * (first_term_3 + lambda_c * (first_term_4 + lambda_phi * last_term))))

        # print(partial_probability)
        return math.log(partial_probability)
    else:
        total_words = 0
        for i in unigram_map:
            total_words += unigram_map[i]
        partial_probability = float(discounting_factor / total_words)

        return math.log(partial_probability)

    return partial_probability

def perplexity(partial_probability):
    pass


smoothing_technique = sys.argv[1]
corpus = sys.argv[2]
# final_probability = 0

if os.path.exists(corpus):
    while True:
        input_sen = input("input sentence : ")
        ip_file = open(corpus,"r")
        ip_text_train = ip_file.read()
        tokens = tokenize(ip_text_train)

        
        input_sentence = tokenize(input_sen)
        
        # print(tokens)
        # pprint.pprint(fourgram_map, width=1)
        # for i in input_sentence:
        #     print(i)

        train = []
        test = []

        # print(len(tokens))
        for i in range(20):
            # print(tokens[i])
            train.append(tokens[i])
        
        for i in range(20,len(tokens)):
            test.append(tokens[i])

        # print(test)

        unigram_map, bigram_map, trigram_map, fourgram_map = mapsFormatation(train)
        
        f1 = open("2018101112-LM1-test-perplexity.txt", "a")
        
        if smoothing_technique == 'k'or smoothing_technique == 'K':
            for i in range(len(test)):
                final_probability = 0
                sentence = ""
                for j in range(3,len(test[i])):
                    sentence += test[i][j] + " "
                    a = test[i][j-3]
                    b = test[i][j-2]
                    c = test[i][j-1]
                    d = test[i][j]

                    partial_probability = kneser_ney_smoothing(a, b, c, d, unigram_map, bigram_map, trigram_map, fourgram_map)
                    # print("partial probability", partial_probability)

                    final_probability = final_probability + partial_probability

                print((final_probability))
                f1.write(sentence)
                f1.write("\t")
                f1.write(str(final_probability))
                f1.write("\n")
                
            f1.close
        elif smoothing_technique == 'w' or smoothing_technique == 'W':
            pass
        else:
            print("Wrong Smoothing Technique. Please try again!")
else:
    print("Wrong File Name. Please try again!")






# log probability ?