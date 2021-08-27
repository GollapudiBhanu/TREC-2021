import ir_datasets
from ir_datasets.datasets.base import YamlDocumentation
from ir_datasets.formats import TsvDocs, TsvQueries, TrecQrels

dataset = ir_datasets.create_dataset(
    docs_tsv='test/dummy/docs.tsv',
    queries_tsv='test/dummy/queries.tsv',
    qrels_trec='test/dummy/qrels'
)
