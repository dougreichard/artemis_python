cargo build --release
copy target\release\missions-cli.exe F:\backup\artemis-3\Art3.01
pushd F:\backup\artemis-3\Art3.01
missions-cli.exe
popd