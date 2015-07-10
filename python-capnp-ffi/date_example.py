import capnp_ffi

class DateLibInterface(capnp_ffi.CapnpInterface):
	'''
	adding documentation to the interface is possible by extending the 
	interface base class with docstrings 
	'''
	
	def __init__(self, *args, **kwargs):
		'''
		this is required
		'''
		super(DateLibInterface, self).__init__(*args, **kwargs)
	
	def change_date(self, idate):
		'''
		this changes the date by adding one to the year, using the same
		month and setting the day to 1.
		'''
		pass

def get_lib():
	return DateLibInterface(
		capnp_file='../schemas/date.capnp'
		, functions = {
			'change_date' : 'Date'
		}
		, lib_file = '../rust-capnp-ffi/target/release/libcapnp_ffi.so'
		, class_names = [ 'Date' ]
	)
