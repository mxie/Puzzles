#!/usr/bin/env python
import sys
import re
import numpy
import string
import copy

#globals
images = []


# takes the lines in the images.txt file and grabs the keywords
def make_image_list(list):
    for line in list:
        pattern = re.compile(r"^\s*.*\.png\t(?P<words>.*)\s*$")
        result = pattern.search(line).group('words')
        words = result.split()
        for w in words:
            images.append(w)


# breaking down each phrase into an array of words
def break_down(test_lines):
    all_phrases = []
    for line in test_lines:
        line = line.lower()
        line = line.translate(None, string.punctuation)
        words = line.split()
        if words:           # in case of blank lines
            all_phrases.append(words)
    return all_phrases


# given a rebus expression, sum up the costs of the divided parts
def get_expr_cost(expr):
    expr = expr.translate(None, '()+-')
    words = expr.split()
    cost = 0
    for word in words:
        cost += get_str_cost(word)
    return cost


# given a string, calculuate its costs
def get_str_cost(str):
    cost = 0
    if not str.startswith(':'):
        for c in str:
            cost += get_cost(c)
    return cost


# returns the cost depending on type of character
def get_cost(char):
    if char in 'aeiou':
        return 1
    return 5


# find out if the given chars are in a word
# the 'sep' argument is for whether or not we care about order or just want
# check if these letters exist in the word at all as individuals (this
# can prevent certain letters from being accidentally removed)
def contains_chars(chars, cand, sep):
    if sep is True:
        str = r'|'
    else:
        str = r'.*'
    pattern = re.compile(str.join(list(chars)))
    result = pattern.search(cand)
    if result:
        return 1
    return 0


