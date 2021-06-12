Zotero Tag Renamer
==================

Rename  and cleanup all tags in your zotero database. You need a zotero API Key

What it does
=============

This small python code renames all your tags based in the following rules:

1. All lowercase

2. Clean up blanks and dots in start/end of tags

3. Remove multiple spaces

4. Split tags with " and ", " / ", " - ", " -- ", " (", " | ", " : ", " & ", " ," in multiple tags

5. Remove useless tags as "etc", "general", "generic".

6. And some pontual replacements for example:
  - 'Neural and Evolutionary Computing':                ['neural computing', 'evolutionary computing'],
  - 'Picture and Image Generations':                    ['picture generation', 'image generation'],
  - 'Algebras, Linear':                                 ['linear algebra'],
  - 'Mathematics / Linear & Nonlinear Programming':     ['mathematics', 'linear programming', 'nonlinear programming'],
  - 'Mathematics / Applied':                            ['mathematics applied']


What it do not do
==================

Many things ...

1. No GUI

2. Not so simple to customize renaming rules (need to know a bit of
   python/regex)

3. Error handling not done.

4. No eye candy

5. Can trigger the third world war

6. No support


HOW TO USE
==========

1. Clone this repo

2. `chmod 755 zottag.py`

3. `./zottag.py ZOTEROID  APIKEY <user|group>`

Example:

```
user@localhost$ ./zottag.py 123456 23wfds2435fwdf4252fs user
```

HOW TO CUSTOMIZE
================

To customize the filters edit the source code and take a look at function `tag_rename()`.

More info in how to create Zotero keys:

[https://www.zotero.org/settings/keys](https://www.zotero.org/settings/keys)


LICENSE
=======

GNU/GPL version 3. As below

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
