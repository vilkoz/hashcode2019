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

def pair_max_tag_count(vertical):
    """
    Pair to get max tag count in one slide
    complexity: n**2
    """
    pairs = []
    while len(vertical) > 0:
        print('\rremaining:', len(vertical), end='')
        a = vertical.pop()
        max_len = 0
        max_index = 0
        for i, b in enumerate(vertical):
            len_tags = len(b['tags'] & a['tags'])
            if len_tags > max_len:
                max_len = len_tags
                max_index = i
        b = vertical.pop(max_index)
        pairs.append((a, b))
    print('')
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
    # return horisontal + pair_max_tag_count(vertical)

def order_slides(slides, _):
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
                tag_map[tag] = [s]
            else:
                tag_map[tag].append(s)
    return tag_map

def order_slides_similar_tag_lookup(slides, native_score):
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
                if s['num'] not in slide_dict:
                    continue
                iters += 1
                score = score_slide_transition(slide, s)
                if score > max_score:
                    max_score = score
                    max_index = s['num']
                    # break
            # some greedy shit
            if max_score > 1:
                break

        avg_score = 0 if len(res) == 0 else cur_score / len(res)
        print('\rremaining: ', len(slide_dict), end=' ')
        print('iters: ', iters, 'max_score:', max_score, 'avg score: ', avg_score, 'estimate:', avg_score * len(slides), end='')

        if avg_score * len(slides) < native_score and avg_score != 0:
            return None

        res.append(slide)
        if max_index == -1:
            for tag in slide['tags']:
                if len(tag_map[tag]) > 0:
                    s = tag_map[tag][0]
                    max_index = s['num']
                    break
            while max_index == -1 or max_index not in slide_dict:
                max_index = next(iter(slide_dict))
            # if max_index == -1:
            #     max_index = next(iter(slide_dict))

        cur_score += max_score

        slide = slide_dict.pop(max_index)

        # for tag in slide['tags']:
        #     for i, s in enumerate(tag_map[tag]):
        #         if s == slide:
        #             # tag_map[tag].pop(i)
        #             tag_map[tag].remove(s)
    print('')
    return res

def group_photos_to_slides(photos, score):
    """
    Groups photos to achieve highest interest score
    """
    grouped_photos = group_vertical_photos(photos)
    # res = order_slides(grouped_photos, score)
    res = order_slides_similar_tag_lookup(grouped_photos, score)
    if res != None:
        return res
    return photos
