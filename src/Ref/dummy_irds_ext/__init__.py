import ir_datasets
from ir_datasets.formats import TsvDocs, TsvQueries, TrecQrels


# A unique identifier for this dataset. To avoid name conflicts, consider prefixing
# identifiers with a person/org, as done here:
NAME = 'Bhanu/UNT:TREC2016'

# What to the relevance levels in qrels mean?
QREL_DEFS = {
	1: 'relevant',
	0: 'not relevant',
}

# Specify where to find the content. Here it's just from the repository, but it could be anywhere.
#DL_DOCS = ir_datasets.util.RequestsDownload('https://raw.githubusercontent.com/seanmacavaney/dummy-irds-ext/master/data/docs.tsv')
#DL_QUERIES = ir_datasets.util.RequestsDownload('https://raw.githubusercontent.com/seanmacavaney/dummy-irds-ext/master/data/queries.tsv')
#DL_QRELS = ir_datasets.util.RequestsDownload('https://raw.githubusercontent.com/seanmacavaney/dummy-irds-ext/master/data/qrels')
DL_DOCS = '/home/junhua/trec/Trec2021/Output/doc_res_2016.tsv'
DL_QUERIES = '/home/junhua/trec/Trec2021/Output/qrels_2016.tsv'
DL_QRELS = '/home/junhua/trec/Trec2021/Output/qrels-treceval-2016'

# where the content is cached
base_path = ir_datasets.util.home_path() / NAME

# Dataset definition: it provides docs, queries, and qrels
dataset = ir_datasets.Dataset(
	TsvDocs(ir_datasets.util.Cache(DL_DOCS, base_path/'docs.tsv')),
	TsvQueries(ir_datasets.util.Cache(DL_QUERIES, base_path/'queries.tsv')),
	TrecQrels(ir_datasets.util.Cache(DL_QRELS, base_path/'qrels'), QREL_DEFS),
)

# Register the dataset with ir_datasets
ir_datasets.registry.register(NAME, dataset)

#print(ir_datasets.registry.register(NAME, dataset))
