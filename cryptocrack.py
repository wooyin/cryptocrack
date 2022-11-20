#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__  = 'wooyin'
__version__ = '1.3'
__fork__  = 'https://github.com/mufeedvh/basecrack'
__pypi__ = 'https://pypi.org/search/?q=&o='

import os
import re
import sys
import time
import platform
import json
import argparse
from colorama import init
from termcolor import colored
from pathlib import Path

from src.crack_chain import DecodeBase
from src.messages import push_error, print_line_separator

class BaseCrack:
    def __init__(self, output=None, key=None, magic_mode_call=False, quit_after_fail=True):
        self.output = output
        # initial bools
        self.api_call = False
        self.magic_mode_call = magic_mode_call
        self.image_mode_call = False
        self.quit_after_fail = quit_after_fail
        self.stop_decode = False

        # Force key to ListType or None
        if isinstance(key, str):
            self.key = [key]
        else:
            self.key = key
        # global value
        self.chain = 1
        self.decoding_history = []
        self.total_results = []
        self.rotateCipher = ['Rot13']

    def decode_from_file(self, file):
        """
        `decode_from_file()` fetches the set of base encodings from the input file
        and passes it to 'decode_crypto()' function to decode it all
        """

        print(colored('[-] Decoding Base Data From ', 'cyan') + colored(file, 'yellow'))

        # check whether file exists
        if not Path(file).is_file():
            push_error('File does not exist.')
            quit()

        with open(file) as input_file:
            # reading each line from the file
            for line in input_file:
                # checking if the line/base is not empty
                if len(line) > 1:
                    line = line.strip()
                    print(colored('\n[-] Encoded Crypto: ', 'yellow')+str(line))
                    
                    if self.magic_mode_call:
                        self.magic_mode(line)
                    else:
                        self.decode_crypto(line)

                    print_line_separator()


    # decode crypto once
    def decode_crypto(self, encoded_crypto):
        self.api_call = True
        if len(encoded_crypto) > 3:
            results = []
            # execute decode chain
            encoding_ciphers, decoded_strings = DecodeBase(
                encoded_crypto,
                api_call = self.api_call,
                image_mode = self.image_mode_call
            ).decode()
            for encoding_cipher,decoded_string in zip(encoding_ciphers,decoded_strings):
                results.append([encoding_cipher,decoded_string])
            return results
        else:
            return []
            # push_error("Found no valid base encoded strings.")

    # decode crypto loop
    def decode(self, results, iteration, encoding_pattern, last_decoded_string):
        for result in results:
            # print("Hook: ",2)
            if self.stop_decode:
                # print("Hook: ",7)
                break

            encoding_cipher = result[0]
            decoded_string = result[1]

            # if len(decoded_string) <= 5:
            #     # print("Hook: ",3,len(decoded_string),decoded_string)
            #     continue

            # TODO: Avoid rotate chain like 'Rot13-Rot47-Rot13-Rot47',
            # Avoid Double Rot13
            if encoding_cipher in encoding_pattern[-1:] and encoding_cipher in self.rotateCipher:
                # print("Hook: ",4)
                # if not only rot13, continue to decode
                if len(results) !=1:
                    continue
                # if only rot13, save chain
                else:
                    self.chain +=1
                    self.save_total_results(encoding_pattern,last_decoded_string)
                    return []
            else:
                # print("Hook: ",5,decoded_string)
                if decoded_string not in self.decoding_history:
                    tmp_encoding_pattern = []
                    tmp_encoding_pattern.append(encoding_cipher)
                    print(colored('\n[-] Chain: ', 'grey', attrs=['bold'])+colored(self.chain, 'green')+colored(', Iteration: ', 'grey', attrs=['bold'])+colored(iteration, 'green'))
                    print(colored('\n[-] Heuristic Found Encoding To Be: ', 'yellow')+colored(encoding_cipher, 'green'))
                    print(colored('\n[-] Decoding as {}: '.format(encoding_cipher), 'blue')+colored(decoded_string, 'green'))
                    print(colored('\n{{<<', 'red')+colored('='*70, 'yellow')+colored('>>}}', 'red'))

                # stop on excepted key like 'flag' or 'ctf'
                if (self.key and any(x in decoded_string for x in self.key)):
                    self.stop_decode = True
                    self.chain +=1
                    self.save_total_results(encoding_pattern+tmp_encoding_pattern,decoded_string)
                    return []
                
                decoded_results = self.decode_crypto(decoded_string)
                # Not Empty or None, and avoid repeat decode
                if decoded_results and decoded_string not in self.decoding_history:
                    tmp_iteration = iteration+1
                    self.decoding_history.append(decoded_string)
                    self.decode(decoded_results,tmp_iteration,encoding_pattern+tmp_encoding_pattern,decoded_string)
                else:
                    # print("Hook: ",6)
                    continue

    def save_total_results(self, encoding_pattern, decoded_string):
        # show the encoding pattern in order and comma-seperated
        pattern = ' -> '.join(map(str, encoding_pattern))
        self.total_results.append([len(encoding_pattern),pattern,decoded_string])
        # print("\nTotal_results:",self.total_results)
        # print(colored('-'*70, 'red'))

        # TODO: CTF mode, different color
        # I-1 S-5 b-6 Z-2
        # abcdef to 123456
        # \\ to \
        # end with AA[==], ascii 61[65] ,offset 4

    def magic_mode(self, encoded_crypto):
        """
        `magic_mode()` tries to decode multi-encoded crypto s of any pattern
        """
        # init value
        self.decoding_history = [encoded_crypto]
        iteration = 1
        decoded_string = encoded_crypto

        start_time = time.time()

        results = self.decode_crypto(decoded_string)
        encoding_pattern = []
        for __ in results:
            # print("Hook: ",1)
            self.decode(results,iteration,encoding_pattern,decoded_string)

        if self.total_results is not None:
            end_time = time.time()

            # Sort by iteration, small first
            sort_total_results = quick_sort(self.total_results)

            # Display total results
            for result,tmp_chain in zip(sort_total_results,range(1,len(sort_total_results)+1)):
                iteration = result[0]
                pattern = result[1]
                decoded_string = result[2]

                if tmp_chain > 1:
                    print(colored('\n{{<<', 'red')+colored('='*70, 'yellow')+colored('>>}}', 'red'))

                if len(sort_total_results) != 1:
                    print(colored('\n[-] Chain: ', 'green')+colored(tmp_chain, 'blue', attrs=['bold'])+colored(', Total Iterations: ', 'green')+colored(iteration, 'blue', attrs=['bold']))
                else:
                    print(colored('\n[-] Total Iterations: ', 'green')+colored(iteration, 'blue', attrs=['bold']))

                print(colored('\n[-] Encoded Crypto: ', 'green')+colored(encoded_crypto, 'white', attrs=['bold']))
                print(colored('\n[-] Encoding Pattern: ', 'green')+colored(pattern, 'red', attrs=['bold']))

                print(
                    colored('\n[-] Magic Decode Finished With Result: ', 'green') +
                    colored(decoded_string, 'yellow', attrs=['bold'])
                )

                # generating the wordlist/output file with the decoded base
            if self.output != None:
                open(self.output, 'a').write(decoded_string+'\n')

            completion_time = str(end_time-start_time)[:6]

            print(
                colored('\n[-] Finished in ', 'green') +
                colored(completion_time, 'cyan', attrs=['bold']) +
                colored(' seconds\n', 'green')
            )
            # print(self.decoding_history)
        else:
            quit(colored('\n[!] Not a valid encoding.\n', 'red'))


