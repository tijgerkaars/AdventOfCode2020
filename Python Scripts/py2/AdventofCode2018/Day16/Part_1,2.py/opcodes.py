class opcodes():
    def __init__(self,input):
        self.input = input
        self.codes = dict()
        for each in self.input:
            if each[1][0] not in self.codes:
                self.codes[each[1][0]] = []
        self.operations = [
        self.addr , self.addi ,
        self.mulr , self.muli ,
        self.banr , self.bani ,
        self.borr , self.bori ,
        self.setr , self.seti ,
        self.gtir , self.gtri ,self.gtrr ,
        self.eqir , self.eqri , self.eqrr ]

    #-------------------------------------------------------------------

    def addr(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] + register[b]
        return register

    def addi(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] + b
        return register

    #-------------------------------------------------------------------

    def mulr(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] * register[b]
        return register

    def muli(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] * b
        return register

    #-------------------------------------------------------------------

    def banr(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] & register[b]
        return register

    def bani(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] & b
        return register

    #-------------------------------------------------------------------

    def borr(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] | register[b]
        return register

    def bori(self,register, a,b,c):
        register = register[:]
        register[c] = register[a] | b
        return register

    #-------------------------------------------------------------------

    def setr(self,register, a,b,c):
        register = register[:]
        register[c] = register[a]
        return register

    def seti(self,register, a,b,c):
        register = register[:]
        register[c] = a
        return register

    #-------------------------------------------------------------------

    def gtir(self,register, a,b,c):
        register = register[:]
        if a > register[b]:
            register[c] = 1
        else:
            register[c] = 0
        return register

    def gtri(self,register, a,b,c):
        register = register[:]
        if register[a] > b:
            register[c] = 1
        else:
            register[c] = 0
        return register

    def gtrr(self,register, a,b,c):
        register = register[:]
        if register[a] > register[b]:
            register[c] = 1
        else:
            register[c] = 0
        return register

    #-------------------------------------------------------------------

    def eqir(self,register, a,b,c):
        register = register[:]
        if a == register[b]:
            register[c] = 1
        else:
            register[c] = 0
        return register

    def eqri(self,register, a,b,c):
        register = register[:]
        if register[a] == b:
            register[c] = 1
        else:
            register[c] = 0
        return register

    def eqrr(self,register, a,b,c):
        register = register[:]
        if register[a] == register[b]:
            register[c] = 1
        else:
            register[c] = 0
        return register
