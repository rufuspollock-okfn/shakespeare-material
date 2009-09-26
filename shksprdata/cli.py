import os
import shutil
from ConfigParser import SafeConfigParser

import pkg_resources

import shakespeare.cli

class BaseCommand(shakespeare.cli.BaseCommand):
    max_args = None
    min_args = 0
    group_name = 'shkspr'

class TestSite(BaseCommand):
    '''Perform simple consistency tests on wui.

    Usage: test-data <wui url>
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        print 'WUI check'
        print   '========='
        import paste.fixture
        import paste.proxy
        self.wui_address = self.args[0]
        if not self.wui_address.startswith('http://'):
            self.wui_address = 'http://' + self.wui_address
        if self.wui_address.endswith('/'):
            self.wui_address = self.wui_address[:-1]

        wsgiapp = paste.proxy.make_proxy({}, self.wui_address)
        self.app = paste.fixture.TestApp(wsgiapp)

        def check_page(path, required_contents, status=200):
            print "* Checking page '%s%s'" % (self.wui_address, path)
            res = self.app.get(path, status=status)
            for required in required_contents:
                print '    ...checking for %r' % required
                assert required in res, res
            return res

        res = check_page('/', ['Work', 'Material'])
        res = res.click('Read texts')
        print '* Checking work index'
        worktitle = 'Antony and Cleopatra'
        assert worktitle in res

        print '* Checking work info'
        res = res.click(worktitle)
        assert worktitle in res
        assert 'Associated Material' in res
        mattitle = worktitle + ' [Gutenberg]' 
        assert mattitle in res

        print '* Checking material info'
        assert mattitle + '</a>' in res, res.showbrowser()
        # res.showbrowser()
        # res = res.click(mattitle)
        # does not work ....


class LoadTexts(BaseCommand):
    '''Load shakespeare texts.

    %prog [action]

        action = gutenberg | moby | all (default)
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        self._load_config()
        if self.args:
            action = self.args[0]
        else:
            action = 'all'

        if action == 'all':
            self.load_texts()
        elif action == 'gutenberg':
            self.load_works()
            self.load_gutenberg()
        elif action == 'moby':
            self.load_works()
            self.load_moby()
        else:
            print 'Command not recognized: %s' % action
        print 'Loaded successfully'

    @classmethod
    def load_texts(self):
        print '******* Loading Works'
        self.load_works()
        print '******* Loading Gutenberg'
        self.load_gutenberg()
        print '******* Loading Moby'
        self.load_moby()

    @classmethod
    def load_works(self):
        import shakespeare.model as model
        pkg = 'shksprdata'
        work_fileobj = pkg_resources.resource_stream(pkg, '/works_metadata.txt')
        model.load_works(work_fileobj)

    @classmethod
    def load_gutenberg(self):
        import shakespeare.model as model
        pkg = 'shksprdata'
        fileobj = pkg_resources.resource_stream(pkg, '/gutenberg/metadata.txt')
        def norm_work_name(out):
            if out.endswith('_f'):
                out = out[:-2]
            out = out.replace('_gut', '')
            out = out.replace('anthonie', 'antony')
            out = out.replace('errours', 'errors')
            out = out.replace('all_is', "alls")
            out = out.replace('loves_labour_', 'loves_labours_')
            out = out.replace('dreame', 'dream')
            out = out.replace('twelfe-', 'twelfth_')
            out = out.replace('tragedy_of_', '')
            return out

        material = model.load_material(fileobj, norm_work_name=norm_work_name)
        for item in material:
            if not item.resources:
                locator = u'%s::/gutenberg/%s.txt' % (pkg, item.name)
                res = model.Resource(
                    locator_type=u'package',
                    locator=locator,
                    # TODO: use format correctly
                    format=u'txt',
                    material=item,
                    )
        model.Session.flush()

    @classmethod
    def load_moby(self):
        import shakespeare.model as model
        pkg = 'shksprdata'
        fileobj = pkg_resources.resource_stream(pkg, '/moby/metadata.txt')
        def norm_work_name(out):
            out = out.replace('_moby', '')
            out = out.replace('labor', 'labour')
            out = out.replace('part_iii', 'part_3')
            out = out.replace('part_ii', 'part_2')
            out = out.replace('part_i', 'part_1')
            return out

        material = model.load_material(fileobj, norm_work_name=norm_work_name)
        for item in material:
            if not item.resources:
                res = model.Resource(
                    locator_type=u'cache',
                    locator='moby/html/%s.html' % item.name,
                    # TODO: use format correctly
                    format=u'html',
                    material=item,
                    )
                res = model.Resource(
                    locator_type=u'cache',
                    locator='moby/pdf/%s.pdf' % item.name,
                    # TODO: use format correctly
                    format=u'pdf',
                    material=item,
                    )
        model.Session.flush()
    
    # doing markdown conversion of EB text live takes too long ...
    # so exclude for time being
    @classmethod
    def eb11(self):
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


