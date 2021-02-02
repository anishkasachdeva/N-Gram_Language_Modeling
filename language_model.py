import pprint, os , sys, pprint, math, re, random

def tokenize(input_text):
    tokens = []
    lines = input_text.split("\n")
    for i in range(len(lines)):
        temp = []
        words = lines[i].split(" ")
        for word in words:
            token = ""
            for j in range(len(word)):
                if (word[j] >= 'a' and word[j] <= 'z') or (word[j] >= 'A' and word[j] <= 'Z'):
                    token = token + word[j]
            token = token.lower()
            
            if len(token) >= 1 :
                temp.append(token)
        if len(temp) >= 1:
            temp = ["<", "<", "<"] + temp
            temp.append(">")
            tokens.append(temp)
    return tokens


def formUnigramMap(tokens):
    unigram_map = {}
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            a = tokens[i][j]
            # print(a)
            if a in unigram_map:
                unigram_map[a] += 1
            else:
                unigram_map[a] = 1
    return unigram_map


def formBigramMap(tokens):
    bigram_map = {}
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
    return bigram_map


def formTrigramMap(tokens):
    trigram_map = {}
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
    return trigram_map


def formFourgramMap(tokens):
    fourgram_map = {}
    for i in range(len(tokens)):
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
    return fourgram_map


def mark_unknown_words(input_tokens):
    unknown_word = "<markunkwownmark>"
    frequency = []
    unigram_map = formUnigramMap(train)
    for word in unigram_map:
        frequency.append(unigram_map[word])

    frequency.sort()
    lower_limit = frequency[int(0.05*len(frequency))]

    for i in range(len(input_tokens)):
        for j in range(len(input_tokens[i])):
            if unigram_map[input_tokens[i][j]] <= lower_limit:
                if input_tokens[i][j] != "<" and input_tokens[i][j] != ">":
                    input_tokens[i][j] = unknown_word
    return input_tokens


def mark_unknown_test(test, unigram_map):
    unknown_word = "<markunkwownmark>"
    for i in range(len(test)):
        for j in range(len(test[i])):
            if test[i][j] not in unigram_map:
                test[i][j] = unknown_word
    return test


def witten_bell_smoothing(sen, unigram_map, bigram_map, trigram_map, fourgram_map, fourgrams_variety, total_words):
    discounting_factor = 0.75
    final_probability_of_sentence = 0.0
    Vocab = len(unigram_map)

    for index in range(3, len(sen)):
        a = sen[index - 3]
        b = sen[index - 2]
        c = sen[index - 1]
        d = sen[index]
        partial_probability = 0.0

        if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:

            num_1 = len(fourgram_map[a][b][c])
            deno_1 = len(fourgram_map[a][b][c]) + trigram_map[a][b][c]
            lambda_abc = 1-float(num_1)/float(deno_1)

            f_abc = 0

            if d not in fourgram_map[a][b][c]:
                cnt_abc_variety = len(fourgram_map[a][b][c])
                cnt_abc = trigram_map[a][b][c]
                f_abc = float(cnt_abc_variety)/float((Vocab - cnt_abc_variety)*(cnt_abc + cnt_abc_variety))                
            else:
                cnt_abcd = fourgram_map[a][b][c][d]
                cnt_abc_variety = len(fourgram_map[a][b][c])
                cnt_abc = trigram_map[a][b][c]
                f_abc = float(cnt_abcd)/float(cnt_abc + cnt_abc_variety)

            #---------------------------------------------------------------------------------------------------

            num_2 = len(trigram_map[b][c])
            deno_2 = len(trigram_map[b][c]) + bigram_map[b][c] 
            lambda_bc = 1-float(num_2)/float(deno_2)

            f_bc = 0

            if d not in trigram_map[b][c]:
                cnt_bc_variety = len(trigram_map[b][c])
                cnt_bc = bigram_map[b][c]
                f_bc = float(cnt_bc_variety)/float((Vocab - cnt_bc_variety)*(cnt_bc + cnt_bc_variety))
            else:
                cnt_bcd = trigram_map[b][c][d]
                cnt_bc_variety = len(trigram_map[b][c])
                cnt_bc = bigram_map[b][c]
                f_bc = float(cnt_bcd)/float(cnt_bc + cnt_bc_variety)

            #---------------------------------------------------------------------------------------------------
            
            num_3 = len(bigram_map[c])
            deno_3 = len(bigram_map[c]) + unigram_map[c]
            lambda_c = 1-float(num_3)/float(deno_3)

            f_c = 0

            if d not in bigram_map[c]:
                cnt_c_variety = len(bigram_map[c])
                cnt_c = unigram_map[c]
                f_c = float(cnt_c_variety)/float((Vocab - cnt_c_variety)*(cnt_c + cnt_c_variety))
            else:
                cnt_cd = bigram_map[c][d]
                cnt_c_variety = len(bigram_map[c])
                cnt_c = unigram_map[c]
                f_c = float(cnt_cd)/float(cnt_c + cnt_c_variety)
            #---------------------------------------------------------------------------------------------------
            cnt_d = 0
            if d in unigram_map:
                cnt_d = unigram_map[d]

            last_term = float(cnt_d)/float(total_words + Vocab)
            
            partial_probability = (lambda_abc * f_abc + (1 - lambda_abc) * (lambda_bc * f_bc + (1 - lambda_bc) * (lambda_c * f_c + (1 - lambda_c) * last_term)))

        else:
            lambd = (float(discounting_factor)/float(total_words))*len(unigram_map)
            partial_probability = float(lambd)/float(fourgrams_variety)

        final_probability_of_sentence += math.log(partial_probability)
    return final_probability_of_sentence        


