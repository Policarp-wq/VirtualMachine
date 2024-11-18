import argparse

from bitarray import bitarray
from bitarray.util import int2ba
import os
from main import Logger


class Assembler:

    def __init__(self, input_script, output, log):
        self.syntax = {
            'LOAD_CONST': self.load_const,
            'READ': self.read_from_memory,
            'WRITE': self.write_in_memory,
            'SGN': self.sgn
        }
        self.input_file = input_script
        self.output_file = output
        self.logger = log

    def log(self, tag, msg):
        self.logger.log(tag, msg)

    def get_hex(self, bin_arr):
        res = []
        arr = bin_arr.to01()
        for i in range(0, len(arr), 8):
            converting = hex(int(arr[i + 4:i + 8][::-1], 2))[2:] + hex(int(arr[i:i + 4][::-1], 2))[2:]
            res.append(f'0x{converting.upper()}')
        return res

    def read_commands(self):
        bit_arrays = []
        print('Read instructions from ', os.path.abspath(self.input_file))
        with open(self.input_file, 'r') as f:
            for line in f.readlines():
                parts = line.split()
                bit_arrays.append(self.syntax[parts[0]](*parts[1:]))
        with open(self.output_file, 'wb') as f:
            for arr in bit_arrays:
                f.write(arr)
        print('Binary file saved to ', os.path.abspath(self.output_file))

    # A[0-6]=66, B[7-36]=const 5byte
    # int2ba выдаёт в читамом виде слева направо
    def load_const(self, const):
        a = 66
        const = int(const)
        res = bitarray(40)
        res.setall(0)
        res[:7] = int2ba(a, length=7)[::-1]
        res[7:37] = int2ba(const, length=30)[::-1]
        bytes = self.get_hex(res)
        logger.log_bytes('LOAD_CONST', bytes)
        return bitarray(res)

    # A[0-6]=81, B[7-16]=address 3byte
    def read_from_memory(self, address):
        a = 81
        address = int(address)
        res = bitarray(24)
        res.setall(0)
        res[0:7] = int2ba(a, length=7)[::-1]
        res[7:17] = int2ba(address, length=10)[::-1]
        bytes = self.get_hex(res)
        logger.log_bytes('READ', bytes)
        return bitarray(res)

    # A[0-6]=53, B[7-21]=shift  3byte
    def write_in_memory(self, shift):
        a = 53
        shift = int(shift)
        res = bitarray(24)
        res.setall(0)
        res[0:7] = int2ba(a, length=7)[::-1]
        res[7:22] = int2ba(shift, length=14)[::-1]
        bytes = self.get_hex(res)
        logger.log_bytes('WRITE', bytes)
        return bitarray(res)

    # A[0-6]=101, B[7-21]=shift, C[22-31]=address 4byte
    def sgn(self, shift, address):
        a = 101
        shift = int(shift)
        address = int(address)
        res = bitarray(32)
        res.setall(0)
        res[0:7] = int2ba(a, length=7)[::-1]
        res[7:22] = int2ba(shift, length=14)[::-1]
        res[22:32] = int2ba(address, length=10)[::-1]
        bytes = self.get_hex(res)
        logger.log_bytes('SGN', bytes)
        return bitarray(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--binpath', type=str, required=True, help='Path to the binary file')
    parser.add_argument('--log', type=str, required=False, help='Path to the log file')
    parser.add_argument('--src', type=str, required=True, help='Source')

    src = parser.parse_args().src
    binary_file = parser.parse_args().binpath
    log = parser.parse_args().log

    logger = Logger(log)
    lol = Assembler(src, binary_file, logger)
    lol.read_commands()
    logger.stop()
