
#![feature(libc)]
extern crate libc;

use std::slice;
use libc::size_t; 

#[repr(C)]
pub struct BytesOutput {
	values : *const u8,
	len : usize,
}

impl BytesOutput {
	
}

#[no_mangle]
pub extern fn it_works(external_data: *const u8, data_len : size_t) -> BytesOutput {
	let buf = unsafe{ slice::from_raw_parts(external_data, data_len as usize) }; 
	println!("hi");
	
	BytesOutput {
		values: buf.as_ptr(),
		len : buf.len(), 
	}
}