def kneser_ney_smoothing(sen, unigram_map, bigram_map, trigram_map, fourgram_map, fourgrams_variety, total_words):
    discounting_factor = 0.75
    final_probability_of_sentence = 0.0

    for index in range(3, len(sen)):
        a = sen[index-3]
        b = sen[index-2]
        c = sen[index-1]
        d = sen[index]
        partial_probability = 0.0

        if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:
            # print(a,b,c,d)

        #-------------------------------------------------Calculation of P(d|abc)
        
            Ckn_abcd = 0
            Ckn_abc = 0
            if d in fourgram_map[a][b][c]:
                Ckn_abcd = fourgram_map[a][b][c][d]
            Ckn_abc = trigram_map[a][b][c]
            first_term_1 = float(max(Ckn_abcd - discounting_factor, 0))/float(Ckn_abc)

            num_1 = 0
            deno_1 = 0
            num_1 = len(fourgram_map[a][b][c])
            deno_1 = trigram_map[a][b][c]
            lambda_abc = float(discounting_factor * num_1)/float(deno_1)
            
            #-------------------------------------------------Calculation of P(d|bc)

            Ccn_bcd = 0
            CCn_bc = 0
            for i in fourgram_map:
                if b in fourgram_map[i] and c in fourgram_map[i][b] and d in fourgram_map[i][b][c]:
                    Ccn_bcd += 1
            for i in fourgram_map:
                if b in fourgram_map[i] and c in fourgram_map[i][b]:
                    CCn_bc += len(fourgram_map[i][b][c])
            first_term_2 = float(max(Ccn_bcd - discounting_factor,0))/float(CCn_bc)

            num_2 = 0
            deno_2 = 0
            num_2 = len(trigram_map[b][c])
            deno_2 = bigram_map[b][c]
            lambda_bc = float(discounting_factor * num_2)/float(deno_2)
            
            #-------------------------------------------------Calculation of P(d|c)

            CCn_cd = 0
            CCn_c = 0
            for i in trigram_map:
                if c in trigram_map[i] and d in trigram_map[i][c]:
                    CCn_cd += 1
            for i in trigram_map:
                if c in trigram_map[i]:
                    CCn_c += len(trigram_map[i][c])
            first_term_3 = float(max(CCn_cd - discounting_factor,0))/float(CCn_c)

            num_3 = 0
            deno_3 = 0
            num_3 = len(bigram_map[c])
            deno_3 = unigram_map[c]
            lambda_c = float(discounting_factor * num_3)/float(deno_3)
            #-------------------------------------------------Calculation of P(d|phi)
            CCn_phi_d = 0
            CCn_phi = 0

            for i in bigram_map:
                if d in bigram_map[i]:
                    CCn_phi_d += 1
            for i in bigram_map:
                CCn_phi += len(bigram_map[i])
            first_term_4 = float(max(CCn_phi_d - discounting_factor,0))/float(CCn_phi)

            num_4 = 0
            deno_4 = 0
            num_4 = len(unigram_map)
            for i in unigram_map:
                deno_4 += unigram_map[i]
            lambda_phi = float(discounting_factor)/float(deno_4)
            #-------------------------------------------------Calculation of Partial Probability
            
            partial_probability = (first_term_1 + lambda_abc * (first_term_2 + lambda_bc * (first_term_3 + lambda_c * (first_term_4 + lambda_phi))))
            
        else:
            lambd = (float(discounting_factor)/float(total_words))*len(unigram_map)
            partial_probability = float(lambd)/float(fourgrams_variety)

        final_probability_of_sentence += math.log(partial_probability)
    return final_probability_of_sentence


