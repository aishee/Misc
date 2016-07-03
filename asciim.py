#!/usr/bin/env python

import argparse, os, re

def add_to_file(text):
    with open('db.txt', 'a') as f:
        f.write(text + '\n')
        print "Add successful"
        
def list_file_content():
    with open('db.txt', 'r') as f:
        if os.path.getsize('db.txt') == 0:
            print "Nothing to show, the file is empty."
        else:
            print f.read()
def delete_from_file(text):
    with open('db.txt', 'r') as f:
        content = f.readlines()
        with open('db.txt', 'w') as f1:
            for line in content:
                if not re.match(text, line):
                    f1.write(line)
            print "Delete successful"
def sort_file():
    with open('db.txt', 'r') as f:
        all = f.readlines()
        all.sort()
        for line in all:
            print line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Just a simple exercise')
    parser.add_argument('-A', '--Add', help='Add details to file')
    parser.add_argument('-L', '--List', help='List contents of the file', action='store_true')
    parser.add_argument('-S', '--Sort', help='Sort contents of the file', action='store_true')
    parser.add_argument('-D', '--Delete', help='Deletes a name in the file')
    args = parser.parse_args()
    
    if args.Add:
        add_to_file(args.Add)
    if args.List:
        list_file_content()
    if args.Delete:
        delete_from_file(args.Delete)
    if args.Sort:
        sort_file()