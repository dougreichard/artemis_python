use pyo3::class::PyIterProtocol;
use pyo3::prelude::*;
use rand::thread_rng;
use rand::Rng;
use std::option::Option;

use super::sbs_math::vec3::Vec3;

#[pyclass]
pub struct Arc {
    count: usize,
    x: f64,
    y: f64,
    z: f64,
    r: f64,
    //    start: f64,
    //    end: f64,
    random: bool,
    // state
    current: usize,
    a_start: f64,
    a_end: f64,
    a_diff: f64,
}

#[pymethods]
impl Arc {
    #[new]
    #[args(start = "0.0", end = "90.0", random = "false")]
    fn new(count: usize, x: f64, y: f64, z: f64, r: f64, start: f64, end: f64, random: bool) -> Self {
        let a_start = -start.to_radians();
        let a_end = -end.to_radians();
        let a_diff = (a_end - a_start) / (count-1) as f64;
        Arc {
            count,
            x,
            y,
            z,
            r,
            random,
            a_start,
            a_end,
            a_diff,
            current: 0,
        }
    }
}

#[pyproto]
impl PyIterProtocol for Arc {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<Vec3> {
        if slf.current < slf.count {
            let angle = if slf.random {
                let mut rng = thread_rng();
                let all = rand::distributions::Uniform::new_inclusive(slf.a_start, slf.a_end);
                rng.sample(all)
            } else {
                slf.current as f64 * slf.a_diff + slf.a_start
            };
            slf.current+=1;

            Some(Vec3::new(
                slf.x + f64::cos(angle) * slf.r,
                slf.y,
                slf.z + f64::sin(angle) * slf.r,
            ))
        } else {
            None
        }
    }
}




#[pyclass]
pub struct Line {
    count: usize,
    start: Vec3,
 //   end: Vec3,
    random: bool,
    // state
    current: usize,
    delta: f64,
    unit: Vec3
}

#[pymethods]
impl Line {
    #[new]
    #[args(random = "false")]
    fn new(count: usize, xs: f64, ys: f64, zs: f64, xe: f64, ye: f64, ze: f64, random: bool) -> Self {
        let start = Vec3::new(xs,ys,zs);
        let end = Vec3::new(xe,ye,ze);
        let diff = end.sub(&start);
        let length = diff.length();
        let unit = diff.divide(length);
        let delta = if random {
            length
        } else {
            length/((count-1) as f64)
        };

        Line {
            count,
            start,
           // end,
            random,
            delta,
            unit,
            current: 0,
        }
    }
}

#[pyproto]
impl PyIterProtocol for Line {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<Vec3> {
        if slf.current < slf.count {
            let cur_delta = if slf.random {
                let mut rng = thread_rng();
                let all = rand::distributions::Uniform::new_inclusive(0_f64, slf.delta);
                rng.sample(all)
            } else {
                slf.current as f64 * slf.delta
            };
            slf.current+=1;
            Some(slf.start.add(&slf.unit.mulf64(cur_delta)))
        } else {
            None
        }
    }
}

/*
#[pyclass]
pub struct Box {
    cw: usize,
    ch: usize,
    cd: usize,
    random: bool,
    // state
    current: usize,
    left: f64,
    bottom: f64,
    front: f64,
    delta_w: f64,
    delta_h: f64,
    delta_d: f64
}

#[pymethods]
impl Box {
    #[new]
    #[args(random = "false")]
    fn new(cw: usize, ch: usize, cd: usize, x: f64, y: f64, z: f64, w: f64, h: f64, d: f64, random: bool) -> Self {
        let front = z-d/2.0;
        let bottom = y-h/2.0;
        let left = x-w/2.0;

        Box {
            cw,
            ch,
            cd,
            random,
            front,
            bottom,
            left,
            current: 0,
        }
    }
}

#[pyproto]
impl PyIterProtocol for Box {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<Vec3> {
        if slf.current < slf.count {
            let cur_delta = if slf.random {
                let mut rng = thread_rng();
                let all = rand::distributions::Uniform::new_inclusive(0_f64, slf.delta);
                rng.sample(all)
            } else {
                slf.current as f64 * slf.delta
            };
            slf.current+=1;
            Some(slf.start.add(&slf.unit.mulf64(cur_delta)))
        } else {
            None
        }
    }
}
*/

