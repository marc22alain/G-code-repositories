def parseModuleClasses(imported_module):
    d = {}
    module_dir = dir(imported_module)
    for i in module_dir:
        module_member = getattr(imported_module,i)

        if hasattr(module_member, '__bases__'):
            bases =  getattr(module_member, '__bases__')

            if bases[0].__name__ == 'GeometricFeature':
                if hasattr(module_member, 'name'):
                    d[module_member.name] = module_member
                else:
                    d[module_member.__name__] = module_member

    return d
