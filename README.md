# Solving_sudoku
I am trying to compare the cost of time for each approach to solve sudoku. It proves the importance of efficiency of algorithms.

Some approachs are never gonna solve a large size problem (I mean, at least for several hunderds of years), some other approachs can solve a really large problem in a few minutes.

# Half Naive Approach
It generates a list of possibilities for each empty box at first, then try those possibilities one by one.

The efficiency is really low, because it spends a lot of time trying a large amount of ridiculous attempts.

For example, there're three empty box, each of them has 3 possibilities. (It's just a example, it's not gonna happen.) This program would generate a list of possibilities like [ [ 0, 0, [1, 2, 3] ], [ 0, 1, [1, 2, 3] ], [ 0, 2, [1, 2, 3] ] ]. Containing each empty box in a list, where the first two elements represents the location of the box (row number & column number), the third element represents the possible value for this particular box. In thsi case, the main function would generate a solution like [0, 0, 0], it means to fill every empty box with the solution of 0 indexing, which is the first element in the possibility list, 1.

Then, the first box is fill by 1, as well as the second and third box. After passing the modified board to the check function, the main function would know that it's not a correct answer and generates a new solution.

The solution would generates like this:
[0, 0, 0]
[1, 0, 0]
[2, 0, 0]
[0, 1, 0]
[1, 1, 0]
[2, 1, 0]
[0, 2, 0]
[1, 2, 0]
[2, 2, 0]
[0, 3, 0]
......

The frequency is really low, because it generaetes a lot of ridiculous solutions. For example, when the box [0, 0] was filled by the 1, the box [0, 1] shoul have a different value because they're on the same column. Then [0, 2] should have no choice but have to choose the one that the others didn't choosed, because there shouldn't be duplicate numbers on the same row/column/square.

However it's capable for solving small size problems (like 25 empty box). 
My MacBook solves the answer for 25 empty box in 1 seconds.

# Smarter Approach
A fill_information function was added in this approach. The program would try to fill in the blanks that are very obvious, bofore it tries to crack by attempting every possibilities. 

The fill_information will first fill thost blanks which has only one possibilities (by checking their neighbour), if the modification made some other blanks that has more than one possibilities reduced their problem size to just one possibilities, loop the whole process, until there're no more informations could be fill by their neighbour.

In most cases, it shorts the problem size really quickly and performs very fast. It solves the same problem for 'Half naive approach' in just 0.04 seconds.

# A Lot Smarter
Using a function call try_attempt to replace the old main function. In this way, the problem size is significantily reduced.

In general, after trying to fill the obvious informations in the blanks, it starts to try putting a number (from the possibility list) in one of the empty box, then refresh the possibility list. And try putting another number in another empty box...... until it detects there's mistakes (detects empty possibilit list for any unfilled box or detects duplicated numbers). When there's mistake detected, the recursive function goes back and change the value.....

It's way more faster because it doesn't try as much attempts as the 'Smarter Approach' and 'Half Naive Approach', and also detects mistakes before it the mistake happens.

# Coloured Edition
Add colors to the 'A Lot Smarter' approach. Original numbers would display as red, filled boxes would display as green.

# BOSS
It's faster than the 'A Lot Smarter' approach. It tries to fill the blank every time the attemps happens, which saves a lot of unnecessary attempts.

# SUPER
It's faster for some complicated problems but slower for some simple problems.
This approach will sort the possibility list by the length (numbers of items on the list), and then do the attemp. For those complicated (large size) problems, it would save a lot of time on attempting. Because it does the simple work first, at the same time it reduces the amount of calculation before it detects error. Having an effect that it tries fewer attempts than the BOSS solution for larger size problems.

The sorting part is based on merge sort, which is a really fast way to rearrange the possibility list. The additional functions for this approach is on the  sort_list.py.
