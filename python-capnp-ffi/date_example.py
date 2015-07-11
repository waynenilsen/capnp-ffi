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
