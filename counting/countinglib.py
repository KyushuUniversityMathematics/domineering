# 2018.07.07 Y.Mizoguchi
#  libray functions for 
#  complete reward values for 4x4 board status
#  1st player is vertical.
#
import pandas as pd

def transpose(b):
    return([b[0],b[4],b[8],b[12],
            b[1],b[5],b[9],b[13],
            b[2],b[6],b[10],b[14],
            b[3],b[7],b[11],b[15]])
def rotate90(b):
    return([b[3],b[7],b[11],b[15],
            b[2],b[6],b[10],b[14],
            b[1],b[5],b[9],b[13],
            b[0],b[4],b[8],b[12]])
def rotate180(b):
    return(rotate90(rotate90(b)))
def rotate270(b):
    return(rotate90(rotate90(rotate90(b))))
def rotatecheck(b0,l):
    b = int2board(b0)
    tb = transpose(b)
    cl = [b,rotate90(b),rotate180(b),rotate270(b),
          tb,rotate90(tb),rotate180(tb),rotate270(tb)]
    for x in l:
        board=int2board(x[0])
        if board in cl:
            return [x[0],cl.index(board)]
    return []

def reverse_rotate(b0,i):
    b = int2board(b0)
    tb = transpose(b)
    cl = [b,rotate270(b),rotate180(b),rotate90(b),
          tb,rotate90(tb),rotate180(tb),rotate270(tb)]
    return board2int(cl[i]) if (i<8) else b0

def board2int(b):
    return int(''.join(list(map(str,b))),2)

def int2board(i):
    return [int(c) for c in '{:016b}'.format(i)]

# 0: after H, before V
# 1: after V, before H
def turncheck(b):
    return (0 if sum(b) % 4 == 0 else 1)

def boardprint(b):
    board = b if sum(b) % 4==0 else transpose(b)
    for i in range(4):
        print(''.join(['.' if x==0 else 'O' for x in board[4*i:4*(i+1)]]))
#    print('=',board2int(b))
    return None

def boardtex(board):
    l0 = '\\begin{tabular}{|c|c|c|c|}\\hline\n'
    for i in range(4):
        l0 = l0 + ''.join(['.&' if x==0 else 'O&' for x in board[4*i:4*(i+1)-1]])
        l0 = l0 + ''.join(['.' if x==0 else 'O' for x in board[4*(i+1)-1:4*(i+1)]])+'\\\\ \\hline\n'
    l0 = l0 + '\end{tabular}'
    return l0

# check 'board' for putting a horizontal domino at position 'i'
def hcheck(board, i):
    return (i % 4 != 3) and board[i]==0 and board[i+1]==0
# put a horizontal domino on a 'board' at position 'i'
def hfill(board, i):
    b2=[]
    for x in board: b2.append(x)
    b2[i]=b2[i+1]=1
    return b2
# check 'board' for putting a vertical domino at position 'i'
def vcheck(board, i):
    return (i < 4*3) and board[i]==0 and board[i+4]==0
# put a vertical domino on a 'board' at position 'i'
def vfill(board, i):
    b2=[]
    for x in board: b2.append(x)
    b2[i]=b2[i+4]=1
    return b2

def hmoved(board):
    return list(map(lambda x:hfill(board,x),
                    map(lambda x:x[1],
                        filter(lambda x:x[0],
                               map(lambda y:[hcheck(board,y),y], range(16))))))
def vmoved(board):
    return list(map(lambda x:vfill(board,x),
                    map(lambda x:x[1],
                        filter(lambda x:x[0],
                               map(lambda y:[vcheck(board,y),y], range(16))))))

# list of scores starting from a board 'b' and a horizontal domino
def hretrieve(board):
    # list of horizontal moved boards from a board 'board'
    hmoved = list(map(lambda x:hfill(board,x),
                 map(lambda x:x[1],
                     filter(lambda x:x[0],
                            map(lambda y:[hcheck(board,y),y], range(16))))))
    cl = []
    if (hmoved != []):
        # 'cl' is the list of all pair of hmoved board and its score
        for b in hmoved:
            # list of scores starting from a board 'b'
            child = vretrieve(b)
            # list of vertical moved boards from a board 'b'
            vmoved = list(map(lambda x:vfill(b,x),
                 map(lambda x:x[1],
                     filter(lambda x:x[0],
                            map(lambda y:[vcheck(b,y),y], range(16))))))
            # all boards in 'vmoved' are favorable for H
            # that is there is no chance to win for V
            if (all(map(lambda x:([x,-1] in child),vmoved))):
                cl.append([b,-1])  # H win
            # there exists a board in 'vmoved' being favorable for V
            elif (any(map(lambda x:([x,1] in child),vmoved))):
                cl.append([b,1])    # V win
            # follwoing draw case does not occur in this game
            else:
                cl.append([b,0])
            cl =  cl + child
    return cl

# list of scores starting from a board 'b' and a vertical domino
def vretrieve(board):
    # list of vertical moved boards from a board 'board'
    vmoved = list(map(lambda x:vfill(board,x),
                          map(lambda x:x[1],
                              filter(lambda x:x[0],
                                     map(lambda y:[vcheck(board,y),y], range(16))))))
    cl = []
    if (vmoved != []):
        # 'cl' is the list of all pair of hmoved board and its score
        for b in vmoved:
            # list of scores starting from a board 'b'
            child=hretrieve(b)
            # list of horizontal moved boards from a board 'b'
            hmoved = list(map(lambda x:hfill(b,x),
                 map(lambda x:x[1],
                     filter(lambda x:x[0],
                            map(lambda y:[hcheck(b,y),y], range(16))))))
            # all boards in 'vmoved' are favorable for H
            # that is there is no chance to win for V
            if (all(map(lambda x:([x,1] in child),hmoved))):
                cl.append([b,1])      # V win
            # there exists a board in 'hmoved' being favorable for H
            elif (any(map(lambda x:([x,-1] in child),hmoved))):
                cl.append([b,-1])     # H win
            # follwoing draw case does not occur in this game                
            else:
                cl.append([b,0])
            cl = cl + child
    return cl

def texprint(latex,section,f):
    print('\\section{'+section+' ('+str(len(latex))+'cases)}',file=f)
    l = 0
    c = 0
    for l0, l1, l2 in latex:
        if (l == 0)and(c == 0):
            print('\\begin{tabular}{ccccc}',file=f)
        print('\\begin{tabular}{c}',file=f)
        print(l0,'\\\\',file=f)
        print(l1,'\\\\',file=f)
        print(l2,'\\\\',file=f)
        print('\\end{tabular}',file=f)
        if (c < 4):
            print('&\n',file=f)
            c = c + 1
        else:
            print('\\\\\n',file=f)
            c = 0
            l = l + 1
            if (l == 7):
                print('\\end{tabular}',file=f)
                l = 0
    # print('c,l',c,l,section,len(latex),len(latex)%5,int(len(latex)/5)%7)
    if (l != 0) or (c != 0):
        while (c < 4):
            print('&\n',file=f)
            c = c + 1
        print('\\\\\n',file=f)
        print('\\end{tabular}',file=f)
    print('\\newpage',file=f)
