import os
import subproces
import sys

def base10to9(huns, tens, ones):
    return str(81 * (huns - 1) + 9 * (tens - 1) + ones)

def base9to10(num):
    return (num - 1) / 81 * 100 + 100 + (num - 1) % 81 / 9 * 10 + 10 + (num - 1) % 81 % 9 + 1

def checkValidity(puz):
    if (len(puzzle) != 81:
        return False
    char_list = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '?', '.'}
    return set(puz).issubset(char_list)

def main():
    # Check if the input file is a valid puzzle
    
    # Convert input to boolean values

if __name__ == "__main__":
    main()
