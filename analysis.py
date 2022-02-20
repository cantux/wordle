#!/usr/bin/env python

from collections import defaultdict
import heapq

# most useful statistic

# find the most frequent letters
# find words that include most frequent letters

# find words that include certain chars
# find words that include chars in particular indeces

# pos_sim_g = defaultdict(dict)
import pprint

ord_a, ord_z = ord('a'), ord('z')
all_words = []
char_pos_dct = [[[] for p in range(5)] for c in range(26)]
letter_freqs = {}
starter_words = []

def pull_in_words(filename):
    with open(filename) as f:
        for curr_w in f:
            dont_skip = True
            norm_w = curr_w.lower()[:5]
            for c in norm_w:
                if not (ord_a <= ord(c) <= ord_z):
                    dont_skip = False
                    break
            if dont_skip:
                all_words.append([norm_w, 0])

def set_char_pos_dct():
    for ref_to_curr_w_and_score in all_words:
        for i in range(5):
            norm_c_idx = ord(ref_to_curr_w_and_score[0][i]) - ord_a
            if 0 <= norm_c_idx < 26:
                char_pos_dct[norm_c_idx][i].append(ref_to_curr_w_and_score)

def set_letter_freqs():
    for c_i, c in enumerate(char_pos_dct):
        word_count = 0
        for i in c:
            word_count += len(i)
        letter_freqs[chr(c_i + ord_a)] = word_count

    for k,v in sorted(list(letter_freqs.items()), key=lambda x: x[1], reverse=True):
        print(k + " " + str(v))

def set_word_scores():
    for i, (curr_w, score) in enumerate(all_words):
        all_words[i][1] = sum(letter_freqs[c] for c in set(curr_w))

def set_starter_words():
    hq = []
    heapq.heapify(hq)
    for w, score in all_words:
        heapq.heappush(hq, (score, w))
        if len(hq) > 20:
            heapq.heappop(hq)

    while hq:
        curr = heapq.heappop(hq)
        starter_words.append([curr[1], curr[0]])
    print(starter_words)

def satisfy_contain(candidate, should_contain):
    for c, exclude_indeces in should_contain.items():
        if c not in candidate:
            return False
        for ex in exclude_indeces:
            if candidate[ex] == c:
                return False
    return True

def satisfy_not_banned(candidate, banned_letters):
    for c in candidate:
        if c in banned_letters:
            return False
    return True

def find_next_best_guess(pos_hint, should_contain, banned_letters):
    best_cand = ["zzzzz", -1]
    if should_contain and not any([p_hint != "" for p_hint in pos_hint]):
        for c, idx_exc in should_contain.items():
            for i in range(5):
                if i not in idx_exc:
                    for candidate, w_s in char_pos_dct[ord(c) - ord_a][i]:
                        if satisfy_contain(candidate, should_contain) and satisfy_not_banned(candidate, banned_letters):
                            if best_cand[1] < w_s:
                                best_cand = [candidate, w_s]

    elif any([p_hint != "" for p_hint in pos_hint]):
        for p_i, c in enumerate(pos_hint):
            if c != "":
                for candidate, c_s in char_pos_dct[ord(c) - ord_a][p_i]:
                    candidate_fits_pos_hint = all([candidate[i] == h for i, h in enumerate(pos_hint) if h != ""])
                    if candidate_fits_pos_hint and satisfy_contain(candidate, should_contain) and satisfy_not_banned(candidate, banned_letters):
                        if best_cand[1] < c_s:
                            best_cand = [candidate, c_s]
    elif should_contain:
        for c, idx_exc in should_contain.items():
            for i in range(5):
                if i not in idx_exc: 
                    for candidate, c_s in char_pos_dct[c][i]:
                        if satisfy_not_banned(candidate, banned_letters):
                            if best_cand[1] < c_s:
                                best_cand = [candidate, c_s]
    elif banned_letters:
        for c in range(26):
            if chr(c + ord_a - 1) not in banned_letters:
                for i in range(5):
                    for candidate, c_s in char_pos_dct[c][i]:
                        contains_banned = False
                        for cand_c in candidate:
                            if cand_c in banned_letters:
                                contains_banned = True
                                break
                        if not contains_banned:
                            if best_cand[1] < c_s:
                                best_cand = [candidate, c_s]

    else:
        best_cand = starter_words[-1]
    return best_cand

def score(guess, word, pos_hint, should_contain, banned_letters):
    for i in range(5):
        if guess[i] == word[i]:
            pos_hint[i] = word[i]
        elif guess[i] in word:
            should_contain[guess[i]].add(i)
        else:
            banned_letters.add(guess[i])

def test():
    word = "tacit"
    pos_hint = ["", "", "", "", ""]
    should_contain = defaultdict(set)
    banned_letters = set()
    guess = find_next_best_guess(pos_hint, should_contain, banned_letters)
    guess_count = 1
    while guess[0] != word:
        print(guess)
        guess_count += 1
        score(guess[0], word, pos_hint, should_contain, banned_letters)
        print(pos_hint)
        print(should_contain)
        print(banned_letters)
        guess = find_next_best_guess(pos_hint, should_contain, banned_letters)
    
    print("found: -" + guess[0] + "- with score: " + str(guess[1]))
    print("found in " + str(guess_count) + " tries")
    return guess_count

if __name__ == "__main__":
    pull_in_words("5_let_words")
    set_char_pos_dct()
    set_letter_freqs()
    set_word_scores()
    set_starter_words()


#     pos_hint = ["a", "l", "o", "", ""]
#     should_contain = defaultdict(set)
#     banned_letters = set(['e', 'r', 's', 'b', 'd', 'g'])
#     should_contain['l'] = set([1])
#     should_contain['i'] = set([2])
#     print(pos_hint)
#     print(should_contain)
#     print(banned_letters)

#     guess = find_next_best_guess(pos_hint, should_contain, banned_letters)

#     print(guess)
    test()

