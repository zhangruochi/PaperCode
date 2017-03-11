import gzip

f = gzip.open('file.csv.gz', 'rb')
file_content = f.read()
print(file_content)
f.close()