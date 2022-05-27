from typing import Tuple, List

def input_sudoku() -> List[List[int]]:
	sudoku= list()
	for _ in range(9):
		row = list(map(int, input().rstrip(" ").split(" ")))
		sudoku.append(row)
	return sudoku

def print_sudoku(sudoku:List[List[int]]) -> None:
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j], end = " ")
		print()

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	i = int((pos[0]+2)/3)
	j = int((pos[1]+2)/3)
	block = j+3*(i-1)
	return block

def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	BN = get_block_num(sudoku,pos)
	x = int(BN/3)
	x = 1 + (x)*3
	y = 1 + ((BN-1)%3)*3
	pos[0] -= x-1
	pos[1] -= y-1
	pos_in = pos[0]+(pos[1]-1)*3
	return pos_in


def get_block(sudoku:List[List[int]], x: int) -> List[int]:
	r1 = int((x-1)/3)
	r1 = 1 + r1*3
	c1 = 1 + ((x-1)%3)*3
	lst = []
	for i in range(3):
		for j in range(3):
			lst.append(sudoku[r1-1+i][c1-1+j])
	return lst
	

def get_row(sudoku:List[List[int]], i: int)-> List[int]:
	lst = []
	for n in range(9):
		lst.append(sudoku[i-1][n])
	return lst

def get_column(sudoku:List[List[int]], x: int)-> List[int]:
	lst = []
	for n in range(9):
		lst.append(sudoku[n][x-1])
	return lst

def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]:
	index = [-1,-1]
	for i in range(9):
		for j in range(9):
			if sudoku[i][j] == 0:
				index = [i+1,j+1]
				return index
	return index

def valid_list(lst: List[int])-> bool:
	for i in range(9):
		for j in range(i+1,9):
			if lst[i] == lst[j] and lst[i] != 0 :
				return False
	return True

def valid_sudoku(sudoku:List[List[int]])-> bool:
	for i in range(1,10):
		if valid_list(get_block(sudoku,i)) == False :
			return False
		if valid_list(get_row(sudoku,i)) == False :
			return False
		if valid_list(get_column(sudoku,i)) == False :
			return False
	return True


def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:
	ans = [0,0,0,0,0,0,0,0,0,0]
	BN = get_block_num(sudoku,pos)
	l1 = get_block(sudoku,BN)
	l2 = get_row(sudoku,pos[0])
	l3 = get_column(sudoku,pos[1])
	candid = []
	lst = l1+l2+l3
	for i in range(1,10):
		for x in lst:
			if i==x:
				ans[i]=1
	for i in range(1,10):
		if ans[i]==0:
			candid.append(i);
	return candid
	

def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:
	sudoku[pos[0]-1][pos[1]-1] = num
	return sudoku

def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[List[int]]:
	sudoku[pos[0]-1][pos[1]-1] = 0
	return sudoku

def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
	sudoku1 = sudoku
	def solver(sudoku: List[List[int]]) -> bool:
		if(find_first_unassigned_position(sudoku)!=[-1,-1]):
			pos = find_first_unassigned_position(sudoku)
			l1 = get_candidates(sudoku,pos)
			for x in l1:
				sudoku = make_move(sudoku,pos,x)
				if(solver(sudoku)):
					return True
				sudoku = undo_move(sudoku,pos)
		else:
			return valid_sudoku(sudoku)
		return False
	if(solver(sudoku)):
		return (True, sudoku)
	else:
		return (False, sudoku1)			

if __name__ == "__main__":
	sudoku = input_sudoku()
	possible, sudoku = sudoku_solver(sudoku)
	if possible:
		print("Found a valid solution for the given sudoku :)")
		print_sudoku(sudoku)

	else:
		print("The given sudoku cannot be solved :(")
		print_sudoku(sudoku)
