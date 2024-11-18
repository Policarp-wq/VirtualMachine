import pytest

from assembler import *


def get_instance():
    return Assembler('', '', Logger(None))


@pytest.mark.parametrize("const, expected", [
    (307, bitarray('0100001110011001000000000000000000000000')),
    (54, bitarray('0100001011011000000000000000000000000000'))
])
def test_load_const(const, expected):
    assert get_instance().load_const(const) == expected

@pytest.mark.parametrize("address, expected", [
    (375, bitarray('100010111101110100000000')),
    (22, bitarray('100010101101000000000000'))
])
def test_read(address, expected):
    assert get_instance().read_from_memory(address) == expected

@pytest.mark.parametrize("shift, expected", [
    (99, bitarray('10101101100011000000000')),

])
def test_write(shift, expected):
    assert get_instance().write_in_memory(shift) == expected

@pytest.mark.parametrize("shift, address, expected", [
    (449, 243, bitarray('10100111000001110000001100111100')),

])
def test_sgn(shift, address, expected):
    assert get_instance().sgn(shift, address) == expected
