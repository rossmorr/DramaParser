import random

import summary_functions

# to simulate the process of the article, this function returns the play
# as one large string

def get_play_as_string(play):
    play = summary_functions.remove_square_brackets(play)
    to_return = ""

    for the_line in play:
        if the_line.startswith("SCENE ") or the_line.startswith("ACT ")\
                or the_line.strip().rstrip('.').isupper() :
            continue
        for i, ch in enumerate(the_line):
            if ch.isalnum() or ch.isspace():
                to_return += ch
            elif ch == "’":
                if (0 < i < len(the_line)-1
                        and the_line[i-1].isalpha()
                        and the_line[i+1].isalpha()):
                    to_return += ch
            else:
                to_return += " "
    clean = " ".join(to_return.split())
    return clean


# Follows article logic, builds an array of 100 words, then goes through this array, and flips a coin for each
# word to thin it down, after this, for every round that has passed a coin is flipped when a word is either
# being entered into the list or when it has already been seen in the list, if at any point that coin is tails (0)
# the word is either not entered into the list or removed from it depending on if it was there.
# once all words are accounted for we use the formula length of list × 2^round to estimate the count

def unique_words_estimate(play):
    play = play.lower()
    play = play.split()
    l = []
    rnd = 0

    for word in play:
        if rnd == 0:
            if len(l) <100:
                if word not in l:
                    l.append(word)
            elif len(l) == 100:
                new_l = []
                for listed_word in l:
                    coin = random.randint(0, 1)
                    if coin ==0:
                        new_l.append(listed_word)
                l = new_l
                rnd = 1

        if rnd > 0:
            if word not in l and len(l) < 100:
                add_word = True
                for x in range(rnd):
                    coin = random.randint(0, 1)
                    if coin ==0:
                        add_word = False
                        break
                if add_word:
                    l.append(word)
                    if len(l) == 100:
                        new_l = []
                        for listed_word in l:
                            coin = random.randint(0, 1)
                            if coin ==0:
                                new_l.append(listed_word)
                        l = new_l
                        rnd += 1
                        continue
            elif word in l:
                for x in range(rnd):
                    coin = random.randint(0, 1)
                    if coin ==0:
                        if word in l:
                            l.remove(word)
                        break
                continue


            elif len(l) == 100:
                new_l = []
                for listed_word in l:
                    coin = random.randint(0, 1)
                    if coin ==0:
                        new_l.append(listed_word)
                l = new_l
                rnd +=1

    return len(l) * (2 ** rnd)