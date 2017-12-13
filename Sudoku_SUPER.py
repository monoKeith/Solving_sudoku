#import time
import time
import copy

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
                return False
    #Check each column
    for column_num in range(9):
        current_list = []
        for tmp in range(9):
            current_list.append(su_map[column_num][tmp])
        for num in range(1,10):
            if not num in current_list:
                return False
    #Check each square
    for sq_row in range(0,7,3):
        for sq_column in range(0,7,3):
            #Gererate a list contains the nine numbers in that particular square.
            current_list = []
            for sr in range(3):
                for sq in range(3):
                    current_list.append(su_map[sq_row + sr][sq_column + sq])
            for num in range(1,10):
                if not num in current_list:
                    return False
    #Return value if all
    return True

#This function will print out the state in terminal.
def print_map(su_map):
    print('  ========== S U D O K U ==========')
    for row_list in su_map:
        print('\t', end = '  ')
        for number in row_list:
            if number == 0:
                print(' ', end = ' ')
            else:
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
    candidate_dic = sort(candidate_dic)
    return candidate_dic

#Merge sort fot the candidate list!
#Sort function
def sort(source):
    if len(source) == 1 or source == []:
        return source
    left = sort(source[:len(source)//2])
    right = sort(source[len(source)//2 :])
    return merge(left,right)

#Merge function
def merge(left, right):
    l, r, result = 0, 0, []
    for times in range(len(left)+len(right)):
        if l != len(left) and r != len(right):
            if len(left[l][2]) > len(right[r][2]):
                result.append(right[r])
                r += 1
            else:
                result.append(left[l])
                l += 1
        elif l == len(left):
            result.append(right[r])
            r += 1
        elif r == len(right):
            result.append(left[l])
            l += 1
    return result

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
                break
        if modified == True:
            dictionary = generate_candidate(result_map)
    return result_map

#This function trys to fill blanks by guessing.
def try_attempt(last_map):
    su_map = copy.deepcopy(last_map)
    su_map = fill_information(su_map)
    #Generate candidates list.
    candidates = generate_candidate(su_map)
    #Check if there're possibility for each blank.
    if candidates == []:
        if check_answer(su_map):
            return su_map
        return False
    for candidate in candidates:
        if candidate[2] == []:
            return False
    #Attempt an answer for the blank.
    for answer in candidates[0][2]:
        su_map[candidates[0][0]][candidates[0][1]] = answer
        processing = try_attempt(su_map)
        if processing != False:
            return processing
    return False

#This function takes 2 arguments, previous map and final map, and it prints out the differences by using colour.
def colour_map(original_map, final_map):
    #from colorama import init
    print('  ========== S U D O K U ==========')
    for row_num in range(9):
        line = ''
        print('\t', end = ' ')
        for column_num in range(9):
            original_num = original_map[row_num][column_num]
            final_num = final_map[row_num][column_num]
            if original_num == final_num:
                line += (' \x1b[31m' + str(final_num))
            else:
                line += (' \x1b[36m' + str(final_num))
        print(line + '\x1b[0m')
    print('  =================================')

#Main function
def main():
    #Load files, and record the starting time.
    filename = input('Please input the name of the sudoku file:')
    starting_time = time.time()
    mapsu = load_file(filename)
    mapsu = generate_list(mapsu)
    ori_map = copy.deepcopy(mapsu)
    #Print out the original map.
    print_map(mapsu)
    #Try attempts
    mapsu = try_attempt(mapsu)
    #If the correst answer does exists, print it out.
    if mapsu != False:
        #Print out the time consume.
        print('  Finished in ', round((time.time() - starting_time), 10), 'seconds')
        colour_map(ori_map, mapsu)
    else:
        print("Can't find the answer for this question.")


#Call main function
main()
