import math, sys

class JPEG:
    
    MARKER_START = 0xFF
    MARKER_FLAGS = [
        0xD8, 0xC0, 0xC2, 0xC4,
        0xDB, 0xDD, 0xDA, 0xD0,
        0xE0, 0xFE, 0xD9
    ]
    MEANING = {
        MARKER_FLAGS[0]: 'start'
    }
    
    # JPEG image bytecode data
    bytecode_data = []
    index = 0
    
    # Start Of Image
    soi = False
    
    # Image Width
    iw = 0
    
    # Image Height
    ih = 0
    
    # XDensity
    XDen = 0
    
    # YDensity
    YDen = 0
    
    # Open a jpeg file
    def open_file(filename: str) -> None:
        JPEG.index = 0
        f: bytearray = open(filename, 'rb').read()
        
        for i in f:
            JPEG.bytecode_data.append(i)
        
        if JPEG.bytecode_data[0] == JPEG.MARKER_START:
            JPEG.index += 1
            if JPEG.bytecode_data[JPEG.index] in JPEG.MARKER_FLAGS:
                for i in JPEG.MARKER_FLAGS:
                    if i == JPEG.bytecode_data[JPEG.index]: 
                        if JPEG.MEANING[i] == 'start':
                            soi = True
                            break
    
    def decipher_JPEG_header() -> None:
        
        # Skip FF E0
        JPEG.index += 3
        JPEG.index += 11
        
        if JPEG.bytecode_data[JPEG.index] != 0x01:
            # Check two bytes deep, if still no, error.
            JPEG.index += 1
            if JPEG.bytecode_data[JPEG.index] != 0x01:
                print('Expected value: 0x01 at index {}'.format(JPEG.index))
                sys.exit(1)
            
        JPEG.XDen = JPEG.bytecode_data[JPEG.index]
        JPEG.index += 2
        
        if JPEG.bytecode_data[JPEG.index] != 0x01:
            print('Expected value: 0x01 at index {}'.format(JPEG.index))
            sys.exit(1)
        
        JPEG.YDen = JPEG.bytecode_data[JPEG.index]
        JPEG.index += 3
        
        # Start of RGB values
        if not JPEG.bytecode_data[JPEG.index] == JPEG.MARKER_START:
            print("Expected `MARKER_START` flag at index {}.".format(JPEG.index))
            sys.exit(1)
        
        JPEG.index += 1
    
    def obtain_pixel_array() -> list:
        
        pixel_array = []
        
        # The last two bytes indicate the end of the file.
        while JPEG.index < len(JPEG.bytecode_data)-2:
            current_rgb = []
            
            for i in range(3):
                current_rgb.append(JPEG.bytecode_data[JPEG.index])
                JPEG.index += 1
            
            pixel_array.append(tuple(current_rgb))
        
        # We just want to know if the last byte is 0xD9.
        if JPEG.bytecode_data[JPEG.index] != int(0xD9):
            # Check 2 bytes deep, if still no, error.
            JPEG.index += 1
            if JPEG.bytecode_data[JPEG.index] != int(0xD9):
                print('Expected EOF byte 0xD9 at index {}'.format(JPEG.index))
                sys.exit(1)

        return pixel_array

JPEG.open_file("testIMG.jpg")
JPEG.decipher_JPEG_header()
array = JPEG.obtain_pixel_array()
print(array)

JPEG.open_file("testIMG2.jpg")
JPEG.decipher_JPEG_header()
JPEG.obtain_pixel_array()
