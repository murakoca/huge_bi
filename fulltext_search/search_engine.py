from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os, shutil

class SearchEngine:
    def __init__(self, index_dir="indexdir"):
        self.index_dir = index_dir
        self.schema = Schema(id=ID(stored=True), content=TEXT)
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            self.ix = create_in(index_dir, self.schema)
        else:
            self.ix = open_dir(index_dir)

    def add_document(self, doc_id, content):
        writer = self.ix.writer()
        writer.add_document(id=doc_id, content=content)
        writer.commit()

    def search(self, query_str):
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(query_str)
            results = searcher.search(query)
            return [hit['id'] for hit in results]