class MobyDownload(BaseCommand):
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

class Moby(BaseCommand):
    '''Convert Moby texts to various output formats.

    moby {action} [ {path-to-source} ]

    actions:
        html: convert to html
        latex: convert to latex
        pdf: convert to pdf (via latex)

    Source input files are at shksprdata/moby/

    If {path-to-source} is a directory run operation on all xml files in that
    directory.

    Output is placed in {cachedir}/moby/{format}/{original-file-name}.{format}
    
    e.g. if cachedir in config is cache and format is html:
    
        cache/moby/html/king_lear.html
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 2
    group_name = 'shkspr'

    def command(self):
        self._load_config()
        import shakespeare 
        conf = shakespeare.get_config()
        cachedir = os.path.abspath(conf['cachedir'])
        self.basedir = os.path.join(cachedir, 'moby')
        for format in [ 'html', 'latex', 'pdf' ]:
            fp = os.path.join(self.basedir, format)
            if not os.path.exists(fp):
                os.makedirs(fp)
        action = self.args[0]
        path = self.args[1]
        if os.path.isdir(path):
            for fn in [ f for f in os.listdir(path) if f.endswith('.xml') ]:
                self._run(action, os.path.join(path, fn))
        else:
            self._run(action, path)
    
    def _run(self, action, path):
        print 'Processing: %s' % path
        if action == 'html':
            print self.html(path)
        elif action == 'latex':
            print self.latex(path)
        elif action == 'pdf':
            print self.pdf(path)
        else:
            raise Exception('Unknown action: %s' % action)

    def _out_path(self, path, format):
        fn = os.path.basename(path)
        fn = os.path.splitext(fn)[0]
        out = os.path.join(self.basedir, format, fn + '.' + format)
        return out

    def _save(self, path, format, data):
        fp = self._out_path(path, format)
        fo = open(fp, 'w')
        fo.write(data)
        fo.close()
        return fp

    def html(self, path):
        import shksprdata.getdata.moby as moby
        t = moby.Transformer()
        out = t.to_html(open(path))
        return self._save(path, 'html', out)

    def latex(self, path):
        import shksprdata.getdata.moby as moby
        t = moby.Transformer()
        out = t.to_latex(open(path))
        return self._save(path, 'latex', out)

    def pdf(self, path):
        # import tempfile
        # builddir = os.path.join(tempfile.tempdir, 'shksprdata')
        builddir = os.path.join(self.basedir, 'build')
        if not os.path.exists(builddir):
            os.makedirs(builddir)
        if path.endswith('.xml'): # assume we have not converted yet
            latex_fp = self.latex(path)
        else:
            latex_fp = path
        cmd = 'pdflatex --output-dir=%s %s' % (builddir, latex_fp) 
        os.system(cmd)
        # bit of a hack ...
        pdfpath = self._out_path(path, 'build')
        # strip off .build
        pdfpath = pdfpath[:-6] + '.pdf'
        dest = self._out_path(path, 'pdf')
        shutil.copy(pdfpath, dest)

