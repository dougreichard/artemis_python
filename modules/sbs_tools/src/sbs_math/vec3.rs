use pyo3::prelude::*;
use pyo3::{basic::CompareOp, PyNumberProtocol, PyObjectProtocol};
use rand::thread_rng;
use rand::Rng;
use std::option::Option;

#[pyclass]
#[derive(Clone)]
/// A class representing a 3D vector
pub struct Vec3 {
    /// The x value
    #[pyo3(get, set)]
    x: f64,
    /// the y value
    #[pyo3(get, set)]
    y: f64,
    /// the z value
    #[pyo3(get, set)]
    z: f64,
}

#[pyclass]
#[derive(Clone)]
pub struct Angles3 {
    #[pyo3(get, set)]
    theta: f64,
    #[pyo3(get, set)]
    phi: f64,
}

#[pymethods]
impl Vec3 {
    #[new]
    fn new(x: f64, y: f64, z: f64) -> Self {
        Vec3 { x, y, z }
    }
    /// The dot product of this vector and another
    fn dot(&self, v: &Vec3) -> f64 {
        self.x * v.x + self.y * v.y + self.z * v.z
    }
    /// The cross product of this vector and another
    fn cross(&self, v: &Vec3) -> Vec3 {
        Vec3::new(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )
    }
    /// An new vector diving this vector and a float value
    fn divide(&self, f: f64) -> Vec3 {
        Vec3 {
            x: self.x / f,
            y: self.y / f,
            z: self.z / f,
        }
    }
    /// the length of the vector
    fn length(&self) -> f64 {
        return f64::sqrt(self.dot(self));
    }
    /// returns the unit vector from this vector
    fn unit(&self) -> Vec3 {
        self.divide(self.length())
    }
    /// the minimum of x,y or z
    fn min(&self) -> f64 {
        f64::min(f64::min(self.x, self.y), self.z)
    }
    /// the maximum of x,y or z
    fn max(&self) -> f64 {
        f64::max(f64::max(self.x, self.y), self.z)
    }
    /// return a new vector by adding another vector to this one
    fn add(&self, v: &Vec3) -> Vec3 {
        Vec3 {
            x: self.x + v.x,
            y: self.y + v.y,
            z: self.z + v.y,
        }
    }
    /// return a new vector by multiplying another vector to this one
    fn mul(&self, v: &Vec3) -> Vec3 {
        Vec3 {
            x: self.x * v.x,
            y: self.y * v.y,
            z: self.z * v.y,
        }
    }
    /// return a new vector by adding a float to this one
    fn mulf64(&self, v: f64) -> Vec3 {
        Vec3 {
            x: self.x * v,
            y: self.y * v,
            z: self.z * v,
        }
    }
    /// convert to angle
    fn to_angles(&self) -> Angles3 {
        Angles3 {
            theta: f64::atan2(self.z, self.x),
            phi: f64::asin(self.y / self.length()),
        }
    }
    /// angle to
    fn angle_to(&self, v: &Vec3) -> f64 {
        f64::acos(self.dot(v) / (self.length() * v.length()))
    }

    /// return a new vector by offset this vector randomly
    #[args(outer = "0.0", only_top_half = "false", ring = "false")]
    fn rand_offset(&self, r: f64, outer: f64, only_top_half: bool, ring: bool) -> Vec3 {
        let v = Vec3::rand_in_sphere(r, outer, only_top_half, ring);
        self.add(&v)
    }

    /// Creates a random point in a sphere
    #[staticmethod]
    #[args(outer = "0.0", only_top_half = "false", ring = "false")]
    fn rand_in_sphere(radius: f64, outer: f64, only_top_half: bool, ring: bool) -> Vec3 {
        const PI: f64 = std::f64::consts::PI;
        let mut rng = thread_rng();
        let all = rand::distributions::Uniform::new_inclusive(-PI, PI);
        let half = rand::distributions::Uniform::new_inclusive(0.0, PI);

        let yaw = rng.sample(all);
        let pitch = if only_top_half {
            rng.sample(half)
        } else {
            rng.sample(all)
        };

        let mut ret = Vec3::new(0.0, 0.0, 0.0);
        ret.y = f64::sin(pitch) * radius;

        let out_rad = f64::cos(pitch) * radius;
        ret.x = f64::sin(yaw) * out_rad;
        ret.z = f64::cos(yaw) * out_rad;

        //# if there is an outer, r is an inner
        if outer > 0.0 {
            let radi = rand::distributions::Uniform::new_inclusive(radius, outer);
            let r = rng.sample(radi);
            if ring {
                ret.y = 0.0;
            }
            ret = ret.unit();
            ret = ret.mulf64(r);
        }
        // return ret
        ret
    }
}

#[pyproto]
impl PyNumberProtocol for Vec3 {
    fn __add__(lhs: Vec3, other: Vec3) -> PyResult<Vec3> {
        Ok(lhs.add(&other))
        //Ok(Vec3{x: lhs.x + other.x, y: lhs.y + other.y, z: lhs.z + other.z })
    }
    fn __sub__(lhs: Vec3, other: Vec3) -> PyResult<Vec3> {
        Ok(Vec3 {
            x: lhs.x - other.x,
            y: lhs.y - other.y,
            z: lhs.z - other.z,
        })
    }
    fn __mul__(lhs: Vec3, other: Vec3) -> PyResult<Vec3> {
        Ok(lhs.mul(&other))
    }
    fn __truediv__(lhs: Vec3, other: Vec3) -> PyResult<Vec3> {
        Ok(Vec3 {
            x: lhs.x / other.x,
            y: lhs.y / other.y,
            z: lhs.z / other.z,
        })
    }
    fn __neg__(self) -> PyResult<Vec3> {
        Ok(Vec3 {
            x: -self.x,
            y: -self.y,
            z: -self.z,
        })
    }
}

#[pyproto]
impl PyObjectProtocol for Vec3 {
    fn __richcmp__(&'p self, other: PyRef<Vec3>, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(self.x == other.x && self.y == other.y && self.z == other.z),
            _ => Ok(false),
        }
    }
}
