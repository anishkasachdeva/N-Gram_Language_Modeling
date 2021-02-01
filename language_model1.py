import pprint, os , sys, pprint, math, re, random


def tokenize(ip_text):
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

    return unigram_map,bigram_map,trigram_map,fourgram_map


# def witten_bell_smoothing(a, b, c, d, unigram_map, bigram_map, trigram_map, fourgram_map):
#     partial_probability = 0

#     if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:
#         pass
#     else:
#         pass


def kneser_ney_smoothing(a, b, c, d, unigram_map, bigram_map, trigram_map, fourgram_map):
    discounting_factor = 0.75
    partial_probability = 0

    if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:
    #-------------------------------------------------Calculation of P(d|abc)
        
        Ckn_abcd = 0
        Ckn_abc = 0
        # if a in fourgram_map and b in fourgram_map[a] and c in fourgram_map[a][b] and d in fourgram_map[a][b][c]:
        if d in fourgram_map[a][b][c]:
            Ckn_abcd = fourgram_map[a][b][c][d]
        # if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:
        Ckn_abc = trigram_map[a][b][c]
        first_term_1 = float(max(Ckn_abcd - discounting_factor, 0))/float(Ckn_abc)

        num_1 = 0
        deno_1 = 0
        # if a in fourgram_map and b in fourgram_map[a] and c in fourgram_map[a][b]:
        num_1 = len(fourgram_map[a][b][c])
        # if a in trigram_map and b in trigram_map[a] and c in trigram_map[a][b]:
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
        # if b in trigram_map and c in trigram_map[b]:
        num_2 = len(trigram_map[b][c])
        # if b in bigram_map and c in bigram_map[b]:
        deno_2 = bigram_map[b][c]
        # lambda_bc = (float(discounting_factor)/float(deno_2))*float(num_2)
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
        # if c in bigram_map:
        num_3 = len(bigram_map[c])
        # if c in unigram_map:
        deno_3 = unigram_map[c]
        lambda_c = float(discounting_factor * num_3)/float(deno_3)

        #-------------------------------------------------Calculation of P(d|phi)

        CCn_phi_d = 0
        CCn_phi = 0

        for i in bigram_map:
            if d in bigram_map[i]:
                CCn_phi_d += 1
        for i in bigram_map:
            CCn_phi = len(bigram_map[i])
        first_term_4 = float(max(CCn_phi_d - discounting_factor,0))/float(CCn_phi)

        num_4 = 0
        deno_4 = 0
        num_4 = len(unigram_map)
        for i in unigram_map:
            deno_4 = unigram_map[i]
        lambda_phi = float(discounting_factor * num_4) / float(deno_4)
        last_term = float(lambda_phi)/float(num_4)

        #-------------------------------------------------Calculation of Partial Probability

        partial_probability = (first_term_1 + lambda_abc * (first_term_2 + lambda_bc * (first_term_3 + lambda_c * (first_term_4 + last_term))))
        return math.log(partial_probability)
        
    else:
        lambd = (float(discounting_factor)/float(sum(unigram_map.values())))*len(unigram_map)
        
        fourgrams_variety = 0
        for i in fourgram_map:
            for j in fourgram_map[i]:
                for k in fourgram_map[i][j]:
                    fourgrams_variety += len(fourgram_map[i][j][k])
        
        partial_probability = float(lambd)/float(fourgrams_variety)
        return math.log(partial_probability)

    return partial_probability


def calculate_perplexity_of_sentence(probability, n):
    return (probability**(1/float(n)))


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


def file_open():
    f1 = open("2018101112-LM1-train-perplexity.txt", "w")
    f2 = open("2018101112-LM1-test-perplexity.txt", "w")
    f3 = open("2018101112-LM2-train-perplexity.txt", "w")
    f4 = open("2018101112-LM2-test-perplexity.txt", "w")
    f5 = open("2018101112-LM3-train-perplexity.txt", "w")
    f6 = open("2018101112-LM3-test-perplexity.txt", "w")
    f7 = open("2018101112-LM4-train-perplexity.txt", "w")
    f8 = open("2018101112-LM4-test-perplexity.txt", "w")
    return f1,f2,f3,f4,f5,f6,f7,f8


def file_close(f1,f2,f3,f4,f5,f6,f7,f8):
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()
    f7.close()
    f8.close()


#--------------------------------------------------------------------------------> System input by the user
smoothing_technique = sys.argv[1]
corpus = sys.argv[2]

if os.path.exists(corpus):
    while True:
        input_sen = input("input sentence : ")
        ip_file = open(corpus,"r")
        ip_text_train = ip_file.read()
        tokens = tokenize(ip_text_train)
        input_sentence = tokenize(input_sen)

        train = []
        test = []
        # random.shuffle(tokens)
        for i in range(5):
            test.append(tokens[i])
        
        for i in range(5,len(tokens)):
            train.append(tokens[i])

        unigram_map, bigram_map, trigram_map, fourgram_map = mapsFormatation(train)
        
        #---------------------------------------------------------------------------------------> Started file writing part
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
        if smoothing_technique == 'k'or smoothing_technique == 'K':

            for i in range(len(test)):
                # print(test[i])
                # partial_probability_list = []
                final_probability_of_sentence = 0
                # sentence = ""
                for j in range(3,len(test[i])):
                    # sentence += test[i][j] + " "
                    a = test[i][j-3]
                    b = test[i][j-2]
                    c = test[i][j-1]
                    d = test[i][j]
                    partial_probability_of_sentence = kneser_ney_smoothing(a, b, c, d, unigram_map, bigram_map, trigram_map, fourgram_map)

                    final_probability_of_sentence += partial_probability_of_sentence

                # partial_probability_list.append(partial_probability)
                final_probability_of_sentence = (final_probability_of_sentence)
                # perplexity_of_sentence = calculate_perplexity_of_sentence(final_probability_of_sentence, len(test[i]) - 3)
                print("Probability of sentence ", final_probability_of_sentence)
                # print("perplexity of sentence ", perplexity_of_sentence)
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        elif smoothing_technique == 'w' or smoothing_technique == 'W':
            pass
        else:
            print("Wrong Smoothing Technique. Please try again!")
else:
    print("Wrong File Name. Please try again!")


# log probability ?
  # pp1 = pprint.PrettyPrinter(indent=4)
        # pp1.pprint(test)