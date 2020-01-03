import datetime
import re
import sqlite3 as sqldb

now = datetime.datetime.now()
strNowTime = now.strftime('%d%m%Y_%H%M%S')

conn = sqldb.connect('db/ynablocal.db')
sqlSelect = '''
SELECT a.nombre AS 'acreedor', c.nombre AS 'categoria', sc.nombre AS 'subcategoria', p.descripcion AS 'palabraclave' 
FROM palabraclave p
JOIN acreedor a ON p.acreedor=a.id
JOIN subcategoria sc ON p.subcategoria=sc.id
JOIN categoria c ON sc.categoria=c.id
WHERE p.descripcion = ?
'''

inputFilePath = './in/extracto-cuenta.txt'
outputFilePath = f'./out/extracto-csv-{strNowTime}.csv'

file = open(inputFilePath)
filelines = file.readlines()
print(f'lines array length {len(filelines)}')
movs = filelines[28:-10]

for line in movs:
    if line.strip():
        # print(line.strip())
        # reemplazar los espacios múltiples por un separador y dividir
        newline = re.sub(' {2,}', ';', line.rstrip().strip())
        try:
            # verificar si la línea empieza con un número (parte de la fecha de transacción)
            # para filtrar el pie de página insertado en el txt en caso de ser multipágina
            int(newline[0:2])
            print(newline)
            aux = newline.split(';')
            # desempaquetar los datos relevantes del arreglo en distintas variables
            fecha, _, _, descripcion, importe_debito, importe_credito, _, _ = aux
            # sacar el separador de miles de los montos
            debito = importe_debito.replace(',', '')
            credito = importe_credito.replace(',', '')
            print(f'{fecha}, {descripcion}, {debito}, {credito}')
        except ValueError:
            continue
