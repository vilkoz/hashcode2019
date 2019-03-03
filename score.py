#!/usr/bin/env python3
from output import pretty_print

def score_slide_transition(slide1, slide2):
    """
    Scores pair of slides depending on tags
    """
    tags1 = set(slide1['tags'])
    tags2 = set(slide2['tags'])
    common_num = len(tags1 & tags2)
    diff_1 = len(tags1 - tags2)
    diff_2 = len(tags2 - tags1)
    return min(common_num, diff_1, diff_2)

def score_slide_list(slides):
    # pretty_print([{'tags': list(x['tags']), 'num': x['num']} for x in slides])
    score = 0
    for i, s in enumerate(slides):
        if i == len(slides) - 1:
            continue
        score += score_slide_transition(s, slides[i+1])
    # pretty_print(pairs)
    return score
