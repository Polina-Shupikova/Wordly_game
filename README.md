# Wordle_game
Wordle_game is a Web app with a game based on wordle 
# The rules
The objective of the game is to guess the 5-letter word of the day in 6 tries or fewer. Think of a starter word – it can be any word as long as it is valid. Once you enter that first 5-letter word, the letters will be one of three colors:

Gray – Incorrect letter

Yellow – Correct letter in the incorrect spot

Green – Correct letter in the correct spot

Use these clues to get closer to the word of the day and eventually guess it within 6 tries! Keep in mind that there may be double letters in the word of the day. So, even if you have a green E, you may have another E hidden in the word that you haven’t guessed yet.
# Installation
start with installatin of librares 
```
pip install random

pip install flack
```
Don't forget to add a dictionary_english.txt file, it contains a list of words that will be used for choosing a secret word
# Additional information 
File dictionary_english.txt contains 2000 words.
If you want less words, you can cut some words out off there
Also you can uncomment line 93 in file Index.html 
```
<!--<p>Secret Word: {{ secret_word }}</p>-->
```
to get a secret word