/* 

def box_fill(cw, ch, cd, x, y, z, w, h, d, random=False):
    r"""Calculate the points within a box
        
    Parameters
    ----------
    cw: int
        The number of points to generate for each line width (x)
    ch: int
        The number of points to generate for each line height (y)
    cd: int
        The number of points to generate for each line width (z)
    x,y,z: float,float,float
        the start point/origin
    w: float
        the width
    h: float
        the height
    d: float
        the depth
    random: bool
        when true pointw will be randomly placed
        when false points will be evenly placed
    """
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
*/


#[pyclass]
struct Ring {
    cr: u32,
    ca: u32,
    origin: Vec3,
    outer: f64,
    inner: f64,
    a_start: f64,
    a_end: f64,
    a_diff: f64,
    r_diff: f64,
    random: bool,
    current: u32
}

#[pymethods]
impl Ring {
    #[new]
    #[args(inner="0.0", random="false")]
    fn new(cr: u32, ca: u32, x: f64, y: f64, z: f64,  outer: f64, inner: f64, start: f64, end: f64, random: bool)-> Self {
        let a_start = -start.to_radians();
        let a_end = -end.to_radians();
        let a_diff = (a_end - a_start)/ (ca-1) as f64;
        let r_diff = (outer - inner) / (cr-1) as f64;

        let origin = Vec3::new(x,y,z);
        Ring{cr, ca,origin,inner,outer, a_start, a_end, a_diff, r_diff, random, current: 0}
    }
}

#[pyproto]
impl PyIterProtocol for Ring {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<Vec3> {
        if slf.current < (slf.cr*slf.ca) {
            let d = (slf.current as f64/slf.ca as f64) as f64;
            let r=d.trunc();
            let a = d.fract() * slf.ca as f64;
            let dist = slf.inner + (r* slf.r_diff);
            let angle = if slf.random {
                let mut rng = thread_rng();
                let all = rand::distributions::Uniform::new_inclusive(slf.a_start, slf.a_end);
                rng.sample(all)
            }
            else{
                a*slf.a_diff + slf.a_start
            };

            Some(slf.origin.add(&Vec3::new(angle.cos()*dist, 0.0, angle.sin()*dist)))
            //Some(slf.origin.rand_offset(slf.r, slf.outer, slf.top_only, slf.ring))
        } else {
            None
        }
    
    }
}

/* 
  a_start = -math.radians(start)
    a_end = -math.radians(end)
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
*/

#[pyclass]
struct RingDensity {
    count: u32,
    origin: Vec3,
    outer: f64,
    inner: f64,
    a_start: f64,
    a_end: f64,
    a_diff: f64,
    r_diff: f64,
    random: bool,
    current: u32
}

#[pymethods]
impl RingDensity {
    #[new]
    #[args(inner="0.0", random="false")]
    fn new(count: u32, x: f64, y: f64, z: f64,  outer: f64, inner: f64, random: bool)-> Self {
        let a_start = -start.to_radians();
        let a_end = -end.to_radians();
        let a_diff = (a_end - a_start) / (count-1) as f64;
        let r_diff = (outer - inner) / (count-1) as f64;

        let origin = Vec3::new(x,y,z);
        RingDensity{count,origin,inner,outer,top_only, a_start, a_end, a_diff, r_diff, random, current: 0}
    }
}

#[pyproto]
impl PyIterProtocol for RingDensity {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<Vec3> {
        if slf.current < slf.count {
            Some(slf.origin.rand_offset(slf.r, slf.outer, slf.top_only, slf.ring))
        } else {
            None
        }
    
    }
}

/*
def ring_density(counts, x,y,z,  outer_r, inner_r=0, start=0.0, end=90.0, random=False):
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
*/


#[pyclass]
struct Sphere {
    count: u32,
    origin: Vec3,
    r: f64,
    outer: f64,
    top_only: bool,
    ring: bool,
    current: u32
}

#[pymethods]
impl Sphere {
    #[new]
    #[args(outer="0.0", top_only = "false", ring="false")]
    fn new(count: u32, x: f64, y: f64, z: f64, r: f64, outer: f64, top_only: bool, ring: bool)-> Self {
        let origin = Vec3::new(x,y,z);
        Sphere{count,origin,r,outer,top_only, ring, current: 0}
    }
}

#[pyproto]
impl PyIterProtocol for Sphere {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<Self>) -> Option<Vec3> {
        if slf.current < slf.count {
            Some(slf.origin.rand_offset(slf.r, slf.outer, slf.top_only, slf.ring))
        } else {
            None
        }
    
    }
}

    