## python load_data.py 394_individual_networks/*.txt

# DB configs
DATABASE_NAME = "glycogenes"
USER = "postgres"
PWD = "847468"
HOST = "127.0.0.1"
PORT = "5432"


#from fileinput import fileno
import sys
import psycopg2

import time
startTime = time.time()


conn = psycopg2.connect(database=DATABASE_NAME, 
                        user = USER, 
                        password = PWD, 
                        host = HOST, 
                        port = PORT)


cur = conn.cursor()

if len(sys.argv) < 2:
    raise Exception("Arguments missing: example arguments [filenames, data_source]")

total_files = len(sys.argv[1:])
print(f'######### Loading {total_files} files ##########')
fileno = 0
print(sys.argv[1:])

for filename in sys.argv[1:]:
    fileno += 1
    cell_type_id = filename.split('/')[-1].split('.')[0]

    file = open(filename, 'r')
    lines = file.readlines()

    total = len(lines)
    count = 0

    query = "INSERT INTO TF_Glyco VALUES "
    for line in lines:
        count += 1
        progress = int((count/total) * 10)
        print(f'##### {fileno}/{total_files} {cell_type_id}.txt [{ "#" * progress }{ "-" *(10 - progress)}]', end='\r')
        data = line.split('\t')
        query += f"('{cell_type_id}','{data[0]}','{data[1]}','{float(data[2])}'),"


    query = query.strip(',')
    cur.execute(query) 
    print('\n', end='\r')
    conn.commit()

executionTime = (time.time() - startTime)
print(f'Execution time: {executionTime//60} minutes and {executionTime%60} secs')
