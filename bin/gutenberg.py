"""Various useful functionality related to Project Gutenberg
"""
import os
import StringIO
import shakespeare.gutenberg


class GutenbergIndex(shakespeare.gutenberg.GutenbergIndexBase):
    """Parse the index of Gutenberg works so as to find Shakespeare works.
    """
    
    def get_relevant_works(self):
        """Get list of shakespeare works and urls.

        Results are sorted by work title.

        Notes regarding list of plays:

          * no Folio edition of Troilus and Cressida
          * no Folio edition of Pericles
        """
        # results have format [ title, url, comments ]
        # folio in comments indicates it is a first folio
        results = [ ["Sonnets", 'http://www.gutenberg.org/dirs/etext97/wssnt10.txt', ''] ]
        plays = self._extract_shakespeare_works()
        for play in plays:
            url = self.make_url(play[1], play[2])
            results.append([play[0], url, play[3]])
        # add in by hand some exceptions
        results.append(["The Winter's Tale",
                'http://www.gutenberg.org/files/1539/1539.txt', '']
                )
        def compare_list(item1, item2):
            if item1[0] > item2[0]: return 1
            else: return -1
        results.sort(compare_list)
        return results
    
    def _extract_shakespeare_works(self):
        """Get non-copyrighted Shakespeare works from Gutenberg
        Results consist of folio and one other 'standard' version.
        @return: list consisting of tuples in form [title, year, id, comment]
        """
        ff = file(self._gutindex_local_path)
        results = []
        for line in ff.readlines():
            result = self.parse_line_for_folio(line)
            if result:
                results.append(result + ['folio'])
            resultNormal = self.parse_line_for_normal(line)
            if resultNormal:
                results.append(resultNormal + [''])
        return results
    
    def parse_line_for_normal(self, line):
        """Parse GUTINDEX for 'normal' gutenberg shakespeare versions (i.e. not
        folio and out of copyright).
        """
        # normal shakespeare are those with id starting [2
        # most have 'by William Shakespeare' but also have 'by Shakespeare'
        # (Othello) and 'by Wm Shakespeare' (Titus Andronicus)
        # everything is by William Shakespeare except for Othello
        if ('Shakespeare' in line and '[2' in line
                and 'mp3' not in line and 'Apocrypha' not in line):
            year = line[4:8]
            tmp = line[9:]
            endOfTitle = tmp.find(', by')
            title = tmp[:endOfTitle]
            startOfId = tmp.find('[2')
            endOfId = tmp.find(']', startOfId)
            idStr = tmp[startOfId+1:endOfId]
            xstart = idStr.find('x')
            idStr = idStr[:xstart]
            return [title, year, idStr]
        
    def parse_line_for_folio(self, line):
        if '[FF]' in line:
            year = line[4:8]
            tmp = line[9:]
            endOfTitle = tmp.find(', by')
            title = tmp[:endOfTitle]
            startOfId = tmp.find('[FF]') + 5
            endOfId = tmp.find(']', startOfId)
            idStr = tmp[startOfId+1:endOfId]
            xstart = idStr.find('x')
            idStr = idStr[:xstart]
            return [title, year, idStr]
        else:
            return None


class Helper(shakespeare.gutenberg.HelperBase):

    def clean(self, line=None):
        '''See parent class.
        '''
        textsToProcess = self._filter_index(line) 
        for item in textsToProcess:
            url = item[1]
            src = self.cache.path(url)
            dest = self.cache.path(url, 'plain')
            if os.path.exists(dest):
                if self.verbose:
                    print 'Skip clean of %s as clean version already exists' % src
                continue
            if self.verbose:
                print 'Formatting %s to %s' % (src, dest)
            infile = file(src)
            if src.endswith('wssnt10.txt'): # if it is the sonnets need a hack
                # delete last 140 characters
                tmp1 = infile.read()
                infile = StringIO.StringIO(tmp1[:-120])
            formatter = shakespeare.gutenberg.GutenbergCleaner(infile)
            ff = file(dest, 'w')
            out = formatter.extract_text()
            ff.write(out)
            ff.close()

    def add_to_db(self):
        """Add all gutenberg texts to the db list of texts.
        
        If a text already exists in the db it will be skipped.
        """
        import shakespeare.model
        for text in self._index:
            title = text[0]
            name = self.title_to_name(title) + '_gut'
            url = text[1]
            notes = 'Sourced from Project Gutenberg (url=%s). %s' % (text[1],
                    text[2])
            if text[2] == 'folio':
                name += '_f'
            
            numExistingTexts = shakespeare.model.Material.query.filter_by(
                        name=name).count()
            if numExistingTexts > 0:
                if self.verbose:
                    print('Skip: Add to db. Gutenberg text already exists with name: %s' % name)
            else:
                if self.verbose:
                    print('Add to db. Gutenberg text named [%s]' % name)
                shakespeare.model.Material(name=name,
                                        title=title,
                                        creator='Shakespeare, William',
                                        url=url,
                                        notes=notes)

