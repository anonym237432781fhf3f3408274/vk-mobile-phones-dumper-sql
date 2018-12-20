from sys import platform

END = '\x1b[0m'
GRAY = '\x1b[37;4m'
RED = '\x1b[31m'
BLUE = '\x1b[37;36m'
WINDOWS = ['win32', 'win64']

def echoPlus(text):
    if platform in WINDOWS:
        print('[+] ' + text)
    else:
        print('[' + BLUE + '+' + END + '] ' + text)

def echoMinus(text):
    if platform in WINDOWS:
        print('[-] ' + text)
    else:
        print('[' + RED + '-' + END + '] ' + text)

def echoWarning(text):
    if platform in WINDOWS:
        print('[!] ' + text)
    else:
        print('[' + RED + '!' + END + '] ' + text)

def echoInfo(text):
    if platform in WINDOWS:
        print('[*] ' + text)
    else:
        print('[' + BLUE + '*' + END + '] ' + text)
