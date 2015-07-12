import capnp
import capnp.lib.capnp as cpl
capnp.remove_import_hook()
fs_capnp = capnp.load('schemas/fs.capnp')

def create_ffi(capnp_file):
    RType = type('GenericFFI', (object,), {})
    tmp_capnp = capnp.load(capnp_file)
    for attr_name in dir(tmp_capnp):
        interface = getattr(tmp_capnp, attr_name)
        if not isinstance(interface, cpl._InterfaceModule):
            continue
        Tmp = type(attr_name, (interface.Server,), {})
        #attach the implementations for the ffi functions, we know what they are
        for method_name, method in interface.schema.methods.items():
            def tmp_ffi_func(self, **kwargs):
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

            tmp_ffi_func.__name__ = method_name
            setattr(Tmp, method_name, tmp_ffi_func)
        setattr(RType, attr_name, Tmp)
    return RType

fs = create_ffi('schemas/fs.capnp')

assert hasattr(fs, 'Node')
assert hasattr(fs.Node, 'isDirectory')
