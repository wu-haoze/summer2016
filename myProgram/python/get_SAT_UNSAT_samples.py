
import os
import sys
import random
import copy

"""
This file is used to obtain training data.
"""
def main():
    content = []
    original_cnf = sys.argv[1]
    with open(original_cnf, 'r') as in_file: # Read a dimacs file
        for line in in_file:
            if len(content) == 1:
                content.append(line.split())
            elif len(content) >= 2:
                content.append(map(int, line.split()))
            else:
                content.append(line)
    with open(original_cnf.split(".")[0] + ".txt", 'r') as in_file:
        contentS = in_file.readlines()
    if "UNSAT" in contentS[0]:
        UNSAT_original_formula(original_cnf, content)
    elif "INDET" in contentS[0]:
        pass
    else: 
        solution = map(int, contentS[1].split())
        write_UNSAT(original_cnf, copy.deepcopy(content))
#        write_SAT_file(original_cnf, content, solution[:-1])


def UNSAT_original_formula(original_cnf, content):
    return




def write_UNSAT(original_cnf, content):
    i = 1
    unsat_lit_file = original_cnf.split('.')[0]+ '-' + str(i) + ".ulit"
    while(os.path.isfile(unsat_lit_file)):
        print i
        with open(unsat_lit_file, 'r') as in_answer:
            first = in_answer.readline().split()
            second = in_answer.readline().split()
            if len(second) !=0 : 
                lits = map(int, first[: len(second) + 1])[1:]
            else:
                i += 1
                unsat_lit_file = original_cnf.split('.')[0]+ '-' + str(i) + ".ulit"
                continue
        new_content = copy.deepcopy(content)
        write_UNSAT_file(unsat_lit_file.split(".")[0], new_content, lits)
        i += 1
        unsat_lit_file = original_cnf.split('.')[0]+ '-' + str(i) + ".ulit"



def write_UNSAT_file(filename, content, lits):
    """
    Takes in a satisfiable formula, and takes in a wrong lits assignment, generates a .dimacs if the resulting formula does not contain empty clauses  
    """
    while len(lits) > 0:
        new_dimacs, lits = update_content(content, lits)
        content, lits = unit_propagation(new_dimacs, lits)
       #content, lits = shrink_formula(new_dimacs, lits)
    if not contains_empty(content):
        with open("u" + filename + ".dimacs", 'w') as out_file:
            out_file.write(content[0]) # The first line has change line itself
            for line in content[1:]:
                out_file.write(' '.join(map(str,line)) + "\n")


    


def write_SAT_file(original_cnf, in_content, solution):
    if len(solution) < 1:
        return
    new_dimacs, solution = update_content(in_content, solution)
    new_dimacs, solution = unit_propagation(new_dimacs, solution)
    new_dimacs, solution = shrink_formula(new_dimacs, solution)

    if len(original_cnf.split('-')) == 1:
        new_original_cnf = original_cnf.split('.')[0]+ '-' + "1.dimacs"
    else:
        new_original_cnf = original_cnf.split('-')[0]+ '-' + str (int (original_cnf.split('-')[1].split('.')[0]) + 1) + ".dimacs"

    with open(new_original_cnf, 'w') as out_file:
        out_file.write(new_dimacs[0])
        for line in new_dimacs[1:]:
            out_file.write(' '.join(map(str,line)) + "\n")
    with open(new_original_cnf.split('.')[0]+".txt", 'w') as out_file:
        out_file.write(" ".join(map(str, solution)) + "\n")

    write_SAT_file(new_original_cnf, new_dimacs, solution)


#---------------------------------------- Helper methods ----------------------------------------#

def update_content(content, solution):
    lit = solution[-1]
    solution.remove(lit)
    deleted_clause = 0
    new_dimacs = [content[0],[]]
    for line in content[2:]:
        if lit not in line:
            if -lit in line:
                line.remove(-lit)
            new_dimacs.append(line)
        else:
            deleted_clause += 1
    info = content[1]
    info[2] = int(info[2]) - 1
    info[3] = int(info[3]) - deleted_clause
    new_dimacs[1] = info  # update the number of clauses 
    for i in range(2, len(new_dimacs)):
        new_dimacs[i] = update_line(new_dimacs[i], abs(lit))
    solution = update_sol(solution, abs(lit))
    return new_dimacs, solution

def update_sol(solution, var):
    for i in range(len(solution)):
        if abs(solution[i]) > var:
            sign = solution[i] / abs(solution[i])
            solution[i] = sign * (abs(solution[i])-1)
    return solution

def update_line(line, var):
    """
    decrease the numbers of variables by 1
    """
    for i in range(len(line)):
        if abs(line[i]) > var:
            sign = line[i] / abs(line[i])
            line[i] = sign * (abs(line[i]) - 1)
    return line


def unit_propagation(content, solution):
    for i in range(2, len(content)):
        if len(content[i]) == 2:
            lit = content[i][0]
            deleted_clause = 0
            new_dimacs = [content[0],[]]
            for line in content[2:]:
                if lit not in line:
                    if -lit in line:
                        line.remove(-lit)
                    new_dimacs.append(line)
                else:
                    deleted_clause += 1
            for j in range(2, len(new_dimacs)):
                new_dimacs[j] = update_line(new_dimacs[j], abs(lit))
            if lit in solution:
                solution.remove(lit)
            else:
                print "can't find", lit
            solution = update_sol(solution, abs(lit))
            info = content[1]
            info[2] = int(info[2]) - 1
            info[3] = int(info[3]) - deleted_clause
            new_dimacs[1] = info # update the number of clauses
            return unit_propagation(new_dimacs, solution)
    return content, solution


def shrink_formula(content, solution):
    for ele in range(len(solution)+1)[1:]:
        if (not any(-ele in line for line in content[2:])) and (not any(ele in line for line in content[2:])):
            for i in range(2, len(content)):
                content[i] = update_line(content[i], abs(ele))
            try:
                if ele in solution:
                    solution.remove(ele)
                else:
                    solution.remove(-ele)
            except ValueError:
                print ""
            solution = update_sol(solution, abs(ele))
            content[1][2] -= 1
            return shrink_formula(content, solution)
    return content, solution


def contains_empty(content):
    for ele in content[2:]:
        if len(ele) == 1:
            return True
    return False



if __name__ == "__main__":
    main()
