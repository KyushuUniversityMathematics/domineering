00Readme.txt

Do 'make texmain'

texmain.pdf : all board lists with scores

counting.csv : reduced boardlist (zv2u2,zh2u2)
   boardnumber, score
   313 cases for after V moves
   175 cases for after H moves
   488 cases
counting0.csv : full boardlist (zv2u, zh2u)
   boardnumber, score
   1192 cases for after V move
   1250 cases for after H move
   2442 cases
= counting.bin : variable reduce : list of score and board [s,b]

hash.csv : reduced link : list of [b,br]
   boardnumber, reduced-boardnumber
    879 cases for after V move
   1075 cases for after H move
   1954 cases

counting00.csv : list f [turn, no. of domino, board,
                         v=score, v2=score %, v3=-1,0,1] (z2u2)
   488 cases
= sample44.bin : z2u2 (v3=0) : there are chance of win and lose

countinglib.py : library functions
counting.py : creating counting.csv, couting0.csv, hash.csv
                       counting.bin, sample44.bin, counting00.csv

printing.py : creating counting.tex

texmain.tex : manually created main tex file including 'counting.tex'

#### under construction
printperfect.py : obsolated
	checking counting.bin
shrink2.py : obsolated
	converting counting.csv to counting.bin for perfectplayer's np.array
forplayer2.py :
forplayer.py :
monte1.py :
monte2.py :
training.py :
