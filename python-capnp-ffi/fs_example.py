import capnp
import capnp.lib.capnp as cpl
capnp.remove_import_hook()
fs_capnp = capnp.load('schemas/fs.capnp')

def create_ffi(capnp_file):
    GenericFFI = type('GenericFFI', (object,), {})
    capnp_schema = capnp.load(capnp_file)
    for interface in dir(capnp_schema):
        interface = getattr(capnp_schema, interface)
        if not isinstance(interface, cpl._InterfaceModule):
            continue
        InterfaceType = type(interface, (interface.Server,), {})
        #attach the implementations for the ffi functions, we know what they are
        for method_name, method in interface.schema.methods.items():
            def ffi_method(self, **kwargs):
                for field_name, field in method.param_type.fields.items():
                    field=field.proto.slot
                    if field.hasExplicitDefault:
                        if field_name not in kwargs:
                            kwargs[field_name] = field.defaultValue
                    try:
                        assert field in kwargs
                    except Exception:
                        raise KeyError('Missing required field "{}" to function "{}" with no default'.format(field_name, method_name))

                    # insert call to ffi library here and parse return type but what is it?

            ffi_method.__name__ = method_name
            setattr(InterfaceType, method_name, ffi_method)
        setattr(GenericFFI, interface, InterfaceType)
    return GenericFFI

fs = create_ffi('schemas/fs.capnp')

assert hasattr(fs, 'Node')
assert hasattr(fs.Node, 'isDirectory')
