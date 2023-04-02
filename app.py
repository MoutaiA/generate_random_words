import random
import numpy as np
from nltk.corpus import words
import string
from flask import Flask, jsonify

app = Flask(__name__)

words_list = words.words()

MIN_LEN = 3
MAX_LEN = len(max(words_list, key = len))

@app.route('/fake')
def generate_word():
    """
    Generate a total random word
    """
    word_len = random.randint(MIN_LEN, MAX_LEN)
    letter_freqs = np.zeros((word_len, 26))

    for word in words_list:
        if len(word) == word_len:
            for i, letter in enumerate(word):
                letter_freqs[i, ord(letter.lower()) - ord('a')] += 1

    # Normalize frequencies to probabilities
    letter_probs = letter_freqs / np.sum(letter_freqs, axis=1, keepdims=True)

    # Generate new word using Markov chain
    word = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(0, 25)))
    for i in range(1, word_len):
        prev_letter = word[i-1]
        probs = letter_probs[i, :]
        next_letter = chr(ord('a') + np.random.choice(26, p=probs))
        word += next_letter

    return jsonify({ 'word': word })

@app.route('/word')
def get_word():
    """
    Get a word among the pool of words available in the nltk corpus
    """
    word = words_list[random.randint(0, len(words_list))]
    return jsonify({ 'word': word })

if __name__ == '__main__':
    app.run()
