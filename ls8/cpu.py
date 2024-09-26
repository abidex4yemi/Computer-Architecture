# CPU functionality.

import sys


class CPU:
    def __init__(self):
        # 8 general-purpose registers
        self.reg = [0] * 8

        # hold 256 bytes of memory
        self.ram = [0] * 255

        self.pc = 0
        self.sp = 0b11110100

    def ram_read(self, address):
        # memory address register
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, file_name):
        """Load a program into memory."""
        address = 0

        try:
            with open(file_name) as file:
                for instruction in file:
                    binary_num = instruction.split('#')
                    binary_num = binary_num[0].strip()

                    if binary_num == '':
                        continue
                    self.ram_write(address, binary_num)
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(1)

        print(int(self.ram[0], 2))

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = self.pc
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]

        runing = True
        current_address = 0

        while runing:
            op_code = int(f'{self.ram_read(current_address)}', 2)
            if op_code == 130:
                self.reg[int(f'{self.ram_read(current_address+1)}', 2)
                         ] = int(f'{self.ram_read(current_address+2)}', 2)
                shift = op_code
                increment = shift >> 6
                current_address += (increment + 1)

            elif op_code == 71:
                binary = self.reg[int(
                    f'{self.ram_read(current_address+1)}', 2)]
                shift = op_code
                increment = shift >> 6
                current_address += (increment + 1)

            elif op_code == 162:
                self.alu('MUL', self.ram_read(current_address+1),
                         self.ram_read(current_address+2))
                shift = op_code
                increment = shift >> 6
                current_address += (increment + 1)

            elif op_code == 160:
                self.alu('ADD', self.ram_read(current_address+1),
                         self.ram_read(current_address+2))
                print(f"add result: {self.reg[0]}")
                shift = op_code
                increment = shift >> 6
                current_address += (increment + 1)

            elif op_code == 69:
                self.reg[7] = self.reg[self.ram_read(current_address+1)]
                self.sp -= 1
                self.ram_write(self.sp, self.reg[7])

                shift = op_code
                increment = shift >> 6
                current_address += (increment + 1)

            elif op_code == 70:

                self.reg[int(f'{self.ram_read(current_address+1)}', 2)
                         ] = self.ram[self.sp]
                self.sp += 1
                shift = op_code
                increment = shift >> 6
                current_address += (increment + 1)

            elif op_code == 1:
                sys.exit(1)

            elif op_code == 80:
                self.sp -= 1
                self.ram_write(self.sp, current_address+2)
                current_address = self.reg[self.ram_read(current_address+1)]

            elif op_code == 17:
                current_address = self.ram_read(self.sp)
                self.sp += 1
                print(current_address)
