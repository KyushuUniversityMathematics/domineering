all:
	echo 'make model1'
model1-10: ./dump/model1_00010.h5
	python training_model1.py
	python testing_model16.py
model2-10: ./dump/model2_00010.h5
	python training_model2.py
	python testing_model4x4.py
model1-1000: ./dump/model1_00010.h5
	python training_model1.py 1000
	python testing_model16.py model1 1000
model2-1000: ./dump/model2_00010.h5
	python training_model2.py 1000
	python testing_model4x4.py model2 1000
model1-2000: ./dump/model1_00010.h5
	python training_model1.py 2000
	python testing_model16.py model1 2000
model2-2000: ./dump/model2_00010.h5
	python training_model2.py 2000
	python testing_model4x4.py model2 2000
model1-9000: ./dump/model1_00010.h5
	python training_model1.py 9000
	python testing_model16.py model1 9000
model2-9000: ./dump/model2_00010.h5
	python training_model2.py 9000
	python testing_model4x4.py model2 9000
batch: model1-10 model2-10 model1-1000 model2-1000 model1-2000 model2-2000
	echo 'model1-10 model2-10 model1-1000 model2-1000 model1-2000 model2-2000'
batchall: model1-9000 model2-9000
	echo 'model1-9000 model2-9000'
clean:
	rm -rf *~ *.aux *.log __pycache__
veryclean:
	rm ./dump/*.pdf ./dump/*.csv ./dump.h5
open:
	open ./dump/model1_00010.pdf


