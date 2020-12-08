class opcodes():
    def __init__(self,input):
        self.input = input
        self.codes = dict()
        for each in self.input:
            if each[1][0] not in self.codes:
                self.codes[each[1][0]] = []
        self.not_valid = []
        self.operations = [
        self.addr , self.addi ,
        self.mulr , self.muli ,
        self.banr , self.bani ,
        self.borr , self.bori ,
        self.setr , self.seti ,
        self.gtir , self.gtri ,self.gtrr ,
        self.eqir , self.eqri , self.eqrr ]


    def copy(self,a,b,c):
        new_a = a[:]
        new_b = b[:]
        new_c = c[:]
        return [new_a,new_b,new_c]

    def try_all(self,a,b,c):
        valid_operations = 0
        # addition
        if self.addr(a,b,c):
            valid_operations += 1
        if self.addi(a,b,c):
            valid_operations += 1
        # multiplications
        if self.mulr(a,b,c):
            valid_operations += 1
        if self.muli(a,b,c):
            valid_operations += 1
        # Bitwise AND
        if self.banr(a,b,c):
            valid_operations += 1
        if self.bani(a,b,c):
            valid_operations += 1
        # Bitwise OR
        if self.borr(a,b,c):
            valid_operations += 1
        if self.bori(a,b,c):
            valid_operations += 1
        # Assignment
        if self.setr(a,b,c):
            valid_operations += 1
        if self.seti(a,b,c):
            valid_operations += 1
        # Greater-than testing
        if self.gtir(a,b,c):
            valid_operations += 1
        if self.gtri(a,b,c):
            valid_operations += 1
        if self.gtrr(a,b,c):
            valid_operations += 1
        # Equality testing:
        if self.eqir(a,b,c):
            valid_operations += 1
        if self.eqri(a,b,c):
            valid_operations += 1
        if self.eqrr(a,b,c):
            valid_operations += 1
        if valid_operations != 0:
            return valid_operations
        else:
            if b[0] not in self.not_valid:
                self.not_valid.append(b[0])
            print "no valid opcodes", self.not_valid, "||||", a,b,c
            return False

    def addr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] + input[instruction[2]])
        if input == wanted_result:
            self.codes[code].append(self.addr)
            return True
        else:
            return False

    def addi(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] + instruction[2])
        if input == wanted_result:
            self.codes[code].append(self.addi)
            return True
        else:
            return False

    #--------------------

    def mulr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] * input[instruction[2]])
        if input == wanted_result:
            self.codes[code].append(self.mulr)
            return True
        else:
            return False

    def muli(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] * instruction[2])
        if input == wanted_result:
            self.codes[code].append(self.muli)
            return True
        else:
            return False

    #--------------------
    def banr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] & input[instruction[2]])
        if input == wanted_result:
            self.codes[code].append(self.banr)
            return True
        else:
            return False

    def bani(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] & instruction[2])
        if input == wanted_result:
            self.codes[code].append(self.bani)
            return True
        else:
            return False

    #--------------------

    def borr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] | input[instruction[2]])
        if input == wanted_result:
            self.codes[code].append(self.borr)
            return True
        else:
            return False

    def bori(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = (input[instruction[1]] | instruction[2])
        if input == wanted_result:
            self.codes[code].append(self.bori)
            return True
        else:
            return False

    #--------------------

    def setr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = input[instruction[1]]
        if input == wanted_result:
            self.codes[code].append(self.setr)
            return True
        else:
            return False

    def seti(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        input[instruction[3]] = instruction[1]
        if input == wanted_result:
            self.codes[code].append(self.seti)
            return True
        else:
            return False

    #--------------------

    def gtir(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        if instruction[1] > input[instruction[2]]:
            input[instruction[3]] = 1
        else:
            input[instruction[3]] = 0
        if input == wanted_result:
            return True
            self.codes[code].append(self.gtir)
        else:
            return False

    def gtri(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        if input[instruction[1]] > instruction[2]:
            input[instruction[3]] = 1
        else:
            input[instruction[3]] = 0
        if input == wanted_result:
            self.codes[code].append(self.gtri)
            return True
        else:
            return False

    def gtrr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        if input[instruction[1]] > input[instruction[2]]:
            input[instruction[3]] = 1
        else:
            input[instruction[3]] = 0
        if input == wanted_result:
            self.codes[code].append(self.gtrr)
            return True
        else:
            return False


    #-------------------

    def eqir(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        if instruction[1] == input[instruction[2]]:
            input[instruction[3]] = 1
        else:
            input[instruction[3]] = 0
        if input == wanted_result:
            self.codes[code].append(self.eqir)
            return True
        else:
            return False

    def eqri(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        if input[instruction[1]] == instruction[2]:
            input[instruction[3]] = 1
        else:
            input[instruction[3]] = 0
        if input == wanted_result:
            self.codes[code].append(self.eqri)
            return True
        else:
            return False

    def eqrr(self,a,b,c):
        input,instruction,wanted_result = self.copy(a,b,c)
        code = instruction[0]
        if input[instruction[1]] == input[instruction[2]]:
            input[instruction[3]] = 1
        else:
            input[instruction[3]] = 0
        if input == wanted_result:
            self.codes[code].append(self.eqrr)
            return True
        else:
            return False
