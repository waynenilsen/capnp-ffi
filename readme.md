# FFI With Cap'n Proto

This project provides helpers for using Cap'n Proto to call Rust functions from Python 3. It may expand to other calling directions and languages but that is what it is limited to for now.

## Why bother?

> Cap’n Proto is an insanely fast data interchange format and capability-based RPC system.

Currently defining a common c-style interface between Rust and Python can be arduous especially for complex types. Cap'n Proto seemed like the perfect way to bridge the gap between languages (and others, javascript, ruby, etc) and provide interfaces on top that hide the serialization/deserialization that is going on. While I have not yet figured out a convenient way to do this with rust (help appreciated) the Python interface is quite clean. Also, this does not even use the interface feature
of capnproto which I believe could be even more useful.

## Setup

This has been tested on Ubuntu, it may work with Python 2.x but I have not tested it. The instructions below will setup the directory and run the test to make sure it is working correctly.

```shell
git clone --depth=1 https://github.com/waynenilsen/capnp-ffi
cd capnp-ffi
sudo apt-get install -y capnproto python3 pip
sudo pip3 install -r ./python-capnp-ffi/requirements.txt
cd rust-capnp-ffi
cargo build --release
cd ../python-capnp-ffi/
python3 test.py
```

## A simple proof of concept and walkhtrough

### Cap'N Proto setup


Create the `.capnp` schema file that defines the common object(s) see [the capnproto documentation](https://capnproto.org/language.html) for more information on how to do this. 

Generate the rust file that corresponds to the schema that we just created by using the [capnpc-rust](https://github.com/dwrensha/capnpc-rust) capnpc extension. 

```shell
git clone https://github.com/dwrensha/capnpc-rust --depth=1
cd capnpc-rust
multirust override stable
cargo build --release
chmod u+x ./target/release/canpc-rust
sudo cp ./target/release/capnpc-rust /usr/bin
```

Now, you can compile the schema into rust code and python code by using `capnpc -orust <lb>.capnpc` and `capnpc -opython <lb>.capnpc`.

### The Rust side

Setup the rust side by creating a new `dylib` rust project by using `cargo new <lb>` then modifying the `Cargo.toml` file as follows

```
[dependencies]
libc="*"
capnp="*"

[lib]
crate-type = ["dylib"]
name="<lb>"
```

Now in `src/lib.rs` define a function that we are going to use, below is an example for a date function. 

```rust
#![feature(libc)]
extern crate libc;
extern crate capnp;

mod date;

use std::slice;
use libc::size_t; 
use capnp::MessageReader;
use capnp::MallocMessageBuilder; 
use capnp::message::MessageBuilder;

#![feature(libc)]
extern crate libc;
extern crate capnp;

mod date; 

use std::slice;
use libc::size_t; 
use capnp::MessageReader;
use capnp::MallocMessageBuilder; 
use capnp::message::MessageBuilder;

#[repr(C)]
pub struct BytesOutput {
    values : *const u8,
    len : usize,
}


#[no_mangle]
pub extern fn change_date(external_data: *const u8, data_len : size_t) -> BytesOutput {
	let mut buf : &[u8] = unsafe{ slice::from_raw_parts(external_data, data_len as usize) }; 
	let imessage = ::capnp::serialize::read_message(&mut buf, ::capnp::ReaderOptions::new()).unwrap();
	let input_date : date::date::Reader = imessage.get_root().unwrap(); 
	
	
	let mut omessage = MallocMessageBuilder::new_default();
	{
		let mut out_dt = omessage.init_root::<date::date::Builder>();
		out_dt.set_year(input_date.get_year() + 1);
		out_dt.set_month(input_date.get_month());
		out_dt.set_day(1);
	}
	
	let mut out_buf : Vec<u8> = Vec::new();
	capnp::serialize::write_message( &mut out_buf, &omessage );
	BytesOutput {
		values: out_buf.as_ptr(),
		len : out_buf.len(), 
	}
}

```

There should be some better abstraction on the rust side but I haven't quite figured out how to deal with it.

### the Python side

Install the `capnp_ffi` package from this repository by cloning the git repo (it's not in pip) and define the external interface. Here is the same example corresponding to the rust code above. In this way, you can add the documentation here. Eventually this file could be compiled from the rust file above. 

```python
#date_example.py

import capnp_ffi

class DateLibInterface(capnp_ffi.CapnpInterface):
	'''
	adding documentation to the interface is possible by extending the 
	interface base class with docstrings 
	'''
	
	capnp_file = '../schemas/date.capnp'
	lib_file = '../rust-capnp-ffi/target/release/libcapnp_ffi.so'
	
	def __init__(self, *args, **kwargs):
		'''
		this is required
		'''
		super(DateLibInterface, self).__init__(*args, **kwargs)
	
	@capnp_ffi.external(rtype='Date')
	def change_date(self, idate):
		'''
		this changes the date by adding one to the year, using the same
		month and setting the day to 1.
		'''
		pass
```

That's it! Now, this external library can be imported and used as follows:

```python
import date_example
date_example = date_example.DateLibInterface()
d = date_example.Date(year=2015, month=2, day=5)
# call to rust function!
result = date_example.change_date(d)
```