# calculates the edit distance between two words
def distance(goal, orig):
    n = len(goal) + 1
    m = len(orig) + 1
    # sets all entries to 0 in matrix
    table = numpy.zeros((n, m), dtype=numpy.int)

    # matrix set up for when comparing empty strings
    for i in range(1, n):
        table[i][0] = i
    for j in range(1, m):
        table[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            if goal[i-1] is orig[j-1]:          # if same, no edit
                table[i][j] = table[i-1][j-1]
            else:
                dist1 = 1 + table[i][j-1]       # insert letter into a
                dist2 = 1 + table[i-1][j]       # delete letter from a
                dist3 = 2 + table[i-1][j-1]     # delete & insert (subbing)

                table[i][j] = min(dist1, dist2, dist3)

    return table[n-1][m-1]


# makes an instance of LCS, which builds the table and figure out
# what letters differ and what are common between the words
def do_lcs(goal, orig):
    lcs = LCS(goal, orig)
    lcs.populate_diff()
    return lcs


# tries finding words that have images, returns the inserted/deleted o/w
# if the missing/extra letters form an image word itself, return that word,
# o/w see if there are any 2 words that could make up those letters
# worst case scenerio: give back those letters
def get_images(goal):
    results = []
    if (goal in images):
        return ':'+goal
    else:
        contains_goal = filter(lambda x: contains_chars(goal, x, False), images)
        lcs_list = [do_lcs(goal, image) for image in contains_goal]
        for lcs in lcs_list:
            left = lcs.orig                     # some word
            right = ''.join(lcs.deleted)        # letters to remove to get letters to get goal
            if right in images:
                results.append(':' + left + ' - :' + right)
        if not results:
            results.append(goal)
    return sorted(results, key=len)             # to list the shortest first


# main function hat goes out and finds the images
def generate_rebuses(word):
    # grab all the image words that have minimum edit distance with this word
    dists = [distance(word, image) for image in images]
    mapped_dists = dict(zip(images, dists))
    min_dist = min(dists)
    cands = filter(lambda x: mapped_dists[x] == min_dist, images)

    root = ''
    ins_result = ''
    del_result = ''
    cost = 1000
    # for each candidate "root" word, build LCS tables so that we can see
    # what letters are missing or need to be removed
    cands_lcs = [do_lcs(word, c) for c in cands]
    for lcs in cands_lcs:
        ins_cand = get_images(''.join(lcs.inserted))
        del_cand = get_images(''.join(lcs.deleted))
        change_cost = get_expr_cost(ins_cand[0]) + get_expr_cost(del_cand[0])
# START COMMENT TO GET ANSWER2
        if (change_cost < cost):
            cost = change_cost
            root = lcs.orig
            ins_result = ins_cand[0]
            del_result = del_cand[0]
# END COMMENT TO GET ANSWER2
# START UNCOMMENT TO GET ANSWER2
        if change_cost != 0:
            if not ins_cand[0].startswith(':') and del_cand[0].startswith(':'):
                ins_cand = try_again(''.join(ins_cand[0]))
                del_cand = del_cand[0]
            elif ins_cand[0].startswith(':') and not del_cand[0].startswith(':'):
                ins_cand = ins_cand[0]
                del_cand = try_again(''.join(del_cand[0]))
            else:
                ins_cand = try_again(''.join(ins_cand[0]))
                del_cand = try_again(''.join(del_cand[0]))
            new_cost = get_expr_cost(ins_cand) + get_expr_cost(del_cand)
            if new_cost < cost:
                root = lcs.orig
                ins_result = ins_cand
                del_result = del_cand
                cost = new_cost
        else:
            root = lcs.orig
            ins_result = ins_cand[0]
            del_result = del_cand[0]
            cost = 0
            break
# END UNCOMMENT TO GET ANSWER2

    result = ("\t:" + root + ' + (' + ins_result + ') - (' + del_result + ')')
    return (result, cost)


# a class to handle creating the table for longest common subsequence
# between 2 words and accessing the different properties of it
class LCS:
    def __init__(self, g, o):
        self.table = self.make_table(g, o)
        self.goal = g
        self.orig = o
        self.inserted = []
        self.deleted = []

    # builds up the table that calculates the longest common subsequence
    def make_table(self, a, b):
        # get dimensions of matrix
        n = len(a)+1
        m = len(b)+1
        # sets all entries to 0 in matrix
        table = numpy.zeros((n, m), dtype=numpy.int)
        for i in range(1, n):
            for j in range(1, m):
                if a[i-1] is b[j-1]:
                    table[i][j] = table[i-1][j-1]+1
                else:
                    table[i][j] = max(table[i][j-1], table[i-1][j])
        return table

    # returns the number of characters that represent the LCS
    def get_lcs_value(self):
        n = len(self.goal)
        m = len(self.orig)
        return self.table[n][m]

    # populates the lists of characters that were inserted/deleted (different)
    # between the two words
    def populate_diff(self):
        self.get_diff(len(self.goal), len(self.orig))

    # backtraces through the LCS table to find the letters that differ
    def get_diff(self, m, n):
        (g, o, t) = (self.goal, self.orig, self.table)
        # to account for the table being larger than the lengths of the strings
        x = m-1
        y = n-1

        # if the characters are the same, backtrack diagonally 1 spot
        if (m > 0 and n > 0 and g[x] is o[y]):
            self.get_diff(m-1, n-1)
        else:
            if n > 0 and (m == 0 or t[m][n-1] >= t[m-1][n]):
                self.deleted.insert(0, o[y])
                self.get_diff(m, n-1)
            elif m > 0 and (n == 0 or t[m][n-1] < t[m-1][n]):
                self.inserted.insert(0, g[x])
                self.get_diff(m-1, n)


## ONLY USED TO GET ANSWER2
# in case we couldn't find images the first time, we'll try again
# and go a little deeper in our search
def try_again(goal):
    more_cands = []
    max_lcs = 0
    min_cand_cost = get_str_cost(goal)
    images_copy = copy.copy(images)
    contains_goal = filter(lambda x: contains_chars(goal, x, False), images_copy)
    for cand in contains_goal:
        images_copy.remove(cand)
        no_goal = filter(lambda x: not contains_chars(goal, x, True) and contains_chars(x, cand, False), images_copy)
        if no_goal:
            mapped_lcs = [do_lcs(cand, n) for n in no_goal]
            cands = filter(lambda x: x.get_lcs_value() >= len(goal), mapped_lcs)
            for new_lcs in cands:
                lcs_value = new_lcs.get_lcs_value()
                right = new_lcs.orig
                for char in goal:
                    new_lcs.inserted.remove(char)
                new_cost = get_str_cost(''.join(new_lcs.inserted))
                if lcs_value > max_lcs and new_cost < min_cand_cost:
                    max_lcs = lcs_value
                    min_cand_cost = new_cost
                    more_cands.append(':' + cand + ' - :' + right + ' - ' + ''.join(new_lcs.inserted))
    if not more_cands:
        more_cands.append(goal)
    result = sorted(more_cands, key=len)
    return result[0]
    

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "Gimme the mappinz and tests!"
    else:
        # grabs all the lines of the images.txt file
        images_file = open(sys.argv[1])
        mappings = images_file.readlines()
        images_file.close()
        make_image_list(mappings)

        # grabs all the lines of the test cases file
        test_file = open(sys.argv[2])
        tests = test_file.readlines()
        test_file.close()
        phrases = break_down(tests)

        for phrase in phrases:
            print 'PHRASE:', phrase

            total_cost = 0
            for word in phrase:
                (rebus, cost) = generate_rebuses(word)
                total_cost += cost
                print rebus

            print 'TOTAL COST:', total_cost
