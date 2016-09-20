import re


# Function for finding substring between known delimiters
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


# Function for listing substrings of strings of the form "[Pt:5], [Au:1]"
# Separating them as "Pt,5,Au,1"
def get_atype_anumber(s):
    sub_list = s.split(',')
    for i in range(len(sub_list)):
        sub_list[i] = sub_list[i].strip()
        sub_list[i] = find_between(sub_list[i], '[', ']')
        sub_list[i] = sub_list[i].split(':')
    sub_list = [j for i in sub_list for j in i]
    return sub_list


# Function for listing number substrings from strings of the form "[0:10]"
def get_number_list(s):
    return re.findall("[-+]?\d*\.\d+|\d+", s)


# Function for determining if input string is or not an integer
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# Function for joining strings from list previously parsed by get_atype_anumber method.
def get_output_name(s):
    return ''.join(tuple(get_atype_anumber(s)))


# Function for getting total number of atoms from a list
def get_nAtoms_lst(lst):
    nAtoms = 0
    for elem in lst:
        if is_number(elem):
            nAtoms += int(elem)
    return nAtoms


# Function for getting total number of atoms from a string of the form "[Pt:5], [Au:1]"
def get_nAtoms_str(s):
    return get_nAtoms_lst(get_atype_anumber(s))


# Function for getting a list of only the quantities of each atom type
def get_atoms_quantity_list(lst):
    return [int(e) for e in lst if is_number(e)]


# print(get_output_name("[Pt:5], [Au:10]"))
# print(get_nAtoms_str("[Pt:5], [Au:10]"))
