#!/usr/bin/env python3
from sys import argv
from json import dumps
from score import score_slide_list
from magic import group_photos_to_slides

def parse_input(f):
    """
    Parses input in format
    2
    H 3 cat beach sun
    V 2 selfie smile
    or
    Number_of_photos
    Orientation Number_of_tags tag1 tag2 tag3
    """
    with open(f, 'r') as f:
        s = f.read()
    lines = s.split('\n')
    photo_num = int(lines[0])
    lines.pop(0)
    photos = []
    for i in range(photo_num):
        photo_params_list = lines.pop(0).split(' ')
        photo = {}
        photo['is_vertical'] = photo_params_list.pop(0) == 'V'
        photo['num'] = i
        photo['tags'] = []
        for __ in range(int(photo_params_list.pop(0))):
            photo['tags'].append(photo_params_list.pop(0))
        photo['tags'] = set(photo['tags'])
        photos.append(photo)
    return photos

def main():
    photos = parse_input(argv[1])
    print('score:', score_slide_list(photos))
    photos = group_photos_to_slides(photos)
    print('score:', score_slide_list(photos))

if __name__ == "__main__":
    main()
