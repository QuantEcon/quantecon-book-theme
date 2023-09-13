all: 
	rm -rf /home/jacob/.local/lib/python3.8/site-packages/quantumghent_book_theme*
	rm -rf ./build
	rm -rf ./quantumghent-book-theme/static
	web-compile
	pip install /home/jacob/tutorials/QG/quantumghent-book-theme/
