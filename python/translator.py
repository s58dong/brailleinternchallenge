""" Hiya there! My name is Stephen Dong. I am a 1A Computer Engineering student at the University of Waterloo.
I put a ton of effort into making this. There were a lot of edge cases that I had to consider. Hoping this meets 
the criteria! :)
email: s58dong@uwaterloo.ca """

import sys

# create an array that stores all the different types of letters and numbers and special characters in the alphabet
eng_to_braille = {
    # these are for the letters
    'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..',
    'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..',
    'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.',
    'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.',
    'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO', 'y': 'OO.OOO',
    'z': 'O..OOO', ' ': '......',
    # these are for the numbers
    '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..',
    '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...', '0': '.OOO..',
    # these are for the special characters
    'capital': '.....O', 'number': '.O.OOO',
}

# because the mappings for numbers and alpha letters are the same, we need to create SEPARATE mappings for alphabet and numbers
braille_to_eng_dict = {v: k for k, v in eng_to_braille.items() if (k.isalpha() or k.isspace())}
number_to_eng_dict = {v: k for k, v in eng_to_braille.items() if (k.isdigit() or k.isspace())}

# function to check if input is Braille
def is_braille(input_string):
    if len(input_string) % 6 != 0:
        return False  # because braille comes in combos of 6, it should be fully divisible by 6 too
    return all(c in "O." for c in input_string) # the function all only returns true if everything in it is also true
    #c will iterate through all the characters in the input string and see if each character belongs in "0."
    # since braille is only 0s and periods, it will only return true if they are all 0s or periods

# the function will convert english to braille specifically
def eng_to_b(eng_str):
    # set the output string to an empty array we'll be adding to
    braille_output = []
    number_mode = False  # track if we're currently in number mode

    # this will iterate through every string inthe english string
    for char in eng_str:
        if char.isdigit():
            # if we encounter a digit, we need to check if we are in number mode
            if not number_mode:
                # append the "number follows" indicator before the first number in a sequence
                braille_output.append(eng_to_braille['number'])
                number_mode = True  # set the number mode to true
            # now we just append the actual braille code
            braille_output.append(eng_to_braille[char])
        elif char.isalpha():
            # if it is a letter, we reset the number mode to false
            number_mode = False
            # two cases if the character is a letter: capital or non-capital
            if char.isupper():
                #if capital then ALWAYS append the "capital follows" first
                braille_output.append(eng_to_braille['capital'])
            # add the braille conversion for the letter
            braille_output.append(eng_to_braille[char.lower()])
        elif char == ' ':
            #if its a space, reset number mode
            number_mode = False
            # this adds the Braille conversion for space
            braille_output.append(eng_to_braille[char])

    #returns the finished braille string
    return ''.join(braille_output)

# this function right here will turn braille back into english
def braille_to_eng(braille_str):
    #create an empty array to hold characters
    eng_output = []
    
    #extract braille codes and creates a new index in the array for every 6 characters (length of braille code)
    braille_list = [braille_str[i:i + 6] for i in range(0, len(braille_str), 6)]
    
    # initialize the capital and number modes
    capital_mode = False
    number_mode = False

    for braille_char in braille_list:
        #this checks for capital letters
        if braille_char == '.....O':
            capital_mode = True
            continue
        #checks for numbers
        elif braille_char == '.O.OOO':
            number_mode = True
            continue
        # checks for spaces
        elif braille_char == '......':
            # automatically appends a space
            eng_output.append(' ')
            # after a space, we dont know what the next character will be so we reset both states
            number_mode = False
            capital_mode = False
            continue

        # here we will start to analyze the braille code
        if braille_char in braille_to_eng_dict:
            # check for number
            if number_mode:
                # get the number from the number braille to english dictionary
                char = number_to_eng_dict[braille_char]
                eng_output.append(char)  # add the number to the output
            else:
                # get the letter from the letter braille to english dictionary
                char = braille_to_eng_dict[braille_char]
                # here we check if its a capital
                if capital_mode and char.isalpha():
                    eng_output.append(char.upper()) 
                    capital_mode = False  # reset the capital state for the next letter
                else:
                    # this just adds a regular lower case letter
                    eng_output.append(char)
        else:
            eng_output.append('?')  # for debugging

    # joins the string we created and returns it
    return ''.join(eng_output)

# this is the main function where we'll test our work :D
def main():
    # if the user enters nothing we have to debug and tell them to actually enter something
    if len(sys.argv) < 2:
        print("Please provide an input string to translate!")
        return
    
    #we'll take what the user enters as our input string
    input_string = ' '.join(sys.argv[1:])
    # if its braille, we use the braille to english function
    if is_braille(input_string):
        print(braille_to_eng(input_string)) #print the returned string
    # if its english we do the opposite
    else:
        print(eng_to_b(input_string))

# automatically runs main
if __name__ == "__main__":
    main()
