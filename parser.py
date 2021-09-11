import os
import csv
from pixel import Pixel

def main():
    create_csv('flip')
    return 0

def create_csv(path):
    
    i = 0
    fields = ['n', 'grey', 'avgColor(hex)', 'filePath']
    with open('photos.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields)

        for root, dirs, files in os.walk(path):
            for filename in files:
                row = []
                newPixel = Pixel(path+'/'+filename, 5, None, None)
                i+=1
                row.append(i)
                row.append(newPixel.GreyPool)
                row.append(newPixel.avgColor)
                row.append(newPixel.path)
                csvwriter.writerow(row)

class Parser:
    pixelDict = {}
    csv = None

    def __init__(self, csvFile):
        self.csv = csvFile

    def create_pixel_list(self, multiple):
        self.pixelDict['d'] = []
        self.pixelDict['dl'] = []
        self.pixelDict['ld'] = []
        self.pixelDict['l'] = []

        with open(self.csv, 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                dictRow = dict(row)
                newPixel = Pixel(dictRow['filePath'], multiple, dictRow['avgColor(hex)'], dictRow['grey'])
                if dictRow['grey'] == 'd':
                    self.pixelDict['d'].append(newPixel)
                elif dictRow['grey'] == 'dl':
                    self.pixelDict['dl'].append(newPixel)
                elif dictRow['grey'] == 'ld':
                    self.pixelDict['ld'].append(newPixel)
                else:
                    self.pixelDict['l'].append(newPixel)
        
        return self.pixelDict


if __name__ == "__main__":
    main()
