This is a data package for Shakespeare material and includes data and templates
for runnning http://openshakespeare.org/.

INSTALL
=======

1. Install shakespeare package and this package.

   E.g. to do this from source::

     -e hg+https://bitbucket.org/okfn/shakespeare#egg=shakespeare
     -e hg+https://knowledgeforge.net/shakespeare/shkspr#egg=shksprdata

2. Follow shakespeare install instructions

3. Configure for openshakespeare.org.

  1. Set extra_template_paths to shksprdata/templates
  2. Symlink shksprdata/img to shakespeare/public/img/shkspr

