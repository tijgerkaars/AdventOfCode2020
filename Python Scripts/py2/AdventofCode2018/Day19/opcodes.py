class opcodes():
    def __init__(self):
        self.operations = [
        self.addr , self.addi ,
        self.mulr , self.muli ,
        self.banr , self.bani ,
        self.borr , self.bori ,
        self.setr , self.seti ,
        self.gtir , self.gtri ,self.gtrr ,
        self.eqir , self.eqri , self.eqrr ]

        self.codes = [
        "addr" , "addi" ,
        "mulr" , "muli" ,
        "banr" , "bani" ,
        "borr" , "bori" ,
        "setr" , "seti" ,
        "gtir" , "gtri" , "gtrr" ,
        "eqir" , "eqri" , "eqrr" ]

    def execute(self,code,register):
        code,a,b,c = code
        for i,each in enumerate(self.codes):
            if code == each:
                register = self.operations[i](register,a,b,c)
                break
        return register


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
