import cffi
import capnp
import functools
capnp.remove_import_hook()

class CapnpInterface(object):
	def __init__(self, capnp_file, lib_file, functions, class_names=None):
		'''
		this creates a new FFI for explicit use with Cap'n Proto i/o
		
		'''
		#setup FFI
		self.ffi = cffi.FFI()
		self.ffi.cdef('''
		typedef struct {
			char* values;
			size_t len;
		} bytes_output;
		''' + '\n'.join(
			'bytes_output {}(char*, size_t);'.format(f)
				for f in functions.keys()
		))
		self.lib = self.ffi.dlopen(lib_file)
		self.MessageType = capnp.load(capnp_file)
		
		# attach the functions
		for f, rt in functions.items():
			setattr(self, f, lambda message : self.by_name(f, rt, message))
		
		#attach class names (optional)
		if class_names is not None:
			for cn in class_names:
				setattr(self, cn, lambda *args, **kwargs: self.make_new(cn, *args, **kwargs))
	
	def make_new(self, class_name, *args, **kwargs):
		return getattr(self.MessageType, class_name).new_message(*args, **kwargs)
	
	def by_name(self, func, rtype, imessage):
		msgbytes = imessage.to_bytes()
		rvalue = getattr(self.lib, func)(msgbytes, len(msgbytes))
		return getattr(self.MessageType, rtype).from_bytes(b''.join(
			rvalue.values[i] for i in range(rvalue.len)
		))

