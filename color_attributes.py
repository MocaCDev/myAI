import json
import os

class C_Attr:
    def __init__(self):
        if os.path.isfile('image_data.json'):
            self.data = json.load(open('image_data.json', 'r'))
        else:
            self.data = {
                # These will be an array of arrays
                # Each array within the array will contain an
                # R, G, B value
                'average_black_color': [],
                'average_red_color': [],
                'average_orange_color': [],
                'average_gray_color': []
            }
        
    # generate rgb value
    def gen_rgb(R, G, B):
        return R*65536 + G*256 + B
    
    # Background should be relatively dark
    black = [
        # low               max
        gen_rgb(0, 0, 0), gen_rgb(65, 60, 65)
    ]
    
    # Based off the Visible Light Spectrum
    red = [
        gen_rgb(120, 0, 0), gen_rgb(255, 0, 0)
    ]
    
    # There can, and will, be some orange
    orange = [
        gen_rgb(200, 60, 0), gen_rgb(255, 100, 0)
    ]
    
    # Exclude all gray from image
    gray = [
        gen_rgb(90, 110, 120), gen_rgb(128, 128, 128)
    ]
    
    def is_in_range(self, values: tuple, color: list, type: str) -> bool:
        max_length = len(color)-1
        
        max = color[max_length]
        low = color[0]
        
        RGB_VAL = C_Attr.gen_rgb(values[0], values[1], values[2])
        
        if RGB_VAL >= low and RGB_VAL <= max:
            if type == 'black': 
                self.data['average_black_color'].append([
                    int(values[0]), int(values[1]), int(values[2])
                ])
            if type == 'red':
                self.data['average_red_color'].append([
                    int(values[0]), int(values[1]), int(values[2])
                ])
            if type == 'orange':
                self.data['average_orange_color'].append([
                    int(values[0]), int(values[1]), int(values[2])
                ])
            if type == 'gray':
                self.data['average_gray_color'].append([
                    int(values[0]), int(values[1]), int(values[2])
                ])
            return True

        return False

    def finished(self):
        ftw = open('image_data.json', 'w')
        ftw.write(json.dumps(
            self.data,
            indent=2,
            separators=(None),
            sort_keys=True,
        ))
        ftw.close()