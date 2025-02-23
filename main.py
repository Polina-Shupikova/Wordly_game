import random

def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

DICT_GUESSING = load_dict('dictionary_english.txt')
ANSWERS = random.choice(DICT_GUESSING)

COLORS = ["", "green", "yellow", "gray", "red"]  # Add more colors if desired
def determine_color(ourword, letter, j):
    #letter = guess[j]
    if letter == ourword[j]:
        return COLORS[1]
    elif letter in ourword:
        return COLORS[2]
    return  COLORS[3]

def check_word(SECRET_WORD,text_fields,field_colors):
    allB = 0
    CLR = 3
    for r in range(ROWS):
        sumB = 0
        for c in range(COLS):
            b = request.form.get(f'text_field_{r}_{c}', "")
            if (b == SECRET_WORD[c]):
                sumB += 1
        allB = max(allB, sumB)
        print(ROWS, COLS, allB)
    for r in range(ROWS):
        for c in range(COLS):
            field_colors[r][c] = COLORS[0]
            text_fields[r][c] = ""
    if (allB == 5):
        # wellResult
        SECRET_WORD = "_WIN_"
        CLR = 1
    for c in range(COLS):
        text_fields[2][c] = SECRET_WORD[c]
        field_colors[2][c] = COLORS[CLR]

from flask import Flask, render_template, request
import random

app = Flask(__name__)

ROWS = 6
COLS = 5
SECRET_WORD = ANSWERS # Default secret word
VALID_KEYS = "QWERTYUIOPASDFGHJKLZXCVBNM" # Valid keys to type with the physical keyboard

@app.route('/', methods=['GET', 'POST'])
def index():
    global SECRET_WORD
    text_fields = [["" for _ in range(COLS)] for _ in range(ROWS)]
    field_colors = [["" for _ in range(COLS)] for _ in range(ROWS)] # Colors for the fields
    keyboard_colors = {} #New dictionary to hold the colors

    active_row = 0
    active_col = 0
    keyboard_colors = {}  # New dictionary to hold the colors

    if request.method == 'POST':
        # Retrieve all text field values
        for r in range(ROWS):
            for c in range(COLS):
                text_fields[r][c] = request.form.get(f'text_field_{r}_{c}', "")
                #Retrieve field color, or assign a blank string
                field_colors[r][c] = request.form.get(f'field_color_{r}_{c}', "")
                letter = text_fields[r][c]
                if (letter in VALID_KEYS) & (keyboard_colors.get(letter) != "green"):
                    keyboard_colors[letter] = field_colors[r][c]


        key_pressed = request.form.get('key', '')
        active_row = int(request.form.get('active_row', 0))
        active_col = int(request.form.get('active_col', 0))

        if key_pressed == 'NewWord':
            ANSWERS = random.choice(DICT_GUESSING)
            SECRET_WORD = request.form.get('new_word', ANSWERS).upper()  # Get new word from form
            keyboard_colors = {} # Reset the keyboard when a new word is added.
            active_col = 0
            active_row = 0
            for r in range(ROWS):
                for c in range(COLS):
                    field_colors[r][c] = COLORS[0]
                    text_fields[r][c] = ""
        elif key_pressed == 'Enter':
            check_word(SECRET_WORD,text_fields,field_colors)

        elif (key_pressed not in ('Enter', 'Space', 'NewWord', '')) & (active_row < ROWS) & (active_col < COLS):
            text_fields[active_row][active_col] += key_pressed
            #изменим цвет ячейки
            clr = determine_color(SECRET_WORD, key_pressed, active_col)
            field_colors[active_row][active_col] = clr #random.choice(COLORS)
            if (keyboard_colors.get(key_pressed) != "green"):
                keyboard_colors[key_pressed] = clr #Set colors to keyboard!

         # Check if the key pressed comes from physical keyboard, if is a valid key and game is not over

        # Move to next field, wrap around

        if key_pressed not in ('Enter', 'Space', 'NewWord', ''):
            active_col += 1
            if active_col == COLS:
                active_col = 0
                active_row += 1

    return render_template('index.html',
                           text_fields=text_fields,
                           field_colors=field_colors,
                           active_row=active_row,
                           active_col=active_col,
                           rows=ROWS,
                           cols=COLS,
                           colors=COLORS,
                           secret_word=SECRET_WORD,
                           keyboard_colors = keyboard_colors)

if __name__ == '__main__':
    app.run(debug=True)