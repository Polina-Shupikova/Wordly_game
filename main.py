import random

def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

DICT_GUESSING = load_dict('dictionary_english.txt')
ANSWERS = random.choice(DICT_GUESSING)

COLORS = ["", "green", "yellow", "gray", "red"]  # colors for greed and buttons
def determine_color(ourword, letter, j):
    if letter == ourword[j]:
        return COLORS[1]
    elif letter in ourword:
        return COLORS[2]
    return  COLORS[3]

def check_word(word,text_fields,field_colors):
    allB = 0
    CLR = 3
    if text_fields[2][0] != "_":
        for r in range(ROWS):
            sumB = 0
            for c in range(COLS):
                b = request.form.get(f'text_field_{r}_{c}', "")
                if (b == word[c]):
                    sumB += 1
            allB = max(allB, sumB)
            print(ROWS, COLS, allB)
        for r in range(ROWS):
            for c in range(COLS):
                field_colors[r][c] = COLORS[0]
                text_fields[r][c] = ""
        if (allB == 5):
            # wellResult
            word = "_WIN_"
            CLR = 1
        for c in range(COLS):
            text_fields[2][c] = word[c]
            field_colors[2][c] = COLORS[CLR]

def set_letter(letter, clr, active_row, active_col, keyboard_colors, text_fields, field_colors):
    if (active_row < ROWS) & (active_col < COLS):
        text_fields[active_row][active_col] = letter
        field_colors[active_row][active_col] = clr
        if (keyboard_colors.get(letter) != clr):
            keyboard_colors[letter] = clr

def cleanAll(ROWS, COLS, text_fields, field_colors):
 for r in range(ROWS):
    for c in range(COLS):
        field_colors[r][c] = COLORS[0]
        text_fields[r][c] = ""

from flask import Flask, render_template, request
import random

app = Flask(__name__)

ROWS = 6
COLS = 5
VALID_KEYS = "QWERTYUIOPASDFGHJKLZXCVBNM" # letters

@app.route('/', methods=['GET', 'POST'])
def index():
    global ANSWERS
    text_fields = [["" for _ in range(COLS)] for _ in range(ROWS)]
    field_colors = [["" for _ in range(COLS)] for _ in range(ROWS)]
    keyboard_colors = {}

    active_row = 0
    active_col = 0
    keyboard_colors = {}

    if request.method == 'POST':
        # Retrieve all text field values
        for r in range(ROWS):
            for c in range(COLS):
                text_fields[r][c] = request.form.get(f'text_field_{r}_{c}', "")
                field_colors[r][c] = request.form.get(f'field_color_{r}_{c}', "")
                letter = text_fields[r][c]
                if (letter in VALID_KEYS) & (keyboard_colors.get(letter) != COLORS[1]):
                    keyboard_colors[letter] = field_colors[r][c]


        key_pressed = request.form.get('key', '')
        active_row = int(request.form.get('active_row', 0))
        active_col = int(request.form.get('active_col', 0))

        if key_pressed == 'NewWord':
            ANSWERS = random.choice(DICT_GUESSING)
            keyboard_colors = {}
            active_col = -1
            active_row = 0
            cleanAll(ROWS, COLS, text_fields, field_colors)
        elif key_pressed == 'Enter':
            check_word(ANSWERS,text_fields,field_colors)
            active_col = 10
            active_row = 10

        elif key_pressed == 'Chet':
            active_col = max(0,active_col)
            letter = ANSWERS[active_col]
            if (active_col >= 0) & (active_col < COLS) & (active_row >= 0) & (active_row < ROWS):
                set_letter(letter, COLORS[1], active_row, active_col, keyboard_colors, text_fields, field_colors)

        elif key_pressed in VALID_KEYS:
            active_col += 1
            if active_col == COLS:
                active_col = 0
                active_row += 1
            clr = determine_color(ANSWERS, key_pressed, active_col)#change colour
            if (active_col >= 0) & (active_col < COLS) & (active_row >= 0) & (active_row < ROWS):
                set_letter(key_pressed, clr, active_row, active_col, keyboard_colors, text_fields, field_colors)

    return render_template('index.html',
                           text_fields=text_fields,
                           field_colors=field_colors,
                           active_row=active_row,
                           active_col=active_col,
                           rows=ROWS,
                           cols=COLS,
                           colors=COLORS,
                           secret_word=ANSWERS,
                           keyboard_colors = keyboard_colors)

if __name__ == '__main__':
    app.run(debug=True)
