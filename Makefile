init:
	pip3 install -r requirements.txt

test:
	python3 setup.py nosetests
