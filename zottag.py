#!/usr/bin/env python
# TODO:
#   Error should be a raise.
#   Customize rename filters
#   Add terminal colors for eye candy
#   Add counter/maximum to "adding"
#   Add a parameter to set just update after a given date, maybe saving a timestamp somewhere in
#   user dir.
#   In command args assumes USER by default, if missing.
#   Coalesce plurals into singulars
#   Find similar names and merge them???? Complicated..
#   Findout why tee do not work correctly, maybe need flush?

from pyzotero import zotero
import re
import sys

#%% Reading zotero library
def zotero_load_catalog(zotero_connector, verbose=True):
    """Load zotero catalog"""
    zotiter = zotero_connector.makeiter(zotero_connector.top())
    numitems = zotero_connector.num_items()

    i = 0
    allitems = []
    for items in zotiter:
        lastinfo = items[-1]['data']
        i += len(items)
        if verbose:
            print(f"{i:05d}/{numitems:05d} {lastinfo['key']}")
        allitems.extend(items)

    loaded_items = len(allitems)
    if loaded_items == numitems:
        if verbose:
            print(f'Success: All {loaded_items} loaded.')
    else:
        print (f'ERROR: Missing {num_items - loaded_items} items.')

    return allitems

#%% Retrieve all tags
def zotero_load_tags(zotero_connector, verbose=True):
    tagiter = zotero_connector.makeiter(zotero_connector.tags())
    i = 0
    alltags = []
    for tags in tagiter:
        i += len(tags)
        lasttag = tags[-1]
        if verbose:
            print(f"{i:05d} {lasttag}")
        alltags.extend(tags)

    return alltags

#%%
def tag_rename(tag):
    """Rename a tag, returning a list of new tags
    Input:
        tag string
    Output:
        tags: a list of tags
    """

    replacements = {
            'Neural and Evolutionary Computing':                ['neural computing', 'evolutionary computing'],
            'Picture and Image Generations':                    ['picture generation', 'image generation'],
            'Algebras, Linear':                                 ['linear algebra'],
            'Mathematics / Linear & Nonlinear Programming':     ['mathematics', 'linear programming', 'nonlinear programming'],
            'Mathematics / Applied':                            ['mathematics applied'],
            'math':                                             ['mathematics'],
            'math.':                                            ['mathematics'],
            'Math.':                                            ['mathematics'],
            }

    removals = [ 'general', 'etc', 'technique', 'general mathematics', 'math', 'math.' ]


    # If there is a full match in replacements, replace and exit
    if tag in replacements:
        new_tags = replacements[tag]
        return new_tags

    # Lowercase case them
    new_tags = tag.lower().strip().strip('.')
    # Remove closing parenthesis, since we will split on opening ones
    new_tags = new_tags.replace(')', '')
    # Remove multiple spaces
    new_tags = re.sub(r' +',  ' ', new_tags)
    # Split them!
    new_tags = re.split(r' and | / | - | -- | \(| \| | , |, | & | : ', new_tags)

    new_tags = list(set(new_tags))

    # Remove useless tags
    for word in removals:
        if word in new_tags:
            new_tags.remove(word)

    num_of_new_tags = len(new_tags)
    # We have splitted in multiple tags
    if num_of_new_tags> 1:
        return new_tags
    elif (num_of_new_tags == 1) and (new_tags[0] != tag):
        return new_tags
    else:
        # We havent changed anything. (or something weirder)
        return None

#%%
def process_tags(items, tags, verbose=True):
    """Process tags using tag_rename Rules

    Input:
        items: A list of zotero dictionary

    Output:
        tags_to_add: dict - a dictionary of key: [tags] to add
        tags_to_del: list - a list of tags to be removed
    """

    # A list of tags to be removed from database
    tags_to_del = []
    # A dictionary of tags to be added. The key item and the value is a list of tags
    tags_to_add = {}
    longest = len(max(alltags, key=len))

    for item in items:
        info = item['data']
        key = info['key']
        tags_to_add[key] = []
        item_tags = []
        for tagentry in info['tags']:
            tag = tagentry['tag']
            newtags = tag_rename(tag)
            if newtags is not None:
                tags_to_del.append(tag)
                tags_to_add[key].extend(newtags)
                if verbose:
                    print(f"{key}: {tag:>{longest}} --> {newtags}")

    tags_to_del = list(set(tags_to_del))
    tags_to_add = { k: v for (k, v) in tags_to_add.items() if len(v) > 0 }

    return tags_to_add, tags_to_del

#%%
def build_key_index(allitems):
    keytoidx = {}
    for idx, item in enumerate(allitems):
        key = item['key']
        keytoidx[key] = idx

    return keytoidx

#%%
def add_new_tags(zotero_connector, tags_to_add, allitems, verbose=True):
    """Add tags to items. Return tags that failed to add"""
    if verbose:
        print("Building index...")

    keytoidx = build_key_index(allitems)
    failed_to_add = []
    for key, tags in tags_to_add.items():
            item = allitems[keytoidx[key]]
            if verbose:
                print(f"{key} adding {tags}. ", end="")
            if zotero_connector.add_tags(item, *tags):
                if verbose:
                    print("SUCCESS")
            else:
                failed_to_add.append(key)
                if verbose:
                    print("FAILURE")

    return failed_to_add

#%%
def split_list(l, size=50):
    for i in range(0, len(l), size):
        yield l[i:i + size]

#%%
def delete_tags(zotero_connector, tags, verbose=True):
        # Defined on server size, maximum number of tags to
        # delete each time may change in future
        size = 50
        nchunks = len(tags)//size + 1
        for n, tag_chunk in enumerate(split_list(tags, size)):
            print(f"Delete batch {n+1:3d}/{nchunks}: {tag_chunk[0]}")
            zotero_connector.delete_tags(*tag_chunk)

#%% Main
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} ZOTEROID APIKEY <user|group> ")
        sys.exit()
    else:
        zoteroid = sys.argv[1]
        zoterokey = sys.argv[2]
        zoterotp = sys.argv[3]

    #%% access your library
    zot = zotero.Zotero(zoteroid, zoterotp, zoterokey, preserve_json_order=True)

    #%%
    print("Loading catalogs...")
    allitems = zotero_load_catalog(zot, verbose=True)

    #%%
    print("Loading all tags...")
    alltags = zotero_load_tags(zot, verbose=True)

    #%%
    tags_to_add, tags_to_del = process_tags(allitems, alltags, verbose=True)

    #%%
    print(f"{len(tags_to_add)} items need new tags")
    print(f"{len(tags_to_del)} tags need to be removed")

    #%% tags_to_add allitems
    failed_to_add = add_new_tags(zot, tags_to_add, allitems, verbose=True)

    #%%
    if len(failed_to_add) == 0:
        delete_tags(zot, tags_to_del, verbose=True)
    else:
        print(f"We had a issue adding the tags to:\n\n{failed_to_add}\n\nPlease check.")
        sys.exit()

    print("Everything went amazing! You can sync your Zotero for hapiness")
