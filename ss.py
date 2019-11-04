# Encode a 9x9 Sudoku Puzzle in DIMACS format
# Output DIMACS file for MiniSAT
# Read in the output from MiniSAT and translate to Sudoku solution
# Output puzzle solution with pretty printing

import os
from subprocess import Popen, PIPE
import sys
import re

box_size = 3;

def base10ton(huns, tens, ones):
    return str((box_size ** 4) * (huns - 1) + (box_size ** 2) * (tens - 1) + ones)

def basento10(num):
    return (num - 1) / (box_size ** 4) * 100 + 100 + (num - 1) % (box_size ** 4) / (box_size ** 2) * 10 + 10 + (num - 1) % (box_size ** 4) % (box_size ** 2) + 1

def checkValidity(puz):
    if len(puz) != 81:
        print 'length != 81\n'
        return False
    char_list = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '?', '.'}
    return set(puz).issubset(char_list)
    
def makeValid(puz):
    print repr(puz)
    if len(puz) != box_size ** 4:
        print 'Invalid puzzle length!\n'
        quit()
    char_list = {'0', '*', '?', '.'}
    for i in range(0, box_size ** 2):
        char_list.add(str(i + 1))
    filter(char_list.__contains__, puz)
    return puz

def puzzlebool(output, puzzle):
    for i, c in enumerate(puzzle):
        if c.isdigit() and int(c) != 0:
            output.write(base10ton((i % (box_size ** 2) + 1), (i / (box_size ** 2) + 1), int(c)) + ' 0\n')

def cellrule(output):
    for i in range(1, box_size**6+1):
        if i % box_size**2 == 0:
            output.write(''.join((str(i) + ' 0\n')))
        else:
            output.write(str(i) + ' ')

def boxrule(output):
    # output rule for 3x3 box
    for i in range(1, box_size**2+1):
        for j in range(0, box_size):
            for k in range(0, box_size):
                for l in range(1, box_size+1):
                    for m in range(1, box_size+1):
                        for n in range (m+1, box_size+1):
                            output.write('-' + base10ton((box_size*j+l),(box_size*k+m),i))
                            output.write(' -' + base10ton((box_size*j+l),(box_size*k+n),i))
                            output.write(' 0\n')
    for i in range(1, box_size**2 + 1):
        for j in range(0, box_size):
            for k in range(0, box_size):
                for l in range(1, box_size + 1):
                    for m in range(1,box_size + 1):
                        for n in range(l+1, box_size + 1):
                            for o in range(1, box_size + 1):
                                output.write('-' + base10ton((box_size*j+l),(box_size*k+m),i))
                                output.write(' -' + base10ton((box_size*j+n),(box_size*k+o),i))
                                output.write(' 0\n')

def rowrule(output):
    for i in range(1,box_size**2 + 1):
        for j in range(1,box_size**2 + 1):
            for k in range(1,box_size**2):
                for l in range(k+1, box_size**2 + 1):
                    output.write('-' + base10ton(i,k,j))
                    output.write(' -' + base10ton(i,l,j))
                    output.write(' 0\n')

def colrule(output):
    for j in range(1, box_size**2 + 1):
        for k in range(1, box_size**2 + 1):
            for i in range (1, box_size ** 2):
                for l in range(i+1,box_size**2 + 1):
                    output.write('-' + base10ton(i,j,k))
                    output.write(' -' + base10ton(l,j,k))
                    output.write(' 0\n')

def getnumterms(puz):
    rv = 0
    for c in puz:
        if c.isdigit() and int(c) != 0:
            rv += 1
    return rv

def prettyprint(line):
    n = 0
    print ' '
    for i in range(1, (box_size**2 * 2) + 2):
        print '*',
    print '\n',
    # 3 boxes high
    for i in range(1, box_size + 1):
        # 3 rows per box
        for j in range(1, box_size + 1):
            # 3 boxes per row
            print '* ',
            for k in range(1, box_size + 1):
                # 3 cells per row per box
                for l in range (1, box_size + 1):  
                    print '{0:1d} '.format(line[n] % (box_size ** 2)),
                    n += 1
                print '* ',
            print '\n',
        for j in range(1, (box_size**2 * 2) + 2):
            print '*',
        print'\n',

def main():
    # Check if the input file is a valid puzzle
#    unknowns = {'*', '.', '?', '0'}
    if (len(sys.argv) != 2 and len(sys.argv) != 3):
        print "Usage: python ss.py <filename> [boxsize]\n"
        quit()
#    if len(sys.argv) == 3:
#        box_size = sys.argv[-1]
#   else:
#       box_size = 3
    
    f = open(sys.argv[-1], 'r')
    num = 1
    for line in f:
        indest = './Input/' + (sys.argv[-1]) + str(num) + '.txt'
        outdest = './Output/' + (sys.argv[-1]) + str(num) + '.txt'
        Input = open(indest, 'w')
        # read puzzle in one line & check validity
        line = line[:-1]
        if checkValidity(line) == False:
            quit()
        # translate to DIMACS
        Input.write('c DIMACS format for MiniSAT\n')
        Input.write('p cnf ' + str(box_size**6) + ' ' + str(8829+getnumterms(line)) + '\n')
        cellrule(Input)
        boxrule(Input)
        rowrule(Input)
        colrule(Input)
        puzzlebool(Input, line)
        Input.close()
        # submit to MiniSAT
        process = Popen(["./minisat", indest, outdest], stdin = PIPE, stdout = PIPE, stderr = PIPE)
        output, err = process.communicate(b"input passed into subprocess.Popen's stdin")
        retcode = process.returncode
        # read back output
        Output = open(outdest, 'r')
        if retcode == 10:
            # pretty printing of solution
            print 'Puzzle ' + str(num) + ' was solvable:\n'
            # Get second line of output
            s = Output.readline()
            s = Output.readline().split(' ')
            sol = []
            for i in s:
                if i.isdigit() and int(i) > 0:
                    sol.append(int(i))
            prettyprint(sol)
        elif retcode == 20:
            print 'Puzzle ' + str(num) + ' was not satisfiable\n\n'
        else:
            print 'ERROR: MiniSAT hates your input.  -150 HP.\n'
        # reformat and pretty print
        num += 1

if __name__ == "__main__":
    main()
