#-*-coding:utf8;-*-
#qpy:3
#qpy:console


if True: 
    from time import time
    def loop_gen(r,d=None, _f=True):
        if _f:
            if d == None:
                d = len(r) 
            elif len(r) != d:
                raise IndexError( f"{'Not enough' if len(r) < d else 'To many'} ranges ({len(r)}) provided for nesting depth ({d})" )
        if d>0:
            for i in range(*r[-d]): # pylint: disable=invalid-unary-operand-type
                a = [i]
                for each in loop_gen(r,d-1, _f=False):
                    yield a + each
        else:
            yield []
    
    if True:
        t0 = time()
        r = [(-1,2) for _ in range(2)]
         
        for ln, d in enumerate( loop_gen(r) ):
            print(ln, d)
            pass
        print( f"time: {time()-t0}" )
    if False:
        ln = 0
        for i in range(0,5,2):
            for j in range(9):
                for k in range(39,30,-3):
                    for l in range(100,201,50):
                        print(ln, i,j,k,l)
                        pass
        print( f"time: {time()-t0}" )





#