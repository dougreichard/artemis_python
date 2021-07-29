use pyo3::prelude::*;

mod sbs_math;
mod scatter;
mod www;

use sbs_math::vec3::Vec3;

/// A package for additional math realted objects
///
/// Basic usage:
///
fn init_math(m: &PyModule) -> PyResult<()> {
    m.add_class::<Vec3>()?;
    Ok(())
}

fn init_scatter(m: &PyModule) -> PyResult<()> {
    m.add_class::<scatter::Arc>()?;
    m.add_class::<scatter::Line>()?;
    Ok(())
}

fn init_www(m: &PyModule) -> PyResult<()> {
    m.add_class::<www::HttpServer>()?;
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn sbs_tools(py: Python, m: &PyModule) -> PyResult<()> {
    let submod = PyModule::new(py, "math")?;
    init_math(submod)?;
    m.add_submodule(submod)?;

    let submod = PyModule::new(py, "scatter")?;
    init_scatter(submod)?;
    m.add_submodule(submod)?;

    let submod = PyModule::new(py, "www")?;
    init_www(submod)?;
    m.add_submodule(submod)?;


    Ok(())
}
