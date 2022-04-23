import math


def levenshtein_distance(string_1, string_2):
    length_1 = len(string_1)
    length_2 = len(string_2)
    matrix = [list(range(length_1 + 1))] + [[x] + length_1 * [0] for x in range(1, length_2 + 1)]

    for j, char_1 in enumerate(string_1, start=1):
        for i, char_2 in enumerate(string_2, start=1):
            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + (char_1 != char_2))
    return matrix[-1][-1]


def hamming_distance(string_1, string_2):
    if len(string_1) != len(string_2):
        return None
    return sum([char_1 != char_2 for char_1, char_2 in zip(string_1, string_2)])


def insert_delete_distance(string_1, string_2):
    length_1 = len(string_1)
    length_2 = len(string_2)
    matrix = [(length_1 + 1) * [0] for _ in range(length_2 + 1)]

    for j, char_1 in enumerate(string_1, start=1):
        for i, char_2 in enumerate(string_2, start=1):
            if char_1 == char_2:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j],
                                   matrix[i][j - 1])

    return abs(length_1 + length_2 - 2 * matrix[-1][-1])


def levenshtein_distance_improved(string_1, string_2, typos_dict):
    length_1 = len(string_1)
    length_2 = len(string_2)
    matrix = [list(range(length_1 + 1))] + [[x] + length_1 * [0] for x in range(1, length_2 + 1)]

    for j, char_1 in enumerate(string_1, start=1):
        for i, char_2 in enumerate(string_2, start=1):
            if char_1 != char_2:
                if char_1 in typos_dict.setdefault(char_2, "") or char_2 in typos_dict.setdefault(char_1, ""):
                    cost = 0.5
                else:
                    cost = 1
            else:
                cost = 0

            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + cost)
    return matrix[-1][-1]


def hamming_distance_improved(string_1, string_2, typos_dict):
    if len(string_1) != len(string_2):
        return None

    cost = 0
    for char_1, char_2 in zip(string_1, string_2):
        if char_1 != char_2:
            if char_1 in typos_dict.setdefault(char_2, "") or char_2 in typos_dict.setdefault(char_1, ""):
                cost += 0.5
            else:
                cost += 1

    return cost


typos = {"u": "yi", "f": "g", "h": "j", "o": "ip", "y": "ui", "g": "f", "j": "h", "p": "io", "i": "opy"}


def find_similar_word(string_1, words_alpha):
    if string_1 in words_alpha:
        return string_1

    best_fit = ""
    best_similarity = math.inf
    for string_alpha in words_alpha:
        similarity = levenshtein_distance_improved(string_1, string_alpha, typos)
        if similarity < best_similarity:
            best_fit = string_alpha
            best_similarity = similarity

    return best_fit


def correct_text():
    with open("words_alpha.txt", "r") as file_dictionary:
        dictionary = file_dictionary.read().splitlines()
    with open("text_raw.txt", "r") as file_read:
        text_raw = file_read.read().split()

    with open("words_corrected.txt", "w") as file_write:
        for word in text_raw:
            file_write.write(find_similar_word(word, dictionary))
            file_write.write(" ")


print('levenshtein_distance("hello world", "helllo would")')
print("distance: ", levenshtein_distance("hello world", "helllo would"), "\n")

print('hamming_distance("grey", "gray")')
print("distance: ", hamming_distance("grey", "gray"), "\n")

print('insert_delete_distance("color", "colour")')
print("distance: ", insert_delete_distance("color", "colour"), "\n")

print("Typos dictionary: ", typos, "\n")

print('levenshtein_distance_improved("jello world", "helllo would", typos)')
print("distance: ", levenshtein_distance_improved("jello world", "helllo would", typos), "\n")

print('hamming_distance_improved("hrey", "gray", typos)')
print("distance: ", hamming_distance_improved("frey", "gray", typos), "\n")


correct_text()

