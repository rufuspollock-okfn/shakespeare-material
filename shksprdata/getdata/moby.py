"""
Obtain and import the Moby/Bosak xml-i-fied versions of shakespeare's plays
available from:

    <http://www.ibiblio.org/xml/examples/shakespeare/>

Note Moby/Bosak is *not* TEI encoded. See discussion in:

    http://bistro.northwestern.edu/mmueller/ariadne/teixintro/index.htm

TEI resources for transforming TEI to various output formats can be found at:

    <http://www.tei-c.org/Tools/Stylesheets/>
    <http://sourceforge.net/project/showfiles.php?group_id=106328>
"""
import os

# just extract by hand from the above webpage
# vim regex used to do this
# s:^.*href="\([^"]*\)">\([^<]*\)</a>:    ("\2",^M         'http\://www.ibiblio.org/xml/examples/shakespeare/\1'),:g

index = [
    ("All's Well That Ends Well",
        'http://www.ibiblio.org/xml/examples/shakespeare/all_well.xml'),
    ("As You Like It",
        'http://www.ibiblio.org/xml/examples/shakespeare/as_you.xml'),
    ("Antony and Cleopatra",
        'http://www.ibiblio.org/xml/examples/shakespeare/a_and_c.xml'),
    ("A Comedy of Errors",
        'http://www.ibiblio.org/xml/examples/shakespeare/com_err.xml'),
    ("Coriolanus",
        'http://www.ibiblio.org/xml/examples/shakespeare/coriolan.xml'),
    ("Cymbeline",
        'http://www.ibiblio.org/xml/examples/shakespeare/cymbelin.xml'),
    ("A Midsummer Night's Dream",
        'http://www.ibiblio.org/xml/examples/shakespeare/dream.xml'),
    ("Hamlet",
        'http://www.ibiblio.org/xml/examples/shakespeare/hamlet.xml'),
    ("Henry IV, Part I",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_iv_1.xml'),
    ("Henry IV, Part II",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_iv_2.xml'),
    ("Henry V",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_v.xml'),
    ("Henry VIII",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_viii.xml'),
    ("Henry VI, Part 1",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_vi_1.xml'),
    ("Henry VI, Part 2",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_vi_2.xml'),
    ("Henry VI, Part 3",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_vi_3.xml'),
    ("The Life and Death of King John",
        'http://www.ibiblio.org/xml/examples/shakespeare/john.xml'),
    ("Julius Caesar",
        'http://www.ibiblio.org/xml/examples/shakespeare/j_caesar.xml'),
    ("King Lear",
        'http://www.ibiblio.org/xml/examples/shakespeare/lear.xml'),
    ("Love's Labor's Lost",
        'http://www.ibiblio.org/xml/examples/shakespeare/lll.xml'),
    ("Macbeth",
        'http://www.ibiblio.org/xml/examples/shakespeare/macbeth.xml'),
    ("The Merchant of Venice",
        'http://www.ibiblio.org/xml/examples/shakespeare/merchant.xml'),
    ("Much Ado About Nothing",
        'http://www.ibiblio.org/xml/examples/shakespeare/much_ado.xml'),
    ("Measure for Measure",
        'http://www.ibiblio.org/xml/examples/shakespeare/m_for_m.xml'),
    ("The Merry Wives of Windsor",
        'http://www.ibiblio.org/xml/examples/shakespeare/m_wives.xml'),
    ("Othello",
        'http://www.ibiblio.org/xml/examples/shakespeare/othello.xml'),
    ("Pericles",
        'http://www.ibiblio.org/xml/examples/shakespeare/pericles.xml'),
    ("Richard II",
        'http://www.ibiblio.org/xml/examples/shakespeare/rich_ii.xml'),
    ("Richard III",
        'http://www.ibiblio.org/xml/examples/shakespeare/rich_iii.xml'),
    ("Romeo and Juliet",
        'http://www.ibiblio.org/xml/examples/shakespeare/r_and_j.xml'),
    ("The Taming of the Shrew",
        'http://www.ibiblio.org/xml/examples/shakespeare/taming.xml'),
    ("The Tempest",
        'http://www.ibiblio.org/xml/examples/shakespeare/tempest.xml'),
    ("Timon of Athens",
        'http://www.ibiblio.org/xml/examples/shakespeare/timon.xml'),
    ("Titus Andronicus",
        'http://www.ibiblio.org/xml/examples/shakespeare/titus.xml'),
    ("Troilus and Cressida",
        'http://www.ibiblio.org/xml/examples/shakespeare/troilus.xml'),
    ("Two Gentlemen of Verona",
        'http://www.ibiblio.org/xml/examples/shakespeare/two_gent.xml'),
    ("Twelfth Night",
        'http://www.ibiblio.org/xml/examples/shakespeare/t_night.xml'),
    ("A Winter's Tale",
        'http://www.ibiblio.org/xml/examples/shakespeare/win_tale.xml'),
    ]

import shakespeare.gutenberg
import urllib
class Helper(shakespeare.gutenberg.HelperBase):

    def __init__(self, works, cache='', verbose=False):
        self._index = works
        self.cache = cache
        self.verbose = verbose

    def title_to_name(self, title):
        out = super(Helper, self).title_to_name(title)
        tmap = { 'life_and_death_of_king_john': 'john' }
        out = tmap.get(out, out)
        return out

    def download(self):
        for item in self._index:
            title, url = item
            dest = self.title_to_name(title) + '_moby.xml'
            dest = os.path.join(self.cache, dest)
            self.vprint('Processing %s' % url)
            if os.path.exists(dest):
                self.vprint('\tSkipping')
            else:
                urllib.urlretrieve(url, dest)
    
    def make_metadata(self):
        meta = {}
        for text in self._index:
            title, url = text
            textinfo = {}
            textinfo['title'] = title
            textinfo['url'] = url
            textinfo['notes'] = 'Moby/Bosak Shakespeare, sourced from %s' % text[1]
            name = self.title_to_name(title) + '_moby'
            meta[name] = textinfo
        return meta
    
    def save_metadata(self):
        meta = self.make_metadata()
        metapath = os.path.join(self.cache, 'metadata_moby.txt')
        import ConfigParser
        cfgp = ConfigParser.SafeConfigParser()
        x = meta.keys()
        x.sort()
        for textname in x:
            cfgp.add_section(textname)
            for k,v in meta[textname].items():
                cfgp.set(textname, k, v)
        self.vprint('Saving metadata')
        cfgp.write(open(metapath, 'w'))

    def all(self):
        self.download()
        self.save_metadata()

import pkg_resources
from lxml import etree
from StringIO import StringIO
class Transformer(object):

    def norm_name(self, dummy, name):
        out = name
        out = out.split(',')[0]
        out = out.split(',')[0]
        out = out.replace(' ', '')
        return out.lower()
               
    def transform(self, xsltfo, itemfo):
        # ns = etree.FunctionNamespace('http://openshakespeare.org/functions')
        # ns.prefix = 'es'
        # ns['norm_name'] = self.norm_name
        extensions = {('http://openshakespeare.org/functions', 'norm_name'):
                self.norm_name}
        # namespaces = {'es' : 'http://openshakespeare.org/functions'}

        xslt_doc = etree.parse(xsltfo)
        doc = etree.parse(itemfo)
        # print doc.xpath("es:norm_name('bbb')")
        # e = etree.XPathEvaluator(doc)

        transform = etree.XSLT(xslt_doc,
                # namespaces=namespaces,
                extensions=extensions
                )
        out = transform(doc)
        return str(out)

    def to_html(self, itemfo):
        xsltfo = pkg_resources.resource_stream('shksprdata', '/moby_html.xsl')
        return self.transform(xsltfo, itemfo)

    def to_latex(self, itemfo):
        '''Convert to latex.
        '''
        # something weird with pkg_resource streams so that cannot use same
        # fileobj twice even when doing seek(0) ...
        text = itemfo.read()
        itemfo = StringIO(text)
        itemfo2 = StringIO(text)

        xsltfo = pkg_resources.resource_stream('shksprdata', '/moby_latex.xsl')
        body = self.transform(xsltfo, itemfo)
        # escape all latex entities
        for ch in [ '&', '$' ]:
            body = body.replace(ch, '\\%s' % ch)
        header = pkg_resources.resource_stream('shksprdata',
                '/latex/header.tex').read()
        doc = etree.parse(itemfo2)
        # TODO: use supplied title
        title = doc.xpath('/PLAY/TITLE/text()')[0]
        # tidy it up (e.g. 'Twelfth Night, or What You Will')
        title = title.split(',')[0]
        header = header.replace('INSERT TITLE HERE', title)
        out = header + body + '\n\\end{document}'
        return out

if __name__ == '__main__':
    savepath = os.path.abspath('shksprdata/moby')
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    h = Helper(index, savepath, verbose=True)
    h.all()
