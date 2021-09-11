from parser import Parser
from image import BigImage

def main():
    parser = Parser('photos.csv')
    pixelDict = parser.create_pixel_list(5)
    image = BigImage('flip3.jpg',pixelDict)
    mosaic = image.build_mosaic(1000)
    #image.test()

    return 0


if __name__ == "__main__":
    main()