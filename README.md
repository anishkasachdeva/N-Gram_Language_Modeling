## Introduction to NLP - Assignment 1 
### Language-Modelling
---
##### Anishka Sachdeva (2018101112)
###### 1st February, 2021
---
## Steps to execute the code
python3 language_model.py <smoothing_type> <path_corpus>

###### smoothing_type = k for Kneser Ney Smoothing and

###### smoothing_type = w for Witten Bell Smoothing
---
## Files generated

Perplexity is calculated in the following:
1. The corpus is divided into test set and training set using random.shuffle.
2. Then the language model is created on training test.
3. Then each sentence in the test set is evaluated.
4. Probability of each sentence is calculated by the two smoothing methods.
5. Then each probability is written in the file along with the "tokenized sentence".
6. At last the average perplexity score is put in the file.
7. Perplexity is calculated using the following formula : 
    1. float(1)/float(math.exp(float(probability)/float(n)))
    2. Here probability = probablity of each sentence in the test set.
        1. Probability of each sentence = exp(math.log(p1) + math.log(p2) + math.log(p3) + .... + math.log(pN)) 
    3. Here n =  length(sentence) - 3