def calculate_perplexity_of_sentence(probability, n):
    return float(1)/float(math.exp(float(probability)/float(n)))


def perplexity_Train_Test(dataset, file_to_write, unigram_map, bigram_map, trigram_map, fourgram_map ):
    for i in range(len(dataset)):
        final_probability_of_sentence = 0
        sentence = ""
        for j in range(3,len(dataset[i])):
            a = dataset[i][j-3]
            b = dataset[i][j-2]
            c = dataset[i][j-1]
            d = dataset[i][j]
            partial_probabilities_of_sentence = kneser_ney_smoothing(a, b, c, d, unigram_map, bigram_map, trigram_map, fourgram_map)

            final_probability_of_sentence += partial_probabilities_of_sentence

        perplexity = calculate_perplexity_of_sentence(final_probability_of_sentence)
        
        file_to_write.write("Hello " + '\t')
        file_to_write.write(str(perplexity) + '\n')


# def file_open():
#     f1 = open("2018101112-LM1-train-perplexity.txt", "w")
#     f2 = open("2018101112-LM1-test-perplexity.txt", "w")
#     f3 = open("2018101112-LM2-train-perplexity.txt", "w")
#     f4 = open("2018101112-LM2-test-perplexity.txt", "w")
#     f5 = open("2018101112-LM3-train-perplexity.txt", "w")
#     f6 = open("2018101112-LM3-test-perplexity.txt", "w")
#     f7 = open("2018101112-LM4-train-perplexity.txt", "w")
#     f8 = open("2018101112-LM4-test-perplexity.txt", "w")
#     return f1,f2,f3,f4,f5,f6,f7,f8


# def file_close(f1,f2,f3,f4,f5,f6,f7,f8):
#     f1.close()
#     f2.close()
#     f3.close()
#     f4.close()
#     f5.close()
#     f6.close()
#     f7.close()
#     f8.close()

#--------------------------------------------------------------------------------> System input by the user
smoothing_technique = sys.argv[1]
corpus = sys.argv[2]

