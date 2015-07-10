import cffi
import capnp
capnp.remove_import_hook()

class CapnpInterface(object):
	def __init__(self, capnp_file, function_names, lib_file):
		self.ffi = cffi.FFI()
		self.ffi.cdef('''
		typedef struct {
			char* values;
			size_t len;
		} bytes_output;
		''' + '\n'.join(
			'bytes_output {}(char*, size_t);'.format(f)
				for f in function_names
		))
		self.lib = self.ffi.dlopen(lib_file)
		self.MessageType = capnp.load(capnp_file)
		
		# attach the functions
		for f in function_names:
			setattr(self, f, lambda message : self.by_name(f, message))
	
	def by_name(self, func, message):
		msgbytes = message.to_bytes()
		print(getattr(self.lib, func)(msgbytes, len(msgbytes)))

