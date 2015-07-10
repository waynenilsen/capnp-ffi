import unittest
import capnp_ffi
import os

class TestCapnp(unittest.TestCase):
	def setUp(self):
		print(os.getcwd())
		self.interop = capnp_ffi.CapnpInterface(
			capnp_file='../schemas/date.capnp'
			, function_names = ['it_works']
			, lib_file = '../rust-capnp-ffi/target/release/libcapnp_ffi.so'
		)
		
	def test_1(self):
		d = self.interop.MessageType.Date.new_message( year=2015, month=1, day=1)
		self.interop.it_works(d)
		
if __name__ == '__main__':
	unittest.main()
