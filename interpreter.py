import argparse
import os.path

from bitarray import bitarray

from main import Logger


class Interpreter:
    def __init__(self, binary_file, logger):
        self.stack = []
        self.binary_file = binary_file
        self.commands = {
            53: self.write_in_memory,
            66: self.load_const,
            81: self.read_from_memory,
            101: self.sgn
        }
        self.memory = {}
        self.logger = logger
        self.result_file = 'result.txt'

    def log(self, msg):
        self.logger.log('Interpreter', msg)

    def screen(self, range_from, range_to):
        with open(self.result_file, 'w') as f:
            f.write(f'<result>\n')
            for i in range(range_from, range_to + 1):
                if i not in self.memory:
                    continue
                else:
                    num = self.memory[i]
                f.write(f'  <{i}>{num}</{i}>\n')
            f.write(f'</result>')
        print('Result saved to ', os.path.abspath(self.result_file))

    from bitarray import bitarray
    # A[0-6]=66, B[7-36]=const 5byte
    # A[0-6]=81, B[7-16]=address 3byte
    # A[0-6]=53, B[7-21]=shift  3byte
    # A[0-6]=101, B[7-21]=shift, C[22-31]=address 4byte
    def begin_interpretation(self):
        with open(self.binary_file, 'rb') as f:
            data = f.read()
            pointer = 0
            try:
                while pointer < len(data):
                    operation = int(format(data[pointer], '08b')[:7][::-1], 2)
                    if operation == 53:
                        b = int((format(data[pointer], '08b')[-1] + format(data[pointer + 1], '08b')
                                 + format(data[pointer + 2], '08b')[:-2])[::-1], 2)
                        pointer += 3
                        self.write_in_memory(b)
                    elif operation == 66:
                        b = int((format(data[pointer], '08b')[-1] + format(data[pointer + 1], '08b') + format(
                            data[pointer + 2], '08b') + format(data[pointer + 3], '08b') + format(data[pointer + 4], '08b')[
                                                                                           :-3])[::-1], 2)
                        pointer += 5
                        self.load_const(b)
                    elif operation == 81:
                        b = int((format(data[pointer], '08b')[-1] + format(data[pointer + 1], '08b')
                                 + format(data[pointer + 2], '08b')[0])[::-1], 2)
                        pointer += 3
                        self.read_from_memory(b)
                    elif operation == 101:
                        b = int((format(data[pointer], '08b')[-1] + format(data[pointer + 1], '08b')
                                 + format(data[pointer + 2], '08b')[:-2])[::-1], 2)
                        c = int((format(data[pointer + 2], '08b')[-2:] + format(data[pointer + 3], '08b'))[::-1], 2)
                        pointer += 4
                        self.sgn(b, c)
                    else:
                        pointer += 1
            except Exception as x:
                self.log(x)


    def load_const(self, const):
        self.log(f'Load const {const}')
        self.stack.append(const)

    def read_from_memory(self, address):
        self.log(f'Read from memory {address}')
        if address not in self.memory:
            raise Exception(f'Address {address} not in memory!')
        self.stack.append(self.memory[address])

    def write_in_memory(self, shift):
        self.log(f'Write in memory {shift}')
        if len(self.stack) == 0:
            raise Exception('Stack is empty!')
        top = self.stack.pop()
        self.memory[top + shift] = top

    def sgn(self, shift, address):
        self.log(f'Sgn {shift} {address}')
        top = self.stack.pop()
        self.stack.append(top)
        if (shift + top) not in self.memory:
            raise Exception(f'Address {shift + address} not in memory!')
        self.memory[address] = self.memory[shift + self.stack.pop()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--binpath', type=str, required=True, help='Path to the binary file')
    parser.add_argument('--log', type=str, required=False, help='Path to the log file')
    parser.add_argument('--rangefrom', type=int, required=True, help='Range from for memory')
    parser.add_argument('--rangeto', type=int, required=True, help='Range to for memory')

    binary_file = parser.parse_args().binpath
    log = parser.parse_args().log
    rangefrom = parser.parse_args().rangefrom
    rangeto = parser.parse_args().rangeto

    logger = Logger(log)
    interpreter = Interpreter(binary_file, logger)
    interpreter.begin_interpretation()
    logger.stop()
    interpreter.screen(rangefrom, rangeto)
