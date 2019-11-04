# Encode a 9x9 Sudoku Puzzle in DIMACS format
# Output DIMACS file for MiniSAT
# Read in the output from MiniSAT and translate to Sudoku solution
# Output solution with pretty printing

import os
import subprocess
import sys

def base10to9(huns, tens, ones):
    return str(81 * (huns - 1) + 9 * (tens - 1) + ones)

def base9to10(num):
    return (num - 1) / 81 * 100 + 100 + (num - 1) % 81 / 9 * 10 + 10 + (num - 1) % 81 % 9 + 1

def checkValidity(puz):
    if len(puz) != 81:
        return False
    char_list = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '?', '.'}
    return set(puz).issubset(char_list)

def puzzlebool(puzzle):
    rv = []
    for i, c in enumerate(puzzle):
        if c.isdigit() and int(c) != 0:
            rv.append(base10to9((i % 9), (i / 9 + 1), int(c)))
    return rv

def cellrule(output):
    for i in range(1, 730):
        if i % 9 == 0:
            output.write(''.join((str(i) + ' 0\n')))
        else:
            output.write(str(i) + ' ')

def boxrule(output):
    # output rule for 3x3 box
    for i in range(1, 730):
        if i % 81 == 0:
            output.write()

def rowrule(output):
    return

def colrule(output):
    return

def main():
    # Check if the input file is a valid puzzle
#    unknowns = {'*', '.', '?', '0'}
    if (len(sys.argv) != 2 and len(sys.argv) != 3):
        print "Usage: python ss.py <filename> [size]"
        quit()
#    if len(sys.argv) == 3:
#        size = sys.argv[-1]
#   else:
#       size = 9
    
    f = open(sys.argv[-2], 'r')
    outdest = './/Output/'.join(sys.argv[-2])
    out = open(outdest, 'w')
    for line in f:
        # read puzzle in one line & check validity
        if checkValidity(line) == False:
            print "Puzzle has invalid characters: ".join(line)
            quit()
        
        # translate to DIMACS
        singleterms = puzzlebool(line)
        out.write('c DIMACS format for MiniSAT\n')
        out.write('p cnf 729 ' + str(8829+len(singleterms)) + '\n')
        cellrule(out)
        boxrule(out)
        rowrule(out)
        colrule(out)
        
        # submit to MiniSAT
        # read back output
        # reformat and pretty print

if __name__ == "__main__":
    main()
