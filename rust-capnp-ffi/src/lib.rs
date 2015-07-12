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

impl BytesOutput {
	
}

pub extern fn to_date<'a>(external_data: *const u8, data_len : size_t) -> date::date::Reader<'a> {
	let mut buf : &'a [u8] = unsafe{ slice::from_raw_parts(external_data, data_len as usize) }; 
	let imessage = capnp::serialize::read_message(&mut buf, ::capnp::ReaderOptions::new()).unwrap();
	let x : date::date::Reader<'a> = imessage.get_root().unwrap();
	x
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
