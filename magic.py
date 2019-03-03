#!/usr/bin/env python3

from score import score_slide_transition
from slide import Slide
from OrderedHashSet import OrderedHashSet

def stupid_pairing(vertical):
    """
    Naive pairing of vertical photos
    doesn't counting tag combination
    """
    print('vertical len:', len(vertical))
    pairs = [(vertical[i], vertical[i + 1]) for i in range(0, len(vertical), 2)]
    return [{
                'is_vertical': False,
                'num': (a['num'], b['num']),
                'tags': set(a['tags'] & b['tags'])
            } for a, b in pairs]

def stupid_select_first_slide(slides_p):
    """
    Naive first slide selection
    """
    slides = slides_p[0]
    res = slides.pop(0)
    return res

def group_vertical_photos(photos):
    vertical = [x for x in photos if x['is_vertical']]
    horisontal = [x for x in photos if not x['is_vertical']]
    return horisontal + stupid_pairing(vertical)

def order_slides(slides):
    """
    Ordering slides with maximisation of score function
    O(n) ~= n**2
    """
    res = []
    slide = stupid_select_first_slide([slides])
    while len(slides) > 0:
        print('remaining: ', len(slides))
        max_score = 0
        max_index = 0
        for i, s in enumerate(slides):
            score = score_slide_transition(slide, s)
            if score > max_score:
                max_score = score
                max_index = i
        res.append(slide)
        slide = slides.pop(max_index)
    res.append(slide)
    return res

def form_tag_map(slides):
    tag_map = {}
    for s in slides:
        for tag in s["tags"]:
            if tag not in tag_map:
                tag_map[tag] = OrderedHashSet()
            tag_map[tag].add(s)
    return tag_map

def order_slides_similar_tag_lookup(slides):
    slides = [Slide(s) for s in slides]
    tag_map = form_tag_map(slides)

    print("tag count:", len(tag_map))
    print("slide count:", len(slides))
    print("avg slide per tag count:", sum([len(tag_map[x]) for x in tag_map.keys()]) / len(tag_map))
    print("avg tag per slide count:", sum([len(x['tags']) for x in slides]) / len(slides))
    
    cur_score = 0
    slide_dict = {x['num']: x for x in slides}
    res = []
    slide = stupid_select_first_slide([slides])
    while len(slide_dict) > 0:
        max_score = 0
        max_index = -1
        iters = 0
        for tag in slide['tags']:
            for s in tag_map[tag]:
                # if s['num'] not in slide_dict:
                #     continue
                iters += 1
                score = score_slide_transition(slide, s)
                if score > max_score:
                    max_score = score
                    max_index = s['num']
                    break
            # some greedy shit
            if max_score != 0:
                break

        avg_score = 0 if len(res) == 0 else cur_score / len(res)
        print('\rremaining: ', len(slide_dict), end=' ')
        print('iters: ', iters, 'max_score:', max_score, 'avg score: ', avg_score, 'estimate:', avg_score * len(slides), end='')

        res.append(slide)
        if max_index == -1:
            for tag in slide['tags']:
                if len(tag_map[tag]) > 0:
                    s = tag_map[tag][0]
                    max_index = s['num']
                    break
            # while max_index == -1 or max_index not in slide_dict:
            #     max_index = next(iter(slide_dict))
            if max_index == -1:
                max_index = next(iter(slide_dict))

        cur_score += max_score

        slide = slide_dict.pop(max_index)

        for tag in slide['tags']:
            for i, s in enumerate(tag_map[tag]):
                if s == slide:
                    # tag_map[tag].pop(i)
                    tag_map[tag].remove(s)
    # res.append(slide)
    print('')
    return res

def group_photos_to_slides(photos):
    """
    Groups photos to achieve highest interest score
    """
    photos = group_vertical_photos(photos)
    # photos = order_slides(photos)
    photos = order_slides_similar_tag_lookup(photos)
    return photos
