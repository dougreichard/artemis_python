use std::net::{TcpStream, TcpListener};
use std::io::{Read, Write};
use std::thread;
use pyo3::prelude::*;
use std::sync::Arc;
use std::time::{Duration, SystemTime};

#[pyclass]
pub struct HttpServer {
    
}

struct HttpConnectedClient {
    stream: TcpStream
}


impl HttpConnectedClient {
    fn handle_read(&mut self) {
        let mut buf = [0u8 ;4096];
        match self.stream.read(&mut buf) {
            Ok(_) => {
                let req_str = String::from_utf8_lossy(&buf);
                println!("{}", req_str);
                },
            Err(e) => println!("Unable to read stream: {}", e),
        }
    }

    fn handle_write(&mut self) {
        

        
        let x: String = format!("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<html><body>Hello {} </body></html>\r\n", now.elapsed().unwrap().as_secs());
        let response = x.as_bytes();
        match self.stream.write(response) {
            Ok(_) => println!("Response sent"),
            Err(e) => println!("Failed sending response: {}", e),
        }
    }

    fn handle_client(&mut self) {
        self.handle_read();
        self.handle_write();
    }
}

#[pymethods]
impl HttpServer {
    #[new]
    pub fn new() -> Self {
        let mut data = Arc::new(0);
        let shared = Arc::clone(&data);
        let t  = thread::spawn(|| {
            HttpServer::run();
            
        });
        HttpServer{}
    }
    #[staticmethod]
    fn run() {
        let listener = TcpListener::bind("127.0.0.1:8080").unwrap();
        println!("Listening for connections on port {}", 8080);

        for stream in listener.incoming() {
            match stream {
                Ok(stream) => {
                    thread::spawn(|| {
                        let mut client = HttpConnectedClient{stream};
                        client.handle_client()
                    });
                }
                Err(e) => {
                    println!("Unable to connect: {}", e);
                }
            }
        }
    }
}