#!/usr/bin/env python3

from score import score_slide_transition
from slide import Slide
from OrderedHashSet import OrderedHashSet
from random import randint
from time import time

def stupid_pairing(vertical):
    """
    Naive pairing of vertical photos
    doesn't counting tag combination
    """
    print('vertical len:', len(vertical))
    pairs = [(vertical[i], vertical[i + 1]) for i in range(0, len(vertical), 2)]
    print('v pairs:', set([len(pair) for pair in pairs]))
    return [{
                'is_vertical': False,
                'num': (a['num'], b['num']),
                'tags': set(a['tags'] | b['tags'])
            } for a, b in pairs]

def pair_max_tag_count(vertical: list) -> list:
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
                'tags': set(a['tags'] | b['tags'])
            } for a, b in pairs]

def pair_min_tag_intersection(vertical: list) -> list:
    """
    Pairs vertical photos to have minimum tag intersection for two photos in 
    slide
    """
    pairs = []
    while len(vertical) > 0:
        print('\rremaining:', len(vertical), end='')
        a = vertical.pop()
        max_len = 0
        max_index = 0
        for i, b in enumerate(vertical):
            len_tags = len(b['tags'] & a['tags'])
            if len_tags == 0:
                max_index = i
                break
        b = vertical.pop(max_index)
        pairs.append((a, b))
    print('')
    return [{
                'is_vertical': False,
                'num': (a['num'], b['num']),
                'tags': set(a['tags'] | b['tags'])
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
    # return horisontal + stupid_pairing(vertical)
    # return stupid_pairing(vertical) + horisontal
    # return horisontal + pair_max_tag_count(vertical)
    # return horisontal + pair_greedy_max_tag_count(vertical)
    return horisontal + pair_min_tag_intersection(vertical)

def order_slides(slides, _):
    """
    Ordering slides with maximisation of score function
    O(n) ~= n**2
    or O(n) = n*batch_size with lower score
    """
    N = len(slides)

    # Slides with more tags apper closer to begin
    slides = sorted(slides, key=lambda slide: len(slide['tags']))

    # Change to trade speed for score
    batch_size = 10000
    res = []
    slide = stupid_select_first_slide([slides])
    cur_score = 0
    while len(slides) > 0:
        START_TIME = time()
        max_score = 0
        max_index = 0
        for i, s in enumerate(slides):
            # score = score_slide_transition(slide, s)
            score = len(slide['tags'] & s['tags'])
            if score > max_score:
                max_score = score
                max_index = i
            if i >= batch_size:
                break
        
        cur_score += max_score
        avg_score = 0 if len(res) == 0 else cur_score / len(res)
        print('\rremaining: ', len(slides), end=' ')
        print('max_score: {} avg score: {:.3f} estimate: {:.3f}'.format(max_score, avg_score, avg_score * N) , end='')
        END_TIME = time()
        run_time = END_TIME - START_TIME
        print('time: {:.3f} estimate: {:.3f}'.format(run_time, (run_time) * len(slides)), end='')

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
    for tag in tag_map:
        tag_map[tag] = sorted(tag_map[tag], key=lambda slide: len(slide['tags']))
    return tag_map

def order_slides_similar_tag_lookup(slides, native_score):
    """
    This method is best fit for input files with large number of tags and
    small tag per slide number and slides with simillar tag number.
    So the it should be tag_per_slide * slide_per_tag * n << n**2
    to use this method effectively
    Also, it can have minor fluctuations in score because of getting element
    from hash map when slides with simillar tags aren't found
    """
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
    slide_dict.pop(slide['num'])
    while len(slide_dict) > 0:
        max_score = -1
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
                    # uncomment to trade score for speed
                    # break
            # some greedy shit
            # if max_score > 3:
            #     break

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
            while max_index == -1 or max_index not in slide_dict:
                max_index = next(iter(slide_dict))

        cur_score += max_score if max_score > 0 else 0

        slide = slide_dict.pop(max_index)

    print('')
    return res

def group_photos_to_slides(photos, score):
    """
    Groups photos to achieve highest interest score
    """
    grouped_photos = group_vertical_photos(photos)
    res = order_slides(grouped_photos, score)
    # res = order_slides_similar_tag_lookup(grouped_photos, score)
    if res != None:
        print(set([len(slide['num']) if slide['num'].__class__ == set else 1 for slide in res]))
        return res
    return photos
