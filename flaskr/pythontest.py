import csv
fields=['Genre','Count']
data=[['Horror',5],['Action',7]]
with open('totalGenreCount.csv', mode='w')as genreInfo:
        infoWriter=csv.writer(genreInfo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        infoWriter.writerow(fields)
        infoWriter.writerows(data)
print("Hi");