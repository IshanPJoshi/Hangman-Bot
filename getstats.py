import nltk
from nltk.corpus import words
import string
import operator
import json
import multiprocessing as mp
import threading 
import time
start = time.perf_counter()
def initialize():
    ready = "NO"
    #while(ready != "yes"):
    #    ready = input("Hey, wanna play a game of hangman? Enter Yes or No\n")
    #    ready = ready.lower()

    #print("\nAlright, dibs on guessing!\n")
    #word = input("Give me a word. I promise I won't cheat ;)\n")
    word_list =  words.words()
    word_list = [ x for x in word_list if '-' not in x ]
    #file = "./words_dictionary.json"
    #with open(file) as json_file:
    #    json_data = json_file.read()
    #    data = json.loads(json_data)
    #word_list = list(data.keys())
    word_list = [x.lower() for x in word_list]
    return(word_list)

def nextGuess(up_words, guessed_letters):
    letterlist = dict.fromkeys(string.ascii_lowercase, 0)

    for i in up_words:
        for j in i:
            letterlist[j]+=1
    
    dict1 = letterlist
    sortdict = sorted(dict1.items(), key=operator.itemgetter(1), reverse = True)
    count = 0
    for i in sortdict:
        if i[0] not in guessed_letters:
            break
        count+=1
    return sortdict[count]

def removeLetter(letter, word_list):
    updated_words = word_list
    up_words = [ x for x in updated_words if letter not in x ]
    return up_words

def constrainWordPosition(word_list, guess_letter, pos):
    up_words = word_list
    for i in pos:
        up_words = [ x for x in up_words if x[i] == guess_letter ]
    return(up_words)

def main(tries_left, word, word_list):
    word_length = len(word)
    guessed_letters = []
    word_list = [ x for x in word_list if len(x) == word_length ]
    letters_of_word = list(word)
    guessed_word = [' ']*word_length


    while(tries_left and word_list != [] and not letters_of_word==guessed_word):
        next = nextGuess(word_list, guessed_letters)
        guess_letter = next[0]
        guessed_letters.append(guess_letter)
        if (guess_letter in letters_of_word):
            pos = []
            for i in range(word_length): #update word
                if letters_of_word[i] == guess_letter:
                    pos.append(i)
                    guessed_word[i] = guess_letter
            word_list = constrainWordPosition(word_list, guess_letter, pos)
        else:
            tries_left-=1
            word_list = removeLetter(guess_letter, word_list)


    #if (word_list == []):
        #print("It seems I'm not familiar with that word...")
        #print("This means you either misspelt the word or I'm not familiar with the form")
        #print("Make sure it's spelled correctly and try put it in singular form (i.e no punctuation, plurals, etc)")

    if (tries_left == 0):
        print("Guess I lost :(")
        return word, False
    else:
        print("Looks like guessed the word!", guessed_word)
        #print("I had: ", tries_left, "tries left")
        return word, True

def define(word_list, thrd, num):
    results = []
    for word in thrd:
        results.append(main(6, word, word_list))
    with open("thread"+ num + ".txt", 'w') as f:
        for item in results:
            f.write(str(item))
    end = time.perf_counter()
    print(end-start)
def thread():
    word_list = initialize()
    pool = mp.Pool(mp.cpu_count())

    
    #eigth = len(word_list)//10
    #print(eigth)
    #thrd1 = word_list[:eigth//2]
    #thrd2 = word_list[eigth//2:eigth]

    #results = [pool.apply(define, args = (word_list, word_list[:eigth], "5"))]
    

    import random
    word_len = [ x for x in word_list if len(x) == 3 ]
    size = 1000
    sample = random.sample(word_len, size)

    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(main, [(6, word, word_list) for word in sample])
    pool.close()

    #results = []
    #for word in sample:
    #    results.append(main(10, word, word_list))

    truth = [ x for x in results if x[1] == True ]
    print(len(truth)/size)
   #with open("test" + ".txt", 'w') as f:
   #    for item in results:
   #        f.write(str(item)+"\n")
    end = time.perf_counter()
    print(end-start)

    #thrd3 = word_list[2*fourth: 3*fourth]
    #thrd4 = word_list[3*fourth:]
    #t1 = threading.Thread(target=define, args=[word_list, thrd1, "1"])
    #t2 = threading.Thread(target=define, args=[word_list, thrd2, "2"])
    #result1 = thread._start_new_thread(define, (word_list, thrd1))
    #result2 = thread._start_new_thread(define, (word_list, thrd1))
    #pool.close()
    #define(word_list, word_list[:eigth], "4")
    #t1.start()
    #t2.start()

    

    

if __name__ == "__main__":
    thread()
    