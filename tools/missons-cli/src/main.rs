use anyhow::Result;

use regex::Regex;
use tokio::fs::File;
use std::io;
use std::io::{BufReader, Read};
use std::path::Path;
use tokio::fs;
use tokio::io::AsyncWriteExt as _;

use hyper::{body::HttpBody as _, Client};
use hyper_tls::HttpsConnector;
use tokio::{
    process::{Command},
};
use std::process::{Stdio};
use std::env;

//use tokio::prelude::*;


struct Ds9Obs {}

impl Ds9Obs {
    fn new() -> Self {
        Ds9Obs {}
    }
    async fn delay(&self, ms: u64) -> Result<()> {
        tokio::time::sleep(std::time::Duration::from_millis(ms)).await;
        Ok(())
    }
    async fn process_doctor(&mut self) -> Result<bool> {
        let py_exists = Ds9Obs::file_exists("./PyRuntime/python.exe").await;
        let mission_exists = Ds9Obs::dir_exists("./data/missions").await;
        let pip_exists = Ds9Obs::file_exists("./PyRuntime/Scripts/pip.exe").await;
    
        if py_exists && mission_exists {
            println!("Artemis seem to be here");
        } else {
            println!("This EXE should be in an artemis directory");
        }

        if !pip_exists {
            println!("Python PIP is missing. Enter the command \"fixpip\" to fix.");
        }  else {
            println!("Python PIP enabled.");
        }
    
        Ok(true)
    }
    async fn process_fixpip(&mut self) -> Result<bool> {
        let url = "https://bootstrap.pypa.io/get-pip.py";
        let url = url.parse::<hyper::Uri>().unwrap();
        if url.scheme_str() != Some("https") {
            println!("This example only works with 'https' URLs.");
        }
        let script = "PyRuntime\\get-pip.py";
        Ds9Obs::fetch_url(url, &script).await?;
        // It is ok if these fail
        let _ = fs::remove_file("PyRuntime\\python39._pth.renamed").await;
        let _ = fs::rename("PyRuntime\\python39._pth", "PyRuntime\\python39._pth.renamed").await;

        // 
// let command = Command::new("ls")
// .env("PATH", "/bin");
        let _ = Command::new("PyRuntime\\python.exe")
                     .arg(&script)
                     .stdout(Stdio::inherit())
                     .spawn()
                     .expect("Failed to execute command")
                     .wait()
                    .await;

        Ok(true)
    }

    async fn process_scene(&self, scene: &str) -> Result<bool> {
        println!("Switched to scene {0}", &scene);
        Ok(true)
    }

    async fn process_lines(&mut self) -> Result<()> {
        loop {
            let mut input = String::new();
            io::stdin().read_line(&mut input)?;
            if self.process_line(&input).await? == false {
                break;
            }
        }
        Ok(())
    }
    async fn process_add(&mut self, module: &str) -> Result<bool> {
        // let command = Command::new("ls")
        // .env("PATH", "/bin");
        let _ = Command::new("pip")
            .arg("install")
            .arg(&module)
            .arg("--target")
            .arg("PyAddons\\lib")
            .env("PATH", "PyRuntime\\Scripts;PyRuntime\\")
            .env("PY_PIP", "PyRuntime\\Scripts")
            .env("PY_LIBS", "PyRuntime\\Libs;PyRuntime\\Lib\\site-packages")
            .stdout(Stdio::inherit())
            .spawn()
            .expect("Failed to execute command")
            .wait()
            .await;

        Ok(true)
    }
    async fn process_install(&mut self, mission: &str) -> Result<bool> {
        // let command = Command::new("ls")
        // .env("PATH", "/bin");
        let _ = Command::new("pip")
            .arg("install")
            .arg("-r")
            .arg(&mission)
            .arg("--target")
            .arg("PyAddons\\lib")
            .env("PATH", "PyRuntime\\Scripts;PyRuntime\\")
            .env("PY_PIP", "PyRuntime\\Scripts")
            .env("PY_LIBS", "PyRuntime\\Libs;PyRuntime\\Lib\\site-packages")
            .stdout(Stdio::inherit())
            .spawn()
            .expect("Failed to execute command")
            .wait()
            .await;

        Ok(true)
    }
    async fn process_uninstall(&mut self, module: &str) -> Result<bool> {
        // let command = Command::new("ls")
        // .env("PATH", "/bin");
        //let dir = format!("F:\\backup\\artemis-3\\Art3.01\\PyAddons\\{}", &module);
        // let dir = format!("PyAddons\\{}", &module);
        // println!("{}", &dir);
        // if Ds9Obs::dir_exists(&dir).await {
        //     fs::remove_dir_all(&dir).await.expect("Rem dir failed");
        // }
        
        Ok(true)
    }


