# FFI With Cap'n Proto

This project provides helpers for using Cap'n Proto to call Rust functions from Python 3. It may expand to other calling directions and languages but that is what it is limited to for now.

## Setup

This has been tested on Ubuntu, it may work with Python 2.x but I have not tested it. The instructions below will setup the directory and run the test to make sure it is working correctly.

```shell
git clone --depth=1 https://github.com/waynenilsen/capnp-ffi
cd capnp-ffi
sudo apt-get install -y capnproto python3 pip3
sudo pip3 install -r ./python-capnp-ffi/requirements.txt
cd rust-capnp-ffi
cargo build --release
cd ../python-capnp-ffi/
python3 test.py
```


