#import time
import time

#This function can Read the map file and return it as a string
def load_file(filename):
    filevar = open(filename)
    ori_map = filevar.read()
    filevar.close()
    return ori_map

#This function will take the string as a argument and generate a map of all numbers in form of list of list.
def generate_list(su_map):
    su_map = su_map.replace('\n', ' ')
    su_map = su_map.split(' ')
    result = []
    if len(su_map) >= 81 :
        for height in range(9):
            width_list = []
            for width in range(9):
                digit = su_map[ (height * 9) + width ]
                if digit == '#':
                    width_list.append(0)
                else:
                    width_list.append(int(digit))
            result.append(width_list)
        return result

#This function will check if the sudoku is correct and return a bool value.
def check_answer(su_map):
    correct = True
    #Check each row
    for row_num in range(9):
        current_list = su_map[row_num]
        for num in range(1,10):
            if not num in current_list:
                correct = False
    #Check each column
    if correct:
        for column_num in range(9):
            current_list = []
            for tmp in range(9):
                current_list.append(su_map[column_num][tmp])
            for num in range(1,10):
                if not num in current_list:
                    correct = False
    #Check each square
    if correct:
        for sq_row in range(0,7,3):
            for sq_column in range(0,7,3):
                #Gererate a list contains the nine numbers in that particular square.
                current_list = []
                for sr in range(3):
                    for sq in range(3):
                        current_list.append(su_map[sq_row + sr][sq_column + sq])
                for num in range(1,10):
                    if not num in current_list:
                        correct = False
    #Return value
    return correct

#This function will print out the state in terminal.
def print_map(su_map):
    print('  ========== S U D O K U ==========')
    for row_list in su_map:
        print('\t', end = '  ')
        for number in row_list:
            print(number, end = ' ')
        print()
    print('  =================================')

#This function generates a list of candidate number for each blank box on the map.
def generate_candidate(su_map):
    candidate_dic = []
    for row in range(9):
        for column in range(9):
            #If the current box is empty, start to calculate candidates for this single box.
            if su_map[row][column] == 0:
                #List all the numbers that are impossible to be in the box in the no_consider_list.
                no_consider_list = []
                #Check impossible number from row
                for tmp in range(9):
                    checking_num = su_map[row][tmp]
                    if not (checking_num == 0 or (checking_num in no_consider_list)):
                        no_consider_list.append(checking_num)
                #Check impossible number from column
                for tmp in range(9):
                    checking_num = su_map[tmp][column]
                    if not (checking_num == 0 or (checking_num in no_consider_list)):
                        no_consider_list.append(checking_num)
                #Check impossible number from square
                starting_point = ((row//3)*3, (column//3)*3)
                square_list = []
                for sr in range(3):
                    for sq in range(3):
                        checking_num = su_map[starting_point[0] + sr][starting_point[1] + sq]
                        if not (checking_num == 0 or (checking_num in no_consider_list)):
                            no_consider_list.append(checking_num)
                #Add considerable numbers for this box to the candidate_dic
                considerable_num = []
                for considering_num in range(1,10):
                    if not considering_num in no_consider_list:
                        considerable_num.append(considering_num)
                candidate_dic.append([row,column,considerable_num])
    return candidate_dic

#This function generates a list that tells the maximum attempts for each box.
def max_attempts(dictionary):
    attempts = []
    for box in dictionary:
        attempts.append(len(box[2])-1)
    return attempts

#This function modifies the original map and return the new map.
def modify_su(su_map, dictionary, solution):
    case_count = 0
    for case in dictionary:
        su_map[case[0]][case[1]] = case[2][solution[case_count]]
        case_count += 1
    return su_map

#This function fills some blanks that are obviosily already had an answer.
def fill_information(su_map):
    modified, result_map, dictionary = True, su_map, generate_candidate(su_map)
    #If there're modifications during the fill_information section, run again, until there're no more to change.
    while modified:
        modified = False
        #If there are only one possible answer, fill the blank.
        for case in dictionary:
            if len(case[2]) == 1:
                result_map[case[0]][case[1]] = case[2][0]
                modified = True
        if modified == True:
            dictionary = generate_candidate(result_map)
    return result_map

#Main function
def main():
    starting_time = time.time()
    mapsu = load_file("map.dat")
    mapsu = generate_list(mapsu)
    print_map(mapsu)
    mapsu = fill_information(mapsu)
    dic = generate_candidate(mapsu)
    max_list = max_attempts(dic)
    #Init blank solution
    solution, digit = [], 0
    for i in range(len(max_list)):
        solution.append(0)
    length_calc = len(max_list) - 1
    #Start to try
    finding = True
    while finding:
        current_su = modify_su(mapsu, dic, solution)
        #Check
        new_candidate, wrong = generate_candidate(current_su), False
        for c_candidate in new_candidate:
            print(new_candidate)
            if c_candidate[2] == []:
                wrong = True
        if (not wrong) and check_answer(current_su):
            finding = False
        else:
            solution[digit] += 1
            #check
            chk = digit
            while solution[chk] > max_list[chk]:
                if chk != length_calc:
                    solution[chk + 1] += 1
                solution[chk] = 0
                chk += 1
    print('Answer Found!')
    print_map(current_su)
    print('Time consume is:', time.time() - starting_time, 'Seconds!')

#Call main function
main()
