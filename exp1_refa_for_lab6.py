# coding=utf8
import re
import unittest

simplify_pattern = re.compile(r'(?P<var_name>[a-zA-Z]+)\s*=\s*(?P<var_value>\d+)')


def is_valid(char):
    if char.isdigit() or char.isalpha() or is_symbol(char):
        return True
    else:
        return False


def is_symbol(char):
    if char in ['+', '*', '-', '*', '^']:
        return True
    else:
        return False


def raise_error(error_message):
    print error_message


class Term(object):
    def __init__(self, num, dic):
        self.Num = num
        self.Dict = dic

    def eva(self, known):
        for key in known:
            if key in self.Dict:
                self.Num *= known[key] ** self.Dict.pop(key)
            else:
                pass

    def diff(self, var):
        __tmp = self.Dict.get(var)
        if __tmp == 0:
            pass
        else:
            self.Num *= __tmp
            self.Dict[var] = __tmp - 1

    def to_string(self):
        st = str(self.Num)
        for k in self.Dict:
            if self.Dict[k] == 0:
                continue
            else:
                st = st + '*' + k + '**' + str(self.Dict[k])
        return st


class Expression(object):
    def __init__(self, result, tup):
        self.Sum = result
        self.Tup = tup

    def eva(self, known):
        res = ''
        for i in self.Tup:
            term = Term(i[0], i[1])
            term.eva(known)
            st = term.to_string()
            try:
                self.Sum += float(st)
            except ValueError:
                res = res + st + '+'
        res += str(self.Sum)
        return res

    def diff(self, var):
        res = ''
        for i in self.Tup:
            term = Term(i[0], i[1])
            if var in term.Dict:
                term.diff(var)
                st = term.to_string()
                res = res + st + '+'
            else:
                pass
        return res[:-1]


class Solution(object):
    def __init__(self, user_input_expression, user_input_command):
        self.user_input_expression = user_input_expression
        self.user_input_command = user_input_command
        self.expression = ""
        self.command = ""
        self.acceptable_expression = ""
        self.data = ()
        self.var_list = []
        self.var_dict = {}

    def command_or_expression(self):
        """
        :return 1: 化简
        :return 2: 求导
        :return 3: 表达式
        :return 4: 结束循环
        """
        self.expression = self.user_input_expression
        if self.user_input_expression == "#####" or self.user_input_command == "#####":
            return 4
        elif self.user_input_command.startswith("!simplify"):
            self.command = self.user_input_command
            return 1
        elif self.user_input_command.startswith("!d/d"):
            self.command = self.user_input_command
            return 2
        else:

            return 3

    def generate_expression(self):
        """
        :return acceptable_expression: python接受的可运行字符串
        """
        index = 0
        while index < len(self.expression) - 1:
            if self.expression[index].isdigit() and self.expression[index + 1].isalpha():
                self.expression = self.expression[:index + 1] + '*' + self.expression[index + 1:]
            if not (is_valid(self.expression[index]) and is_valid(self.expression[index + 1])):
                raise_error("Invalid Input")
                return False
            index += 1
        acceptable_expression = self.expression
        # 幂运算处理
        if '^' in self.user_input_expression:
            acceptable_expression = self.expression.replace('^', '**')
        # 减号处理
        if '-' in self.user_input_expression:
            acceptable_expression = acceptable_expression.replace('-', '+-')

        self.acceptable_expression = acceptable_expression
        return acceptable_expression

    def generate_var_list(self):
        """
        :return: 变量列表
        """
        index = 1
        name = ""
        var_list = []
        while index < len(self.acceptable_expression):
            if self.acceptable_expression[index - 1].isalpha():
                name += self.acceptable_expression[index - 1]
                if not self.acceptable_expression[index].isalpha():
                    if name in var_list:
                        pass
                    else:
                        var_list.append(name)
                    name = ""
            if index == len(self.acceptable_expression) - 1 and self.acceptable_expression[index].isalpha():
                name += self.acceptable_expression[index]
                if name in var_list:
                    pass
                else:
                    var_list.append(name)
                name = ""
            else:
                pass
            index += 1
        self.var_list = var_list
        return var_list

    def generate_var_data(self):
        add_list = self.acceptable_expression.split('+')
        result = 0
        data_list = []
        for i in add_list:
            try:
                result += eval(i)
            except NameError:
                multiple_list = i.split("*")
                num = 1
                dic = {}
                j = 0
                while j < (len(multiple_list)) - 1:
                    if multiple_list[j].isalpha() and multiple_list[j] not in dic:
                        if multiple_list[j+1] == "":
                            dic[multiple_list[j]] = int(multiple_list[j+2])
                            j += 2
                        else:
                            dic[multiple_list[j]] = 1
                    elif multiple_list[j].isalpha() and multiple_list[j] in dic:
                        if multiple_list[j+1] == "":
                            dic[multiple_list[j]] + int(multiple_list[j+2])
                            j += 2
                        else:
                            dic[multiple_list[j]] += 1
                    else:
                        try:
                            num *= float(multiple_list[j])
                        except ValueError:
                            pass
                    j += 1
                if multiple_list[-1].isalpha():
                    if multiple_list[-1] not in dic:
                        dic[multiple_list[-1]] = 1
                    else:
                        dic[multiple_list[-1]] += 1
                elif multiple_list[-1].isdigit() and j < len(multiple_list):
                    num *= multiple_list[-1]
                data_list.append((int(num), dic))
        self.data = result, tuple(data_list)
        return result, tuple(data_list)

    def generate_var_value(self):
        count = 0
        var_dict = {}
        simplify_match = simplify_pattern.finditer(self.command)
        if simplify_match:
            for match in simplify_match:
                if match.group('var_name') not in self.var_list:
                    raise_error("No such variable")
                else:
                    try:
                        var_dict[match.group('var_name')] = float(match.group('var_value'))
                    except ValueError:
                        raise_error("Invalid value")
                    count += 1
        if not count:
            raise_error("No variable")
            return False
        else:
            self.var_dict = var_dict
            return var_dict

    def diff_var(self):
        try:
            var = self.command.split(" ")[1]
        except IndexError:
            raise_error("Error!")
            return False
        if var in self.var_list:
            return var
        else:
            raise_error("Error!")
            return False

    def setup(self):
        # 处理表达式
        self.command_or_expression()
        self.generate_expression()
        self.generate_var_list()
        self.generate_var_data()
        # 化简
        if self.command_or_expression() == 1:
            self.generate_var_value()
            if self.var_dict:
                main_data = self.data
                e = Expression(main_data[0], main_data[1])
                res = e.eva(self.var_dict).replace("**", "^")
                try:
                    return str(eval(res))
                except:
                    return res
        # 求导
        elif self.command_or_expression() == 2:
            var = self.diff_var()
            if var:
                main_data = self.data
                e = Expression(main_data[0], main_data[1])
                return e.diff(var).replace("**", "^")

if __name__ == "__main__":
    print Solution("3x+2y", "!simplify x=2, y=3").setup()


