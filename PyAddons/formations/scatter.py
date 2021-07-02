import math
from random import uniform
from formations.vec import Vec3

# TODO: Should these swap Z and Y in calulations?

def arc(count, x,y,z, r, start=0.0, end=90.0):
    r"""Calculate the points along an circular arc

    Parameters
    ----------
    count: int
        The number of points to generate
    x,y,z: float,float,float
        the center point/origin
    r:radius
    start: float=0, optional
        the angle to start at in degrees
    end: float=360, optional
        the angle to end at in degrees
    """
    a_start = math.radians(start)
    a_diff = (math.radians(end)-a_start)
    for i in range(0,count):
        angle=(i/count)*a_diff + a_start
        yield Vec3(x+math.cos(angle)*r, y, z+math.sin(angle)*r)


def line(count, start_x,start_y,start_z, end_x,end_y,end_z, random=False):
    r"""Calculate the points along a line
    
    Parameters
    ----------
    count: int
        The number of points to generate
    start_x,start_y,start_z: float,float,float
        the start point/origin
    end_x,end_y,end_z: float,float,float
        the end point
    """

    v1 =  Vec3(start_x, start_y, start_z)
    v2 =  Vec3(end_x, end_y, end_z)

    v = v2 - v1
    d = v.length()
    u = v.divide(d)
   
    delta = u * (d/(count-1))
    for i in range(0,count):
        if random:
            yield v1 + (delta * uniform(0,count))
        else:
            yield v1 + (delta * i)


"""
Calculate the points in a grid from a center point
"""
def rect_fill(cw, cd, x, y, z, w, d, random=False):
    return box_fill(cw, 1, cd, x, y, z, w, 1, d, random)
    # front = z-d/2
    # # bottom = z+h/2
    # left = x-w/2
    # # right = x+w/2
    # w_diff = w/(cw-1)
    # d_diff = d/(cd-1)

    # for row in range(0,cd):
    #     _z = front + row * d_diff
    #     for col in range(0,cw):
    #         _x = left + col * w_diff
    #         yield Vec3(_x,y,_z)

"""
Calculate the points in a box from a center point
"""
def box_fill(cw, ch, cd, x, y, z, w, h, d, random=False):
    front = z-d/2
    bottom = y-h/2
    left = x-w/2
    # right = x+w/2
    if cw >1:
        w_diff = w/(cw-1)
    else: 
        w_diff = 1
    if ch >1:
        h_diff = h/(ch-1)
    else: 
        h_diff = 1
        bottom = y
    if cd >1:
        d_diff = d/(cd-1)
    else: 
        d_diff = 1
    for layer in range(0,ch):
        if random:
            _y =  bottom + uniform(0,ch) * h_diff
        else:
            _y =  bottom + layer * h_diff
        for row in range(0,cd):
            if random:
                _z =  front + uniform(0,cd) * d_diff
            else:
                _z = front + row * d_diff
            for col in range(0,cw):
                if random:
                    _x =  left + uniform(0,cw) * w_diff
                else:
                    _x = left + col * w_diff
                yield Vec3(_x,_y,_z)


"""
Calculate the points in an arc ring
"""
def ring(ca, cr, x,y,z, inner_r, outer_r, start=0.0, end=90.0, random=False):
    # y should be odd
    a_start = math.radians(start)
    a_end = math.radians(end)
    a_diff = (a_end-a_start)
    r_diff = (outer_r - inner_r) / (cr-1)
    for r in range(0, cr):
        dist = inner_r + (r* r_diff)
        for i in range(0,ca):
            if random:
                angle = uniform(a_start, a_end)
            else:
                angle=(i/ca)*a_diff + a_start
            yield Vec3(x+math.cos(angle)*dist, y, z+math.sin(angle)*dist)
"""
Calculate the points in an arc ring with varying density
    
"""
def ring_density(counts, x,y,z, inner_r, outer_r, start=0.0, end=90.0, random=False):
    # y should be odd
    a_start = math.radians(start)
    a_end = math.radians(end)
    a_diff = (a_end-a_start)
    r_diff = (outer_r - inner_r) / (len(counts)-1)
    for r in range(0, len(counts)):
        dist = inner_r + (r* r_diff)
        ca = counts[r]
        print(f'count {ca}')
        for i in range(0,ca):
            if random:
                angle = uniform(a_start, a_end)
            else:
                angle=i*(a_diff/ca) + a_start
            yield Vec3(x+math.cos(angle)*dist, y, z+math.sin(angle)*dist)

"""
Calculate the points in a sphere
"""
def sphere(count, x,y,z, r, outer=0, top_only=False, ring=False):
    # y should be odd
    origin = Vec3(x,y,z)
    for _ in range(0,count):
        yield origin.rand_offset(r, outer, top_only, ring)
    