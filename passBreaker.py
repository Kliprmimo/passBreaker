from pwn import *  # type: ignore  

def check_env():
    if not term.can_init():
        print('try using linux env, logging might not look great because term could not be enabled ')
        exit()

if __name__ == '__main__':
    check_env()