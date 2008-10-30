from ConfigParser import SafeConfigParser

import pkg_resources

import shakespeare.model as model

def load_texts():
    pkg = 'shksprdata'
    fileobj = pkg_resources.resource_stream(pkg, '/texts/metadata.txt')
    cfgp = SafeConfigParser()
    cfgp.readfp(fileobj)
    for section in cfgp.sections():
        item = model.Material.byName(section)
        if item is None:
            item = model.Material(name=section)
        assert item is not None
        for key, val in cfgp.items(section):
            setattr(item, key, val)
        item.src_pkg = pkg
        item.src_locator = '/texts/%s.txt' % section
        model.Session.flush()

