# barcode
Repo for barcode

REQUIREMENTS:

Devlopment uisng Python3.6.7, although other versions of Python3 may work.

DATABASE:
Three tables exist, Sample, Gene, GeneQual.

The makedb.py shows how query functions work. I am adding some examples to the the Wiki.

INSTALLATION:
1. git clone https://github.com/jaredcara/barcode.git
2. cd barcode/app
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. *Copy the app.db file from the google drive to barcode/app directory*

To run the application:
7. flask run

To perform command line queries:
8. flask shell 
9. *do something*

