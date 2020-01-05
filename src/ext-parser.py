import datetime
import re
import sqlite3 as sqldb

now = datetime.datetime.now()
strNowTime = now.strftime('%d%m%Y_%H%M%S')

# initialize local db to obtain required data for YNAB
conn = sqldb.connect('db/ynablocal.db')
sqlSelect = '''
SELECT a.nombre AS 'acreedor', c.nombre AS 'categoria', sc.nombre AS 'subcategoria', p.descripcion AS 'palabraclave' 
FROM palabraclave p
JOIN acreedor a ON p.acreedor=a.id
JOIN subcategoria sc ON p.subcategoria=sc.id
JOIN categoria c ON sc.categoria=c.id
WHERE p.descripcion = ?
'''

# for now files are deposited on fixed path locations
inputFilePath = './in/extracto-cuenta.txt'
outputFilePath = f'./out/extracto-csv-{strNowTime}.csv'

file = open(inputFilePath)
filelines = file.readlines()
print(f'lines array length {len(filelines)}')
movs = filelines[28:-10]
# create csv file and add header row
csvfile = open(outputFilePath, 'w')
csvfile.write("Date,Payee,Category,Memo,Outflow,Inflow\n")

for line in movs:
    if line.strip():
        # print(line.strip())
        # using a regex to clear whitespace and organize data
        newline = re.sub(' {2,}', ';', line.rstrip().strip())
        try:
            # ignore rows that don't start with a number value
            # doing this validation because the txt adds a page foot in case there are enough rows
            int(newline[0:2])
            #print(newline)
            aux = newline.split(';')
            # unpack the data needed
            fecha, _, _, descripcion, importe_debito, importe_credito, _, _ = aux
            # delete any comma separator from monetary variables
            debito = importe_debito.replace(',', '')
            credito = importe_credito.replace(',', '')
            #print(f'{fecha}, {descripcion}, {debito}, {credito}')
            acreedor = categoria = subcategoria = ''

            # connect to local database and query remaining required data
            with conn:
                cursor = conn.cursor()
                cursor.execute(sqlSelect, (descripcion,))
                row = cursor.fetchone()
                if row is not None:
                    #print(row)
                    acreedor, categoria, subcategoria, _ = row

            # format the csv row to insert on its file
            csvstr = f"{fecha},{acreedor},{categoria}: {subcategoria},{descripcion},{debito},{credito}\n"
            print(csvstr)
            csvfile.write(csvstr)

        except ValueError:
            continue
