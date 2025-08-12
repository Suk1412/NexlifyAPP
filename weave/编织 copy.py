
import json

from func import check_critical_positions
from tools import landmine, matrix_flat, split_by_element

def color_print(text="这是红色文字", color="Red"):
    text = str(text)
    if color.lower() == "red" or color.lower() == "r":
        print("\033[1;31m" + text + "\033[0m")
    elif color.lower() == "green" or color.lower() == "g":
        print("\033[1;32m" + text + "\033[0m")
    elif color.lower() == "yellow" or color.lower() == "y":
        print("\033[1;33m" + text + "\033[0m")
    elif color.lower() == "blue" or color.lower() == "b":
        print("\033[1;34m" + text + "\033[0m")
    elif color.lower() == "magenta" or color.lower() == "m":
        print("\033[1;35m" + text + "\033[0m")
    elif color.lower() == "cyan" or color.lower() == "c":
        print("\033[1;36m" + text + "\033[0m")
    elif color.lower() == "white" or color.lower() == "w":
        print("\033[1;37m" + text + "\033[0m")
    else:
        print(text)




class MouseWeaving():
    def __init__(self, height, width, horizontal_dict,vertical_dict):
        self.height = height
        self.width = width
        self.horizontal_dict = horizontal_dict
        self.vertical_dict = vertical_dict
        self.matrix = []
        self.correct = "■"
        self.incorrect = "□"
        self.standby = "○"
        self.beam = None
        self.create_grid()
    

    def create_grid(self):
        self.matrix = [(i, j) for i in range(1, self.height + 1) for j in range(1,self.width + 1)]
        return self.matrix
    
    def firstcheck(self, sector_length=10, value=10, vertical_value=1, ex_length=0):
        a_standby_num = sector_length - value
        b_standby_num = sector_length - value
        a_correct_num = sector_length - a_standby_num - b_standby_num        
        for j in range(ex_length + a_standby_num + 1, ex_length + a_standby_num + a_correct_num + 1):
            try:
                if self.beam == "horizontal":
                    index = self.matrix.index((vertical_value,j))
                if self.beam == "vertical":
                    index = self.matrix.index((j,vertical_value))
                self.matrix[index] = 1
            except ValueError:
                pass

    def secondcheck(self):
        ...
    

    def signgle(self, condition_dict,beam="vertical"):
        self.beam = beam
        length = self.width if beam == "horizontal" else self.height
        for i in condition_dict.keys():
            decryption=False
            num = len(condition_dict[i])
            if num == 1:
                value1 = condition_dict[i][0]
                sector_1_length = length
                if value1 > sector_1_length/2:
                    decryption=True
            if num == 2:
                value1, value2 = condition_dict[i]
                sector_lengths = [length - (sum(condition_dict[i]) - condition_dict[i][_]) - (num-1) for _ in range(num)]
                sector_1_length,sector_2_length = sector_lengths
                if value1 > sector_1_length/2:
                    decryption=True
            if num == 3:
                value1, value2, value3 = condition_dict[i]
                sector_lengths = [length - (sum(condition_dict[i]) - condition_dict[i][_]) - (num-1) for _ in range(num)]
                sector_1_length,sector_2_length,sector_3_length = sector_lengths
                if value1 > sector_1_length/2:
                    decryption=True
            if num == 4:
                value1, value2, value3, value4 = condition_dict[i]
                sector_lengths = [length - (sum(condition_dict[i]) - condition_dict[i][_]) - (num-1) for _ in range(num)]
                sector_1_length,sector_2_length,sector_3_length,sector_4_length = sector_lengths
                if value1 > sector_1_length/2:
                    decryption=True
            if num == 5:
                value1, value2, value3, value4, value5 = condition_dict[i]
                sector_lengths = [length - (sum(condition_dict[i]) - condition_dict[i][_]) - (num-1) for _ in range(num)]
                sector_1_length,sector_2_length,sector_3_length,sector_4_length,sector_5_length = sector_lengths
                if value1 > sector_1_length/2:
                    decryption=True

            axis = "列" if self.beam == "horizontal" else "行"
            status = "可破译" if decryption else "不可破译"
            color = "green" if decryption else "red"
            # color_print(f"第{i}{axis}{status}", color)
            if num >= 1 and decryption:
                self.firstcheck(sector_length=sector_1_length, value=value1, vertical_value=i)
            if num >= 2 and decryption:
                self.firstcheck(sector_length=sector_2_length, value=value2, vertical_value=i, ex_length=value1 + 1)
            if num >= 3 and decryption:
                self.firstcheck(sector_length=sector_3_length, value=value3, vertical_value=i, ex_length=value1 + value2 + 2)
            if num >= 4 and decryption:
                self.firstcheck(sector_length=sector_4_length, value=value4, vertical_value=i, ex_length=value1 + value2 + value3 + 3)
            if num >= 5 and decryption:
                self.firstcheck(sector_length=sector_5_length, value=value5, vertical_value=i, ex_length=value1 + value2 + value3 + value4 + 4)
            else:
                ... 
        

    def signgle2(self,beam="vertical"):
        if beam == "horizontal":
            for i in range(0, len(self.matrix), self.width):
                value = i//self.width+1
                A = horizontal_dict[value]
                B = self.matrix[i:i+self.width]
                self.matrix[i:i+self.width] = landmine(A,B)
        elif beam == "vertical":
            self.matrix = matrix_flat(self.width,self.matrix)
            for i in range(0, len(self.matrix), self.height):
                value = i//self.height+1
                A = horizontal_dict[value]
                B = self.matrix[i:i+self.height]
                self.matrix[i:i+self.height] = landmine(A,B)
            self.matrix = matrix_flat(self.height,self.matrix)
    
    def signgle3(self,condition_dict,beam="vertical"):
        self.beam = beam
        for i in range(0, len(self.matrix), self.width):
            height_value = i // self.width + 1
            condition_lst = condition_dict[height_value]
            becheck_lst = self.matrix[i:i+self.width]
            split_list = split_by_element(becheck_lst,-1)
            decryption=False
            if height_value == 1:
                value1 = condition_lst[0]
            num = len(condition_dict[height_value])
            print(f"第几行:{height_value},真有{num}区间，已有{len(split_list)}区间")
            if num == 1:
                value1 = condition_dict[height_value][0]
                for x in split_list:
                    sector_1_length = len(x)
                    if sector_1_length < value1:
                        for point in x:
                            index = self.matrix.index(point)
                            self.matrix[index] = -1
                    if sector_1_length >= value1:
                        self.firstcheck(sector_length=sector_1_length, value=value1, vertical_value=height_value, ex_length=2)
            if num >= 2:
                ...
                print(condition_lst,becheck_lst)
                correct_list = check_critical_positions(condition_lst,becheck_lst)
                for idx in correct_list:
                    index = self.matrix.index(idx)
                    self.matrix[index] = 1
            #     ...
            # if num == 3:
            #     ...
               


    def convert(self):
        for _ in range(len(self.matrix)):
            if self.matrix[_] == -1:
                self.matrix[_] = self.incorrect
            elif self.matrix[_] == 1:
                 self.matrix[_] = self.correct
            elif self.matrix[_] != -1 or self.matrix[_] != 1:
                self.matrix[_] = self.standby
        print("   ", end="")
        for i in range(1,self.width+1):
            print(f"{i:<2}", end="")
        print(end=" \n")

        height_length = 1
        for i in range(0, len(self.matrix), self.width):
            print(f"{height_length:<2}", *self.matrix[i:i+self.width], end=" \n")
            height_length += 1

        

height_value = 10
horizontal_dict = {1:[8],
                   2:[3,1,1],
                   3:[5,2,1],
                   4:[3,1,2,1],
                   5:[3,1],
                   6:[1,1,1,1],
                   7:[3,1,1,1],
                   8:[5,1,1],
                   9:[3,1,1],
                   10:[8],}


width_value = 10
vertical_dict = {1:[3,3],
                   2:[4,4],
                   3:[10],
                   4:[1,1,1,1,1],
                   5:[10],
                   6:[1,1],
                   7:[1,2,1,1,1],
                   8:[1,2,1,1],
                   9:[2,2],
                   10:[6],
                   11:[8],}
mouseweav = MouseWeaving(height_value, width_value, horizontal_dict, vertical_dict)
mouseweav.signgle(horizontal_dict,"horizontal")
mouseweav.signgle(vertical_dict,"vertical")
mouseweav.signgle2("horizontal")
mouseweav.signgle2("vertical")
mouseweav.signgle3(horizontal_dict,beam="horizontal")
mouseweav.convert()












