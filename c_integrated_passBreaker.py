# to_do make it so that logging actually looks cool

from pwn import log, term, sha256sumhex  # type: ignore
import argparse
import itertools
import time
import subprocess
import sys 

alphabet_lc = "abcdefghijklmnopqrstuvwxyz"
alphabet_uc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"


def check_env():
    if not term.can_init():
        print('try using linux env, logging might not look great because pwnlib term could not be enabled or use --no-env-check option')
        exit()


def execute_hashing(filename, hashe, logger_inst):

    process =  subprocess.Popen(['./hasher', filename, hashe], stdout=subprocess.PIPE,stdin=subprocess.PIPE, stderr=subprocess.PIPE,text=True, bufsize=1, universal_newlines=True)

    while process.poll() is None:
        # stdout, stderr = process.communicate()

        output = process.stdout.readline()
        if output != '':
            logger_inst.status(output)

    return output


def bruteforce_pass_lc(max_length, hashe, mode, logger_inst):
    if mode == 'alphabet_lc':
        for curr_len in range(max_length):
            for pass_candidate in itertools.product(alphabet_lc, repeat=(curr_len+1)):
                pass_candidate = str(''.join(pass_candidate))
                current_hashe = sha256sumhex(
                    pass_candidate.encode())
                # logger_inst.status(current_hashe) # enabling this option slows down breaking hashes to painfull degree
                if current_hashe == hashe:
                    logger_inst.success(
                        'Found hash! Password is: ' + pass_candidate)
                    return pass_candidate
        logger_inst.faliure('Did not find hash :( Try another mode!')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='passBraker.py', description='simple script displaying how easy it is to break weak passwords')
    parser.add_argument('password_hashe', help='password or hashe to be bruteforced')
    parser.add_argument('wordlist', help='file name to bruteforce')
    parser.add_argument('--no-env-check', help='check to allow running on env that does not support pwnlib term', action='store_true', dest='no_env_check')
    parser.add_argument('--hashe', help='add hashe instead of password', action='store_true', dest='hashe_check')

    args = parser.parse_args()

    if not args.no_env_check:
        check_env()

    if not args.hashe_check:
        hashe = sha256sumhex(args.password_hashe.encode())
    else:
        hashe = args.password_hashe

    log.info('Starting hashe checking')
    logger = log.progress('Calculating hashes...')  # temp solution

    start_time = time.time()
    execute_hashing(args.wordlist, hashe , logger)
    end_time = time.time()

    total_time = end_time - start_time
    log.info(f'Time taken: {total_time}')