    async fn process_line(&mut self, input: &str) -> Result<bool> {
        // let cmd_connect = Regex::new(
        //     r"^co(?:n|nn|nne|nnec|nnect)?\s+([\w\*\-]+)(?:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))?(?::(\d{1,5}))?$",
        // )?;
        let cmd_fixpip = Regex::new(r"^fix(p|pi|pip)?$")?;
        let cmd_doctor = Regex::new(r"^doc(t|to|tor)?$")?;
        let cmd_add = Regex::new(r"^add\s+([\w\*\-]+)$")?;
        let cmd_install = Regex::new(r"^in(s|st|sta|stal|stall)?$")?;
        let cmd_uninstall = Regex::new(r"^uni(n|ns|nst|nsta|nstal|nstall)?\s+([\w\*\-]+)$")?;
        let cmd_scene = Regex::new(r"^sc(?:e|en|ene)?\s+([\w\*\-]+)$")?;
        let cmd_exit = Regex::new(r"^ex(i|it)?$")?;

        let line = input.trim();
        println!("Recieved: _{0}_", &line);

        if let Some(_) = cmd_fixpip.captures(&line) {
            self.process_fixpip().await?;
        } else if let Some(_) = cmd_doctor.captures(&line) {
            self.process_doctor().await?;
        } else if let Some(_) = cmd_exit.captures(&line) {
            return Ok(false);
        } else if let Some(_) = cmd_install.captures(&line) {
            self.process_install("mission").await?;
            return Ok(false);
        } else if let Some(tup) = cmd_add.captures(&line) {
            let module = match tup.get(2) {
                Some(s) => s.as_str(),
                _ => "",
            };
            self.process_add(module).await?;
        } else if let Some(tup) = cmd_uninstall.captures(&line) {
            let module = match tup.get(2) {
                Some(s) => s.as_str(),
                _ => "",
            };
            self.process_uninstall(module).await?;
        } else if let Some(tup) = cmd_scene.captures(&line) {
            let scene = match tup.get(1) {
                Some(s) => s.as_str(),
                _ => "",
            };
            self.process_scene(scene).await?;
        }

        Ok(true)
    }
    
/////////////////////////////////////////////////////////////////////////////////////
/// /
/// /
/// /
    // Maybe this should be sync, but I'm leartning Async/Await and Tokio
    async fn file_exists(filename: &str) -> bool {
        let md = fs::metadata(filename).await;
        let exists = if let Ok(attr) = md {
            attr.is_file()
        } else {
            false
        };
        if exists {
            println!("[X] File {} found", &filename);
        } else {
            println!("[ ] File {} NOT found", &filename);
        }
        exists
    }
    async fn dir_exists(filename: &str) -> bool {
        let md = fs::metadata(filename).await;
        let exists = if let Ok(attr) = md {
            attr.is_dir()
        } else {
            false
        };
        if exists {
            println!("[X] Dir {} found", &filename);
        } else {
            println!("[ ] Dir {} NOT found", &filename);
        }
        exists
    }

    async fn fetch_url(url: hyper::Uri, to_file:&str) -> Result<()> {
        let https = HttpsConnector::new();
        let client = Client::builder().build::<_, hyper::Body>(https);

        let mut res = client.get(url).await?;

        println!("Response: {}", res.status());
        println!("Headers: {:#?}\n", res.headers());

        // Stream the body, writing each chunk to stdout as we get it
        // (instead of buffering and printing at the end).
        let mut file = File::create(to_file).await?;
        while let Some(next) = res.data().await {
            let chunk = next?;
            file.write_all(&chunk).await?;
        }

        println!("\n\nDone!");

        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let mut ds9 = Ds9Obs::new();
    ds9.process_doctor().await.expect("Doctor command failed!");

  
    // let file = File::open("config.json");
    // match file {
    //     Ok(f) => {
    //         let mut contents = String::new();
    //         let mut br = BufReader::new(f);
    //         br.read_to_string(&mut contents)?;
    //         // Deserialize
    //         ds9.config = serde_json::from_str(&contents)?;
    //         println!("Loaded config");
    //     }
    //     _ => {
    //         println!("No config found. Using defaults.");
    //     }
    // }
    ds9.process_lines().await.ok().expect("Whoops");
    Ok(())
}
