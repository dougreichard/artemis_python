use anyhow::{anyhow, Result};

use regex::Regex;
use std::io;
use std::io::{BufReader, Read};
use std::path::{Path, PathBuf};
use tokio::fs;
use tokio::fs::File;
use tokio::io::AsyncWriteExt as _;

use hyper::{body::HttpBody as _, Client};
use hyper_tls::HttpsConnector;
use tokio::process::Command;

use std::env;
use std::process::Stdio;
use std::str::FromStr;
use tempdir::TempDir;
use std::iter::Iterator;
use std::ffi::OsString;

//use tokio::prelude::*;

struct CliMission {}

impl CliMission {
    fn new() -> Self {
        CliMission {}
    }
    async fn delay(&self, ms: u64) -> Result<()> {
        tokio::time::sleep(std::time::Duration::from_millis(ms)).await;
        Ok(())
    }
    async fn process_doctor(&mut self) -> Result<bool> {
        env::current_dir().map(|p| { println!("Location: {}", p.display())});
        let py_exists = CliMission::file_exists("./PyRuntime/python.exe").await;
        let mission_exists = CliMission::dir_exists("./data/missions").await;
        let pip_exists = CliMission::file_exists("./PyRuntime/Scripts/pip.exe").await;
        if py_exists && mission_exists {
            println!("Artemis seem to be here");
        } else {
            println!("This EXE should be in an artemis directory");
        }

        if !pip_exists {
            println!("Python PIP is missing. Enter the command \"fixpip\" to fix.");
        } else {
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
        let script = PathBuf::from("PyRuntime\\get-pip.py");
        CliMission::fetch_url(url, &script).await?;
        // It is ok if these fail
        let _ = fs::remove_file("PyRuntime\\python39._pth.renamed").await;
        let _ = fs::rename(
            "PyRuntime\\python39._pth",
            "PyRuntime\\python39._pth.renamed",
        )
        .await;

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
    fn get_py_path(&self) -> OsString {
        if let Some(path) = env::var_os("PATH") {
            let mut paths = env::split_paths(&path).collect::<Vec<_>>();
            let mut pre_path = vec![PathBuf::from("PyRuntime\\Scripts"),PathBuf::from("PyRuntime\\")];
            pre_path.append(&mut paths);
            let new_path = env::join_paths(pre_path).unwrap();
            return new_path;
        }
        OsString::from("PyRuntime\\Scripts;PyRuntime\\")
    }
    async fn process_add(&mut self, module: &str) -> Result<bool> {
        // let command = Command::new("ls")
        // .env("PATH", "/bin");
        let new_path = self.get_py_path();
        println!("{}", new_path.to_str().unwrap());
        

        let _ = Command::new("pip")
            .arg("install")
            .arg(&module)
            .arg("--target")
            .arg("PyAddons\\lib")
            .env("PATH", &new_path)
            .env("PY_PIP","PyRuntime\\Scripts")
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
        let mission_path = format!("data\\missions\\{}\\requirements.txt", mission);
        let mission_lib = format!("data\\missions\\{}\\lib", mission);
        if !CliMission::file_exists(&mission_path).await {
            println!("Mission {} does not have a requirements.txt", &mission);
            return Ok(false);
        }
        
        let new_path = self.get_py_path();
        let _ = Command::new("pip")
            .arg("install")
            .arg("-r")
            .arg(&mission_path)
            .arg("--target")
            .arg(&mission_lib)
            .env("PATH", &new_path)
            .env("PY_PIP", "PyRuntime\\Scripts")
            .env("PY_LIBS", "PyRuntime\\Libs;PyRuntime\\Lib\\site-packages")
            .stdout(Stdio::inherit())
            .spawn()
            .expect("Failed to execute command")
            .wait()
            .await;

        let lib_init = format!("data\\missions\\{}\\lib\\__init__.py", mission);
        if !CliMission::file_exists(&lib_init).await {
            let _ = tokio::fs::write(&lib_init, "")
                .await
                .map(|_| {})
                .map_err(|e| {
                    // handle errors
                    eprintln!("IO error: {:?}", e);
                });
        }

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

    async fn process_fetch(&mut self, user: &str, repo: &str) -> Result<bool> {
        let url = format!("http://github.com/{}/{}/zipball/master/", &user, &repo);
        let url = url.parse::<hyper::Uri>().unwrap();
        // repo is mission name
        let mission_dir = format!("data\\missions\\{}", &repo);
        CliMission::fetch_unzip_url(url, &mission_dir).await.expect("Could not fetch misson");
        self.process_install(&repo).await?;
        Ok(true)
    }

    async fn process_line(&mut self, input: &str) -> Result<bool> {
        // let cmd_connect = Regex::new(
        //     r"^co(?:n|nn|nne|nnec|nnect)?\s+([\w\*\-]+)(?:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))?(?::(\d{1,5}))?$",
        // )?;
        let cmd_fixpip = Regex::new(r"^fix(p|pi|pip)?$")?;
        let cmd_doctor = Regex::new(r"^doc(t|to|tor)?$")?;
        let cmd_add = Regex::new(r"^add\s+([\w\*\-]+)$")?;
        let cmd_install = Regex::new(r"^in(s|st|sta|stal|stall)?\s+([\w\*\-]+)$")?;
        let cmd_uninstall = Regex::new(r"^uni(n|ns|nst|nsta|nstal|nstall)?\s+([\w\*\-]+)$")?;
        let cmd_fetch = Regex::new(r"^fe(t|tc|tch)?\s+([\w\*\-]+)/([\w\*\-]+)$")?;
        let cmd_exit = Regex::new(r"^ex(i|it)?$")?;

        let line = input.trim();
        println!("Recieved: _{0}_", &line);

        if let Some(_) = cmd_fixpip.captures(&line) {
            self.process_fixpip().await?;
        } else if let Some(_) = cmd_doctor.captures(&line) {
            self.process_doctor().await?;
        } else if let Some(_) = cmd_exit.captures(&line) {
            return Ok(false);
        } else if let Some(tup) = cmd_install.captures(&line) {
            let mission = match tup.get(2) {
                Some(s) => s.as_str(),
                _ => "",
            };
            self.process_install(&mission).await?;
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
        } else if let Some(tup) = cmd_fetch.captures(&line) {
            let user = match tup.get(2) {
                Some(s) => s.as_str(),
                _ => "",
            };
            let repo = match tup.get(3) {
                Some(s) => s.as_str(),
                _ => "",
            };
            self.process_fetch(&user, &repo).await?;
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

    // let stream = res.bytes_stream().map_err(convert_error);
    // let mut stream_reader = StreamReader::new(stream);
    // let mut decoder = GzipDecoder::new(stream_reader);

    async fn fetch_url(url: hyper::Uri, to_file: &PathBuf) -> Result<()> {
        let mut url = url.clone();

        let https = HttpsConnector::new();
        let client = Client::builder().build::<_, hyper::Body>(https);
        for _ in 1..10 {
            let mut res = client.get(url.clone()).await?;
            let status = res.status();
            let header = res.headers();

            println!("Response: {}", &status);
            println!("Headers: {:#?}\n", &header);
            if status.is_success() {
                // Stream the body, writing each chunk to stdout as we get it
                // (instead of buffering and printing at the end).
                let mut file = File::create(to_file).await?;
                while let Some(next) = res.data().await {
                    let chunk = next?;
                    file.write_all(&chunk).await?;
                }
                return Ok(());
            } else if status.is_redirection() {
                let location = header.get("location").unwrap().to_str().unwrap();
                url = hyper::Uri::from_str(location).unwrap();
            } else {
                return Err(anyhow!("http get error"));
            }
        }

        println!("\nToo many redirects!");

        Err(anyhow!("Too many redirects"))
    }

    async fn fetch_unzip_url(url: hyper::Uri, to_dir: &str) -> Result<()> {
        // get tempdir
        let temp_dir = TempDir::new("miss")?;
        let temp_file = temp_dir.path().join("mission.zip");
        // Fetch_url to tempfilename
        CliMission::fetch_url(url, &temp_file).await?;
        //UNzip it
        let file = fs::File::open(&temp_file).await?;
        let s_file = file.into_std().await;

        let mut archive = zip::ZipArchive::new(s_file).unwrap();
        let target_path = PathBuf::from(to_dir);
        for i in 0..archive.len() {
            let mut file = archive.by_index(i).unwrap();
            {
                let comment = file.comment();
                if !comment.is_empty() {
                    println!("File {} comment: {}", i, comment);
                }
            }
            let outpath = match file.enclosed_name() {
                Some(path) => path.to_owned(),
                None => continue,
            };
            let outpath = outpath.iter()   // iterate over path components
                    .skip(1)                      // skip "foo" itself
                    .collect::<PathBuf>();    
            let target_out_path = target_path.join(outpath);
            if (&*file.name()).ends_with('/') {
                println!("Folder {} extracted to \"{}\"", file.name(), target_out_path.display());
                fs::create_dir_all(&target_out_path).await?;
            } else {
                println!(
                    "File {} extracted to \"{}\" ({} bytes)",
                    file.name(),
                    target_out_path.display(),
                    file.size()
                );
                if let Some(p) = target_out_path.parent() {
                    if !p.exists() {
                        fs::create_dir_all(&p).await?;
                    }
                }
                let outfile = fs::File::create(&target_out_path).await?;
                let mut outfile = outfile.into_std().await;
                io::copy(&mut file, &mut outfile).unwrap();
            }
        }
        println!("\n\nDone!");

        Ok(())
    }
}

// let url = "http://github.com/dougreichard/chip8-rs/zipball/main/";
    // let url = url.parse::<hyper::Uri>().unwrap();
    // Ds9Obs::fetch_unzip_url(url, "C:\\tmp\\test\\missionDir").await?;
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


#[tokio::main]
async fn main() -> Result<()> {
    // Set the current dir to the location of the EXE
    let mut dir = env::current_exe()?;
    dir.pop();
    env::set_current_dir(dir);

    let mut cli = CliMission::new();
    // if there are commands process the one command
    if env::args().len() > 1 {
        let cmd_line = std::env::args().skip(1).collect::<Vec<String>>().join(" ");
        cli.process_line(&cmd_line).await.ok().expect("Whoops");
        return Ok(());
    } else {
        cli.process_doctor().await.expect("Doctor command failed!");
        cli.process_lines().await.ok().expect("Whoops");
    }
    
    Ok(())
}
