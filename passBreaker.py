from pwn import *  # type: ignore  
import argparse

def check_env():
    if not term.can_init():
        print('try using linux env, logging might not look great because pwnlib term could not be enabled ')
        exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='passBraker.py', description='simple script displaying how easy it is to break weak passwords' )
    parser.add_argument('--no-env-check', help='check to allow running on env that does not support pwnlib term', action='store_true', dest='no_env_check')
    args = parser.parse_args()
    if not args.no_env_check:
        check_env()