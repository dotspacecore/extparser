import datetime
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
movs = filelines[28:-36]

for line in movs:
    if line.strip():
        print(line.strip())
        # dividir la cadena por tabulación
        # TODO: nuevo formato no está tabulado
        aux = line.strip().split('\t')
        print(aux)
        # desempaquetar los datos relevantes del arreglo en distintas variables
        fecha, _, _, descripcion, org_debito, org_credito, _, _, _ = aux
        # sacar el separador de miles de los montos
        debito = org_debito.replace('.', '')
        credito = org_credito.replace('.', '')
        print(f'{fecha}, {descripcion}, {org_credito}, {org_debito}')
