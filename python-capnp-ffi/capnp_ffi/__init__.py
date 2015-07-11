import cffi
import capnp
import functools
from types import FunctionType

capnp.remove_import_hook()

def external(rtype):
	def _external(func):
		func = func.__name__
		def callme(self, imessage):
			msgbytes = imessage.to_bytes()
			rvalue = getattr(self.lib, func)(msgbytes, len(msgbytes))
			return getattr(self.MessageType, rtype).from_bytes(b''.join(
				rvalue.values[i] for i in range(rvalue.len)
			))
		callme.__name__ = func
		callme._rtype = rtype
		return callme
	return _external

def _gen_funcs(self):
	for f in dir(self):
		f = getattr(self, f) 
		if hasattr(f, '_rtype'):
			yield f

class CapnpInterface(object):
	
	def __init__(self):
		'''
		this creates a new FFI for explicit use with Cap'n Proto i/o
		
		'''
		# grab function information
		self.functions = { f.__name__ : f._rtype for f in _gen_funcs(self) }
		self.class_names = { f._rtype for f in _gen_funcs(self) }
		
		#setup FFI
		self.ffi = cffi.FFI()
		self.ffi.cdef('''
		typedef struct {
			char* values;
			size_t len;
		} bytes_output;
		''' + '\n'.join(
			'bytes_output {}(char*, size_t);'.format(f)
				for f in self.functions.keys()
		))
		self.lib = self.ffi.dlopen(self.lib_file)
		self.MessageType = capnp.load(self.capnp_file)
		
		#attach class names
		for cn in self.class_names:
			setattr(self, cn, lambda *args, **kwargs: self.make_new(cn, *args, **kwargs))
	
	def make_new(self, class_name, *args, **kwargs):
		return getattr(self.MessageType, class_name).new_message(*args, **kwargs)
	

