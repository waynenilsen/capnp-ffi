'''
Cap'n Proto FFI tools for Python

Cap'n Proto is a fast binary format which is being used to pass messages across the FFI boundary. This allows easy declaration and modification of complex messages that get passed between function boundaries. There are other possible ways of doing the same thing but Cap'n Proto is the best candidate at this time for spporting Python 2, 3 and Rust at the same time.

Cap'n Proto has the advantage that it also defines interfaces which may be used later. This feature currently is not being used in this library.

'''

import cffi
import capnp
import functools
from types import FunctionType

capnp.remove_import_hook()

def external(rtype):
	'''
	This decorator declares a function as being external (to python) 
	
	:param rtype: the string value of the return type from the capnproto schema
	'''
	def _external(func):
		def callme(self, imessage):
			msgbytes = imessage.to_bytes()
			rvalue = getattr(self.lib, func.__name__)(msgbytes, len(msgbytes))
			return getattr(self.MessageType, rtype).from_bytes(b''.join(
				rvalue.values[i] for i in range(rvalue.len)
			))
		callme.__name__ = func.__name__
		callme.__doc__ = func.__doc__
		callme._rtype = rtype
		return callme
	return _external

def _gen_funcs(self):
	'''
	an internal helper function to iterate over the external functions
	of the object passed.
	'''
	for f in dir(self):
		f = getattr(self, f)
		if hasattr(f, '_rtype'):
			yield f

class CapnpInterface(object):
	'''
	This class is not to be created by itself, only extended. 
	'''
	
	def __init__(self):
		'''
		All subclasses must call the superclass constructor as the first line of their constructor.
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
		'''
		A convenience function for creating new messages.
		'''
		return getattr(self.MessageType, class_name).new_message(*args, **kwargs)


