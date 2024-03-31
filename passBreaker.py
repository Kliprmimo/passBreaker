# to_do make it so that logging actually looks cool

from pwn import *  # type: ignore  
import argparse
import itertools
import time
alphabet_lc = "abcdefghijklmnopqrstuvwxyz"
alphabet_uc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

def check_env():
    if not term.can_init():
        print('try using linux env, logging might not look great because pwnlib term could not be enabled ')
        exit()
        
def bruteforce_pass_lc(max_length, hashe, mode, logger_inst):
    if mode == 'alphabet_lc':
        for curr_len in range(max_length):
            for pass_candidate in itertools.product(alphabet_lc, repeat=(curr_len+1)):
                pass_candidate = str(''.join(pass_candidate))
                current_hashe = sha256sumhex(pass_candidate.encode()) # type: ignore  
                # logger_inst.status(current_hashe) # enabling this option slows down breaking hashes to painfull degree
                if current_hashe == hashe:
                    logger_inst.success('Found hash! Password is: ' + pass_candidate)
                    return pass_candidate
        logger_inst.faliure('Did not find hash :( Try another mode!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='passBraker.py', description='simple script displaying how easy it is to break weak passwords' )
    parser.add_argument('--no-env-check', help='check to allow running on env that does not support pwnlib term', action='store_true', dest='no_env_check')
    args = parser.parse_args()
    if not args.no_env_check:
        check_env()

    log.info('Starting hashe checking')
    # logger = log.progress('Current hashe')
    logger = log.progress('Calculating hashes...') # temp solution

    start_time = time.time()
    bruteforce_pass_lc(5, sha256sumhex('zzzzz'.encode()), 'alphabet_lc', logger) # type: ignore 
    end_time = time.time()
    total_time = end_time - start_time
    log.info(f'Time taken: {total_time}')