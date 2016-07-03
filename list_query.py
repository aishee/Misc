#!/usr/bin/python

#Make by aishee
import re
import string

def main():
    #Input Part starts here
    number_of_words = input("Enter number of words: ")
    list_data = []
    print("Enter the words 1 per line by ppressing Enter after each word ")
    for i in range(0, number_of_words):
        list_data.append(raw_input("Enter Word: "))
    #input part Ends here & processing start here
    converted_string = " ".join(list_data)
    converted_string = converted_string.lower()
    for c in string.punctuation:
        converted_string = converted_string.replace(c, "")
    relisted_data = converted_string.split()
    dict_data = {};
    for item in relisted_data:
        if dict_data.has_key(item):
            dict_data[item] = dict_data[item] + 1
        else:
            dict_data[item] = 1
    #Processing Ends here and Output starts below
    
    for i in dict_data:
        print(i, dict_data[i])
    
    #output ends here
#main module ands here
if __name__ == '__main__':
    main()
    
