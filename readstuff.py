import gzip
import pandas as pd

with open('Box_Scores.csv', 'rb') as fd:
    gzip_fd = gzip.GzipFile(fileobj=fd)
    print(gzip_fd)
    data = pd.read_csv(gzip_fd,header=0,encoding = 'unicode_escape')
