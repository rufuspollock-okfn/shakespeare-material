import os
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
    group_name = 'shkspr'

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
        fileobj = pkg_resources.resource_stream(pkg, '/gutenberg/metadata.txt')
        cfgp = SafeConfigParser()
        cfgp.readfp(fileobj)
        for section in cfgp.sections():
            work_name = self.norm_work_name(section)
            work = model.Work.by_name(work_name)
            if work is None:
                work = model.Work(name=work_name)

            item = model.Material.by_name(section)
            if item is None:
                item = model.Material(name=section)
            assert item is not None
            for key, val in cfgp.items(section):
                if key in ['title', 'creator']:
                    setattr(work, key, val)
                setattr(item, key, val)
            item.work = work
            item.src_pkg = pkg
            item.src_locator = '/gutenberg/%s.txt' % section
            model.Session.flush()

        # doing markdown conversion of EB text live takes too long ...
        # so exclude for time being
        return

        # now do the eb info
        item = model.Material.by_name('shakespeare_eb11')
        if item is None:
            item = model.Material(
                name='shakespeare_eb11',
                title='William Shakespeare Entry in Encyclopaedia Brittanica 11th Edition (1911)',
                creator='Encylopaedia Britannica',
                src_pkg = pkg,
                src_locator = '/ancillary/britannica-11th.txt',
                format='mkd'
                )
        model.Session.flush()

class MobyDownload(shakespeare.cli.BaseCommand):
    '''Download Moby texts.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 0
    group_name = 'shkspr'

    def command(self):
        self._load_config()
        # TODO: allow specifying a path?
        self.download()

    @classmethod
    def download(self, savepath=None):
        if not savepath:
            savepath = os.path.abspath('shksprdata/moby')
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        import shksprdata.getdata.moby as moby
        h = moby.Helper(moby.index, savepath, verbose=self.verbose)
        h.all()

class Moby(shakespeare.cli.BaseCommand):
    '''Convert Moby texts to various output formats.

    moby {action} {path}

    actions:
        html: convert to html
        latex: convert to latex
        pdf: convert to pdf (via latex)

    Source input files are at shksprdata/moby/
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 2
    group_name = 'shkspr'

    def command(self):
        self._load_config()
        action = self.args[0]
        path = self.args[1]
        if action == 'html':
            print self.html(path)
        elif action == 'latex':
            print self.latex(path)
        elif action == 'pdf':
            self.pdf(path)

    def html(self, path):
        import shksprdata.getdata.moby as moby
        t = moby.Transformer()
        out = t.to_html(open(path))
        return out

    def latex(self, path):
        import shksprdata.getdata.moby as moby
        t = moby.Transformer()
        out = t.to_latex(open(path))
        return out

    def pdf(self, path):
        # import tempfile
        # builddir = os.path.join(tempfile.tempdir, 'shksprdata')
        import shakespeare 
        conf = shakespeare.get_config()
        builddir = os.path.join(conf['cachedir'], 'latex')
        if not os.path.exists(builddir):
            os.makedirs(builddir)
        if path.endswith('.xml'): # assume we have not converted yet
            out = self.latex(path)
            latex_fp = os.path.join(builddir, os.path.basename(path) + '.tex')
            fo = open(latex_fp, 'w')
            fo.write(out)
            fo.close()
        else:
            latex_fp = path
        cmd = 'pdflatex --output-dir=%s %s' % (builddir, latex_fp) 
        os.system(cmd)

