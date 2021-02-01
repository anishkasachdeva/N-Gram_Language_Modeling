## Introduction to NLP - Assignment 1 
### Language-Modelling
---
##### Anishka Sachdeva (2018101112)
###### 1st February, 2021
---
## Steps to execute the code :
python3 language_model.py <smoothing_type> <path_corpus>
###### smoothing_type = k for Kneser Ney Smoothing and
###### smoothing_type = w for Witten Bell Smoothing
---
TODO:
1. Handle lower-upper case ---------------------------------------->Done
2. Handle if empty sentence is given in input sentence ------------>Done
3. Handle if spaces are given in input sentence ------------------->
5. Discuss the edge case handling with Viksit in tokenization
6. Write README till tomorrow's work
7. Finish Perplexity and Smoothing

Unigram_map =   {
                    Unigram : c,
                    Unigram : c,
                    Unigram : c
                }


Bigram_map  =   {
                    Bigram :    {
                                    Bigram : c
                                }

                    Bigram :    {
                                    Bigram : c
                                }
                                
                    Bigram :    {
                                    Bigram : c
                                }
                } 


Trigram_map = {
                    Trigram :   {
                                    Trigram :   {
                                                    Trigrams : c
                                                }
                                }

                    Trigram :   {
                                    Trigram :   {
                                                    Trigrams : c
                                                }
                                }

                    Trigram :   {
                                    Trigram : {
                                                    Trigrams : c
                                                }
                                }
                }


Fourgram_map = {
                    Fourgram :  {
                                    Fourgram :  {
                                                    Fourgrams : {
                                                                    Fourgrams : c
                                                                }
                                                }
                                }   

                    Fourgram :  {
                                    Fourgram :  {
                                                    Fourgrams : {
                                                                    Fourgram : c
                                                                }
                                                }
                                }

                    Fourgram :  {
                                    Fourgram : {
                                                    Fourgrams : {
                                                                    Fourgram : c
                                                                }
                                                }
                                }
                }


