from ConfigParser import SafeConfigParser

import pkg_resources

import shakespeare.cli

class LoadTexts(shakespeare.cli.BaseCommand):
    '''Load shakespeare texts.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 0

    def command(self):
        self._load_config()
        self.load_texts()
        print 'Loaded successfully'

    @classmethod
    def norm_work_name(self, name):
        out = name.replace('_f', '')
        out = out.replace('_gut', '')
        out = out.replace('anthonie', 'antony')
        out = out.replace('errours', 'errors')
        out = out.replace('alls', "all_is")
        out = out.replace('loves_labour_', 'loves_labours_')
        out = out.replace('dreame', 'dream')
        out = out.replace('twelfe-', 'twelfth_')
        return out

    @classmethod
    def load_texts(self):
        import shakespeare.model as model
        pkg = 'shksprdata'
        fileobj = pkg_resources.resource_stream(pkg, '/texts/metadata.txt')
        cfgp = SafeConfigParser()
        cfgp.readfp(fileobj)
        for section in cfgp.sections():
            work_name = self.norm_work_name(section)
            work = model.Work.by_name(work_name)
            if work is None:
                work = model.Work(name=work_name)

            item = model.Material.byName(section)
            if item is None:
                item = model.Material(name=section)
            assert item is not None
            for key, val in cfgp.items(section):
                if key in ['title', 'creator']:
                    setattr(work, key, val)
                setattr(item, key, val)
            item.work = work
            item.src_pkg = pkg
            item.src_locator = '/texts/%s.txt' % section
            model.Session.flush()


