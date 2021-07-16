use pyo3::prelude::*;

mod sbs_math;

use sbs_math::vec3::Vec3;

/// A package for additional math realted objects
///
/// Basic usage:
///
fn init_math(m: &PyModule) -> PyResult<()> {
    m.add_class::<Vec3>()?;
    Ok(())
}


/// A Python module implemented in Rust.
#[pymodule]
fn sbs_tools(py: Python, m: &PyModule) -> PyResult<()> {
    let submod = PyModule::new(py, "math")?;
    init_math(submod)?;
    
    m.add_submodule(submod)?;
    Ok(())
}
