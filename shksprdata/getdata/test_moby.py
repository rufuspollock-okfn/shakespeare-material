import shksprdata.getdata.moby

class TestHelper(object):
    index = shksprdata.getdata.moby.index
    helper = shksprdata.getdata.moby.Helper(index, cache='')

    def test_index(self):
        title = 'Twelfth Night'
        url = 'http://www.ibiblio.org/xml/examples/shakespeare/t_night.xml'
        assert (title, url) in self.index
        assert len(self.index) == 37

    def test_helper_make_metadata(self):
        meta = self.helper.make_metadata()
        assert len(meta) == 37
        assert 'twelfth_night_moby' in meta, meta.keys()


from StringIO import StringIO
class TestTransform:
    intext = StringIO('''<?xml version="1.0"?>
<!DOCTYPE PLAY SYSTEM "play.dtd">

<PLAY>
<TITLE>The Tempest</TITLE>

<PERSONAE>
<TITLE>Dramatis Personae</TITLE>

<PERSONA>GONZALO, an honest old Counsellor.</PERSONA>

<PGROUP>
<PERSONA>ADRIAN</PERSONA>
<PERSONA>FRANCISCO</PERSONA>
<GRPDESCR>Lords.</GRPDESCR>
</PGROUP>
</PERSONAE>

<SCNDESCR>SCENE  A ship at Sea: an island.</SCNDESCR>

<PLAYSUBT>THE TEMPEST</PLAYSUBT>

<ACT><TITLE>ACT I</TITLE>

<SCENE><TITLE>SCENE I.  On a ship at sea: a tempestuous noise of thunder and lightning heard.</TITLE>

<STAGEDIR>Enter a Master and a Boatswain &amp;c</STAGEDIR>

<SPEECH>
<SPEAKER>Master</SPEAKER>
<LINE>Boatswain!</LINE>
</SPEECH>
</SCENE>

<SCENE><TITLE>SCENE II.  The island. Before PROSPERO'S cell.</TITLE>
<STAGEDIR>Enter PROSPERO and MIRANDA</STAGEDIR>

<SPEECH>
<SPEAKER>MIRANDA</SPEAKER>
<LINE>If by your art, my dearest father, you have</LINE>
<LINE>Put the wild waters in this roar, allay them.</LINE>
<LINE>The sky, it seems, would pour down stinking pitch,</LINE>
</SPEECH>

<SPEECH>
<SPEAKER>PROSPERO</SPEAKER>
<LINE>Come, follow. Speak not for him.</LINE>
</SPEECH>

<STAGEDIR>Exeunt</STAGEDIR>
</SCENE>
</ACT>
</PLAY>
'''
)

    def test_transform_html(self):
        t = shksprdata.getdata.moby.Transformer()
        out = t.to_html(self.intext)
        assert len(out) > 0
        assert 'PROSPERO' in out, out

    def test_norm_name(self):
        t = shksprdata.getdata.moby.Transformer()
        out = t.norm_name(None, 'ANTHONY')
        assert out == 'anthony', out

    def test_transform_latex(self):
        t = shksprdata.getdata.moby.Transformer()
        out = t.to_latex(self.intext)
        assert len(out) > 0
        assert 'Dramatis Personae' not in out
        assert r'\Character[GONZALO' in out, out
        # assert r'\Character[GONZALO, an honest old Counsellor.]{Gonzalo}' in out, out
        assert r'\GCharacter{ADRIAN}{ADRIAN}{adrian}' in out, out
        assert r'\act' in out
        assert r"\Scene{SCENE II.  The island. Before PROSPERO'S cell.}" in out, out
        assert r'\&c' in out, out

