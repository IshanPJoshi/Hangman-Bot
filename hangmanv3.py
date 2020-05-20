#Hangman Bot v3 by Ishan Joshi

import string
import operator
import json

def initialize():
    word = input("Give me a word. I promise I won't cheat ;)\n")
    file = "./words_dictionary.json"
    with open(file) as json_file:
        json_data = json_file.read()
        data = json.loads(json_data)
    word_list = list(data.keys())
    #word_list = [x.lower() for x in word_list]
    return(word, word_list)

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
    
def main():
    word, word_list = initialize()
    print("Alright, leave it to me!\n")

    word_length = len(word)
    guessed_letters = []
    tries_left = 10
    word_list = [ x for x in word_list if len(x) == word_length ]
    letters_of_word = list(word)
    guessed_word = [' ']*word_length


    while(tries_left and word_list != [] and not letters_of_word==guessed_word):
        next = nextGuess(word_list, guessed_letters)
        guess_letter = next[0]
        guessed_letters.append(guess_letter)
        print("I'm guessing,", guess_letter, "because I found ", next[1], "instances of it")
        if (guess_letter in letters_of_word):
            print(guess_letter, "was in the word")
            pos = []
            for i in range(word_length): #update word
                if letters_of_word[i] == guess_letter:
                    pos.append(i)
                    guessed_word[i] = guess_letter
            print 
            word_list = constrainWordPosition(word_list, guess_letter, pos)
        else:
            tries_left-=1
            print("OOF, looks like there was no", guess_letter)
            word_list = removeLetter(guess_letter, word_list)

        print("KNOWN LETTERS: ", guessed_word)

    if (word_list == []):
        print("It seems I'm not familiar with that word...")
        print("This means you either misspelt the word or I'm not familiar with the form")
        print("Make sure it's spelled correctly and try put it in singular form (i.e no punctuation, plurals, etc)")

    elif (tries_left == 0):
        print("Guess I lost :(")
    else:
        print("Looks like guessed the word!", guessed_word)
        print("I had: ", tries_left, "tries left")

if __name__ == "__main__":
    main()



