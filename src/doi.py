#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    # python3
    from urllib.request import urlopen
except:
    # python2
    from urllib2 import urlopen
from .ordereddict import OrderedDict 
import json
import sys, os
from time import sleep
try:
    import sqlite3
    HAS_SQLITE3 = True
except ImportError:
    HAS_SQLITE3 = False

def doi2papers(doi):
    '''search a paper via doi in crossref database; return a json object'''
    url = "http://api.labs.crossref.org/{0}.json".format(doi)
    count = 0
    limit = 5
    msg = ''
    while count < limit:
        try:
            paper = json.loads(urlopen(url).read().decode('utf-8'))
            break
        except Exception as e:
            msg = e
            sleep(1)
            count += 1
            continue
    if count >= limit:
        raise ValueError('{0}'.format(msg))
    return paper

class PaperList:
    def __init__(self, db, ext = '.json'):
        self.db_ext = ext
        self.filename = db if db.endswith(self.db_ext) else db + self.db_ext
        self.db = self.loadDB(self.filename)
        self.updated = True

    def loadDB(self, fn):
        '''load data if database file exists, otherwise create a new one'''
        try:
            return json.load(open(fn))
        except:
            return json.loads(json.dumps({}))

    def addPaper(self, doi, paper = None, overwrite = False):
        ''' add a new paper (json format) into paperlist, return a pair of boolean:
        first to say if sucess to add; second to say if find a existing one'''
        if doi in self.getDoi():
            if overwrite:
                try:
                    self.db[doi] = doi2papers(doi) if not paper else paper
                    self.updated = True
                    return ('found', 'exists')
                except:
                    return ('not found', 'exists')
            else:
                return ('not searched', 'exists')
        else:
            try:
                self.db[doi] = doi2papers(doi) if not paper else paper
                self.updated = True
                return ('found', 'not exist')
            except:
                return ('not found', 'not exist')

    def getDoi(self):
        doi = set()
        for key, value in self.db.items():
            doi.add(key)
        return list(doi)

    def getAuthors(self, paper):
        try:
            info = paper['doi_record']['crossref']['journal']['journal_article']['contributors']
            info = [x['given_name'] + ' ' + x['surname'] for x in info if x['contributor_role'] == 'author']
            if len(info) == 1:
                info = info[0]
            else:
                info = ', '.join(info[:-1]) + ' and ' + info[-1]
        except:
            info = ''
        return info

    def getTitle(self, paper):
        try:
            info = paper['doi_record']['crossref']['journal']['journal_article']['titles']['title']
        except:
            info = ''
        return info

    def getJournal(self, paper):
        try:
            info = paper['doi_record']['crossref']['journal']['journal_metadata']['full_title']
        except:
            info = ''
        return info
    
    def getDate(self, paper):
        try:
            info = paper['doi_record']['crossref']['journal']['journal_article']['publication_date']
            try:
                info = info['year']
            except:
                info = [x['year'] for x in info if 'year' in x.keys()][0]
        except:
            info = ''
        return info

    def getLink(self, paper):
        try:
            info = paper['doi_record']['crossref']['journal']['journal_article']['doi_data']['resource']
        except:
            info = '-'
        return info
        
    def getInfo(self, paper, info):
        text = eval('self.get{0}'.format(info.capitalize()))(paper)
        return text.encode('utf-8')

    def extract(self, doi):
        paper = self.db[doi]
        info = OrderedDict()
        info["authors"] = self.getInfo(paper, "authors")
        info["title"] = self.getInfo(paper, "title")
        info["date"] = self.getInfo(paper, "date")
        info["journal"] = self.getInfo(paper, "journal")
        info["DOI"] = doi
        info["link"] = self.getInfo(paper, "link")
        return info

    def dump(self):
        if self.updated == True:
            with open(self.filename, 'w') as f:
                f.write(json.dumps(self.db))

class PapersDB:
    def __init__(self, tblname, fields):
        self.name = tblname
        self.fields = [(x, 'VARCHAR (255)') for x in fields]
        self.fields.append(('status', 'VARCHAR (255)'))
        self.PH = '?'
        self.create_query = 'CREATE TABLE {0} ({1});'.format(self.name, ','.join([' '.join(x) for x in self.fields]))
        self.insert_query = 'INSERT INTO {0} ({1}) VALUES ({2});'.format(
                self.name,
                ','.join([x[0] for x in self.fields]),
                ','.join([self.PH] * len(self.fields))
                )

    def write(self, data):
        data = [x + [None] for x in data]
        writer = sqlite3.connect(":memory:")
        cur = writer.cursor()
        cur.execute(self.create_query)
        cur.executemany(self.insert_query, data)
        writer.commit()
        print("\n".join(writer.iterdump()))