if os.path.exists(corpus):
    while True:
        input_sen = input("input sentence : ")
        if input_sen == " " or input_sen == "":
            print(0.0)
        else:
            ip_file = open(corpus,"r")
            ip_text_train = ip_file.read()
            tokens = tokenize(ip_text_train)
            input_sentence = tokenize(input_sen)

            train = []
            test = []

            random.shuffle(tokens)
            
            # for i in range(1000):
                # test.append(tokens[i])
            
            for i in range(0,len(tokens)):
                train.append(tokens[i])

            train = mark_unknown_words(train)

            unigram_map = formUnigramMap(train)
            bigram_map = formBigramMap(train)
            trigram_map = formTrigramMap(train)
            fourgram_map = formFourgramMap(train)
            
            test = mark_unknown_test(test, unigram_map)
            
            # ---------------------------------------------------------------------------------------> Started file writing part
            # train_t = []
            # test_t = []
            # ip_file_t = open("./technical_domain_corpus.txt","r")
            # ip_text_t = ip_file_t.read()
            # tokens_t = tokenize(ip_text_t)
            
            # train_h = []
            # test_h = []
            # ip_file_h = open("./Health_English.txt","r")
            # ip_text_h = ip_file_h.read()
            # tokens_h = tokenize(ip_text_h)

            # for i in range(10):
            #     test_t.append(tokens_t[i])
            # for i in range(10, 20):
            #     train_t.append(tokens_t[i])

            # for i in range(10):
            #     test_h.append(tokens_h[i])
            # for i in range(10, 20):
            #     train_h.append(tokens_h[i])

            # f1,f2,f3,f4,f5,f6,f7,f8 = file_open()

            # for i in range(8):
            #     if i < 4:
            #         unigram_map_t, bigram_map_t, trigram_map_t, fourgram_map_t = mapsFormatation(train_t)
            #     else:
            #         unigram_map_h, bigram_map_h, trigram_map_h, fourgram_map_h = mapsFormatation(train_h)
            #     if i == 0:
            #         perplexity_Train_Test(train_t, f1, unigram_map_t, bigram_map_t, trigram_map_t, fourgram_map_t)
            #     elif i == 1:
            #         perplexity_Train_Test(test_t, f2, unigram_map_t, bigram_map_t, trigram_map_t, fourgram_map_t)
            #     elif i == 2:
            #         perplexity_Train_Test(train_t, f3,  unigram_map_t, bigram_map_t, trigram_map_t, fourgram_map_t)
            #     elif i == 3:
            #         perplexity_Train_Test(test_t, f4,  unigram_map_t, bigram_map_t, trigram_map_t, fourgram_map_t)
            #     elif i == 4:
            #         perplexity_Train_Test(train_h, f5, unigram_map_h, bigram_map_h, trigram_map_h, fourgram_map_h)
            #     elif i == 5:
            #         perplexity_Train_Test(test_h, f6, unigram_map_h, bigram_map_h, trigram_map_h, fourgram_map_h)
            #     elif i == 6:
            #         perplexity_Train_Test(train_h, f7, unigram_map_h, bigram_map_h, trigram_map_h, fourgram_map_h)
            #     elif i == 7:
            #         perplexity_Train_Test(test_h, f8, unigram_map_h, bigram_map_h, trigram_map_h, fourgram_map_h)


            # file_close(f1,f2,f3,f4,f5,f6,f7,f8)
            #---------------------------------------------------------------------------------------> Finished file writing part


            # --------------------------------------------------------------------------------------------------------------------------------------------------
            total_words = 0
            for i in unigram_map:
                total_words += unigram_map[i]
            
            fourgrams_variety = 0
            for i in fourgram_map:
                for j in fourgram_map[i]:
                    for k in fourgram_map[i][j]:
                        fourgrams_variety += len(fourgram_map[i][j][k])

            if smoothing_technique == 'k'or smoothing_technique == 'K':
                final_probability_of_sentence = kneser_ney_smoothing(input_sentence[0], unigram_map, bigram_map, trigram_map, fourgram_map, fourgrams_variety, total_words)

                # for i in range(len(test)):
                #     final_probability_of_sentence = kneser_ney_smoothing(test[i], unigram_map, bigram_map, trigram_map, fourgram_map, fourgrams_variety, total_words)
                # print(final_probability_of_sentence)
                print(math.exp(final_probability_of_sentence))
            # --------------------------------------------------------------------------------------------------------------------------------------------------
            elif smoothing_technique == 'w' or smoothing_technique == 'W':
                    final_probability_of_sentence = witten_bell_smoothing(input_sentence[0], unigram_map, bigram_map, trigram_map, fourgram_map, fourgrams_variety, total_words)

                # for i in range(len(test)):
                        # final_probability_of_sentence = witten_bell_smoothing(test[i], unigram_map, bigram_map, trigram_map, fourgram_map, fourgrams_variety, total_words)
                    print(math.exp(final_probability_of_sentence))

                    # print("perplexity of sentence ", perplexity_of_sentence)
            else:
                print("Wrong Smoothing Technique. Please try again!")
else:
    print("Wrong File Name. Please try again!")