# print a banner to look cool
def banner():
    banner = '''
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ █████╗  ██████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██║     ██████╔╝ ╚═██╔═╝ ██████═╝   ██║   ██║  ██║██║     ██████╔╝███████║██║     █████╔╝ 
██║     ██╔══██╗   ██║   ██╔══╝     ██║   ██║  ██║██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
╚██████╗██║  ██║   ██║   ██║        ██║   ╚█████╔╝╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ v{0} by {1}
    '''
    print(colored(banner.format(__version__,__author__), 'red')+colored('\n\t\tpython3 cryptocrack.py -h [FOR HELP]\n', 'green'))

# https://blog.csdn.net/zhu6201976/article/details/118877993
def quick_sort(total_results):
    if len(total_results) >= 2:
        mid = total_results[len(total_results) // 2]
        left, right = [], []
        total_results.remove(mid)
        for num in total_results:
            if num >= mid:
                right.append(num)
            else:
                left.append(num)
        return quick_sort(left) + [mid] + quick_sort(right)
    else:
        return total_results

def main():
    banner()

    # setting up argparse module to accept arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base', help='Decode a single encoded crypto  from argument.')
    parser.add_argument('-f', '--file', help='Decode multiple encoded crypto s from a file.')
    parser.add_argument('-m', '--magic', help='Decode multi-encoded crypto s in one shot.', action='store_true')
    parser.add_argument('-o', '--output', help='Generate a wordlist/output with the decoded bases, enter filename as the value.')
    parser.add_argument('-k', '--key', help='Key to stop iteration.', nargs='?', const=['flag','ctf'])
    # TODO
    parser.add_argument('-d', '--depth', help='Iteration depth.')
    parser.add_argument('-r', '--replace', help='Auto replace special char.')
    parser.add_argument('-s', '--slient', help='Only display result.')
    args = parser.parse_args()

    if args.output:
        print(
            colored('\n[>] ', 'yellow') +
            colored('Enabled Wordlist Generator Mode :: ', 'green') +
            colored(args.output+'\n', 'blue')
        )

    """
    decodes base encodings from file if argument is given
    else it accepts a single encoded crypto  from user
    """
    if args.file:
        if args.magic:
            BaseCrack(
                output=args.output,
                key=args.key,
                magic_mode_call=True
            ).decode_from_file(str(args.file))
        else:
            BaseCrack(output=args.output).decode_from_file(str(args.file))

    elif args.base:
        print(colored('[-] Encoded Crypto: ', 'yellow')+colored(str(args.base), 'red'))

        if args.magic:
            BaseCrack(key=args.key).magic_mode(str(args.base))
        else:
            BaseCrack().decode_crypto(str(args.base))

    else:
        if sys.version_info >= (3, 0):
            encoded_crypto = input(colored('[>] Enter Encoded Crypto: ', 'yellow'))
        else:
            encoded_crypto = raw_input(colored('[>] Enter Encoded Crypto: ', 'yellow'))
        
        print(colored('\n{{<<', 'red')+colored('='*70, 'yellow')+colored('>>}}', 'red'))

        if args.magic:
            BaseCrack(key=args.key).magic_mode(encoded_crypto)
        else:
            BaseCrack().decode_crypto(encoded_crypto)

    if args.output:
        print(
            colored('\n[-] Output Generated Successfully > ', 'green') +
            colored(args.output+'\n', 'yellow')
        )

if __name__ == '__main__':
    init()
    main()
