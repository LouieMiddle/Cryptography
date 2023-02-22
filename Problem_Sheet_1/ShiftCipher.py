import collections

from math import log


def rotated(n: int):
    """
    Returns a rotated letter if parameter is greater than 26
    """
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    if n >= 26:
        n %= 26
    return ALPHABET[n:26] + ALPHABET[:n]


def caesar_decrypt(text: str, key: int) -> str:
    """
    Returns a decryption of parameter text and key
    """
    text = text.lower()
    key_to_zero = str.maketrans(rotated(key), rotated(0))
    return text.translate(key_to_zero)


def difference(a: str, b: str) -> int:
    a, b = a.lower(), b.lower()
    return ord(b) - ord(a)


def check_string_lengths(lst):
    # Count the number of strings with a length of 1 character
    count = sum(1 for s in lst if len(s) == 1)

    # Calculate the percentage of strings with a length of 1 character
    percentage = count / len(lst)

    # Return False if the percentage is greater than 30%, otherwise return True
    if percentage > 0.25:
        return True
    else:
        return False


def english_test(wordlist: "sequence of valid english words", text: str) -> bool:
    """
    english_test checks that every word in `text` is in `wordlist`
    """
    words = text.split()
    if check_string_lengths(words):
        return False
    return all(word in wordlist for word in words)


def bruteforce_caeser(text: str) -> str:
    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    # https://en.wikipedia.org/wiki/Zipf%27s_law
    words = open("../wordlist.txt").read().split()
    word_cost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
    max_word = max(len(x) for x in words)

    # ordered by most to the least common
    c = collections.Counter(text)
    most_common = c.most_common()

    for ch, _ in most_common:
        diff = difference('e', ch)
        plaintext = caesar_decrypt(text, diff)
        plaintext = infer_spaces(plaintext, word_cost, max_word)
        if english_test(words, plaintext):
            return plaintext


def infer_spaces(s, word_cost, max_word):
    """
    Uses dynamic programming to infer the location of spaces in a string
    without spaces.
    """

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - max_word):i]))
        return min((c + word_cost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k:i])
        i -= k

    return " ".join(reversed(out))


if __name__ == '__main__':
    cipher_text = "WKHPDJLFZRUGVDUHVTXHDPLVKRVVLIUDJH"
    plain_text = bruteforce_caeser(cipher_text.lower())
    print(plain_text)
