
class BoardState:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        # print out the sudoku board, leaving empty cells as '-' including hard borders for each 3x3 square
        result = ''
        for i in range(9):
            if i % 3 == 0:
                result += '-------------\n'
            for j in range(9):
                if j % 3 == 0:
                    result += '|'
                if self.state[i][j] == '':
                    result += '-'
                else:
                    result += str(self.state[i][j])
            result += '|\n'
        result += '-------------\n'
        return result

    def __eq__(self, other):
        return self.state == other.state

    def validate_set(self, num_set):
        # remove -1 from the set
        num_set = [num for num in num_set if num != '']
        if len(set(num_set)) == len(num_set):
            return True

    def is_all_rows_valid(self):
        for row in self.state:
            if not self.validate_set(row):
                return False
            
        return True

    def is_all_columns_valid(self):
        for i in range(9):
            column = [row[i] for row in self.state]
            if not self.validate_set(column):
                return False
            
        return True
        
    def is_all_squares_valid(self):
        for i in range(3):
            for j in range(3):
                square = []
                for k in range(3):
                    for l in range(3):
                        square.append(self.state[i*3+k][j*3+l])
                if not self.validate_set(square):
                    return False
        return True

    def is_valid(self):
        # print(f"Rows: {self.is_all_rows_valid()} Columns: {self.is_all_columns_valid()} Squares: {self.is_all_squares_valid()}")
        return self.is_all_rows_valid() and self.is_all_columns_valid() and self.is_all_squares_valid()
    
    def next_empty_index(self):
        for i in range(8, -1, -1):
            for j in range(8, -1, -1):
                if self.state[i][j] == '':
                    return (i, j)
        return None
    
    def generate_next_board(self, i, j, num):
        new_state = [row[:] for row in self.state]
        new_state[i][j] = num
        return BoardState(new_state)
    
    def get_filled_rows(self):
        return [row for row in self.state if '' not in row]
    
    def get_filled_rows_as_int(self):
        return [
            int(''.join(
                [str(x) for x in row]
            )) for row in self.get_filled_rows()
        ]

    def test_gcd(self, threshold):
        # test if the current gcd between all rows is less than the given threshold
        candidate_numbers = self.get_filled_rows_as_int()
        for i in range(len(candidate_numbers)):
            for j in range(i+1, len(candidate_numbers)):
                if find_gcd(candidate_numbers[i], candidate_numbers[j]) < threshold:
                    return False

def find_gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

def find_list_gcd(num_list):
    _num_list = sorted(num_list, reverse=True)
    while _num_list[1]:
        print(_num_list)
        _num_list = _num_list[:1] + [x % _num_list[0] for x in num_list[1:]]
        _num_list = sorted(_num_list)
    return _num_list
    # result = num_list[0]
    # for num in num_list[1:]:
    #     result = find_gcd(result, num)
    # return result

class Node:
    def __init__(self, data):
        self.parent = None
        self.data = data

    def __str__(self):
        return self.data.state.__str__()

    def get_children(self):
        next_index = self.data.next_empty_index()
        if next_index is None:
            # print("We are done")
            # print(self)
            return []

        i, j = next_index
        return [Node(self.data.generate_next_board(i, j, num)) for num in range(0, 10)]

    def get_children_with_threshold(self, threshold):
        pass


    def is_solved(self):
        return self.data.is_valid() and self.data.next_empty_index() is None
    
    def is_valid(self):
        return self.data.is_valid()