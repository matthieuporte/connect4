from connect4 import *

play(7, 6)

### minmax
"""
1 - get valid locations DONE
2 - check if it's the end of the board or max depth
2.1 - to check whether it is the end of the board you need to the function winning_move that tells
you if someone has one : go over the whole board (again) and check is there is a 4 e connection.
It is the end of the board if either a player has won OR if the board is full
3 - if it is the case return the value of the present board
4 - if it is not then we get real with minmax
4.1 - set the value to the lowest/highest (depending whether it is the maximising player or not)
4.2 - for every playable column make a copy, drop a piece and call minmax with this board copied
4.3 - once the recursion is done we store the value in a variable, if it is bigger/smaller that the value 
we already had set then we can modify it, and the column as well
4.4 - we can also do an alpha beta optimisation, beta is set with the minimiser, it starts at +infinity 
and then is set to the minimal value between the min value found when calling the minimiser and it's value
The same is done with alpha (except that it starts at -infinity and we take the max)
Now if at any time alpha>=beta you can stop searching here, the value will not be interesting
If you want to get a better understanding this website is great :
https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
"""


### board evalutation
"""
two functions
1 - the first function gives a score to a 4 elements array, it checks possibilities : 
this means 4 piece of your color is very good
4 piece of the other color is very bad
3 piece of your color and 1 empty cell or 2 and 2 is good
same for the other player but the other way round.
2 - This second function is a bit harder, we need to find thoses 4 elements arrays mentioned 
in the previous function.
we will go over every cell, upwards, to the left, diagonaly upwards and, starting from the top  
"""









##### exercices ##### 

#winning move () check whether the pawn that was just played

#get valid locations # done

#get next open row # done
 
#is valid location #done

#board copy # done

#drop piece # done

#heristique 

#minmax