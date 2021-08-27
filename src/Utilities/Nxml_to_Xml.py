import re
import os

'''
This file is used to convert NXML file to XML file.
'''
class NxmlConversion:

    def __init__(self, source_dir, dest_dir):
        self.dest_dir = dest_dir
        self.source_dir = source_dir

    def convert_nxml_to_xml(self):
        src_dir = os.listdir(self.source_dir)
        for dir in src_dir:
            sub_dir = os.listdir(self.source_dir + '/' + dir)
            for sdir in sub_dir:
                nxml_files = os.listdir(self.source_dir + '/' + dir + '/' + sdir)
                if not os.path.exists(self.dest_dir + '/' + dir + '/' + sdir):
                    os.makedirs(self.dest_dir + '/' + dir + '/' + sdir)
                for nxml in nxml_files:
                    base = os.path.split(nxml)
                    fileName = os.path.splitext(base[1])
                    dest_file = self.dest_dir + '/' + dir + '/' + sdir + '/' + fileName[0] + '.xml'
                    trec_file = open(dest_file, "a")
                    trec_file.write('<DOC>\n')
                    pmc_file = open(self.source_dir + '/' + dir + '/' + sdir + '/' + nxml).read()
                    searchPMID = re.search(r'<article-id pub-id-type="pmc">(.*?)</article-id>', pmc_file, re.M | re.I)
                    trec_file.write('<DOCNO>{0}</DOCNO>\n'.format(searchPMID.group(1)))
                    trec_file.write('<TEXT>\n')

                    # Journal ID
                    searchJournalTitle = re.search(r'<journal-title>(.*?)</journal-title>', pmc_file, re.M | re.I)
                    JournalTitle = re.sub(r'<(.*?)>', ' ', searchJournalTitle.group(1))
                    JournalTitle = re.sub(r'</(.*?)>', ' ', JournalTitle)
                    JournalTitle = re.sub(r'&#.*?;', ' ', JournalTitle)
                    JournalTitle = re.sub(' +', ' ', JournalTitle)
                    trec_file.write('<journal-title>{0}</journal-title>\n'.format(JournalTitle))

                    # Article Type:
                    searchArticleType = re.search('article-type="(.*?)"', pmc_file)
                    trec_file.write('<article-type>{0}</article-type>\n'.format(searchArticleType.group(1)))

                    # Article Title
                    searchArticleTitle = re.search(r'<article-title(.*?)>(.*?)</article-title>', pmc_file,
                                                   re.M | re.I | re.DOTALL)
                    if searchArticleTitle:
                        ArticleTitle = re.sub(r'<(.*?)>', ' ', searchArticleTitle.group(2))
                        ArticleTitle = re.sub(r'</(.*?)>', ' ', ArticleTitle)
                        ArticleTitle = re.sub(r'&#.*?;', ' ', ArticleTitle)
                        ArticleTitle = re.sub(' +', ' ', ArticleTitle)
                        # print(ArticleTitle)
                        trec_file.write('<article-title>{0}</article-title>\n'.format(ArticleTitle))
                    else:
                        trec_file.write('<article-title></article-title>\n')
                    # Abstract
                    searchAbstract = re.search(r'<abstract(.*?)>(.*?)</abstract>', pmc_file, re.M | re.I | re.DOTALL)
                    if searchAbstract:
                        abstract_paras = re.findall(r'<p>(.*?)</p>', searchAbstract.group(2))
                        # print(searchAbstract.group(1))
                        abstract_paras = "\n".join(abstract_paras)
                        abstract_paras = re.sub(r'<(.*?)>', ' ', abstract_paras)
                        abstract_paras = re.sub(r'</(.*?)>', ' ', abstract_paras)
                        abstract_paras = re.sub(r'&#.*?;', ' ', abstract_paras)
                        abstract_paras = re.sub(' +', ' ', abstract_paras)
                        trec_file.write('<abstract>{0}</abstract>\n'.format(abstract_paras))
                    else:
                        trec_file.write('<abstract></abstract>\n')
                    # Keywords of article
                    searchKeyword = re.search(r'<kwd-group>(.*?)</kwd-group>', pmc_file, re.M | re.I | re.DOTALL)
                    if searchKeyword:
                        keywords = re.sub(r'<kwd>|</kwd>', ',', searchKeyword.group(1))
                        # keywords=re.sub(r'</kwd>',' ',keywords)
                        # print(keywords)
                        trec_file.write('<keywords>{0}</keywords>\n'.format(keywords))

                    else:
                        trec_file.write('<keywords></keywords>\n')

                    # Body of article
                    searchBody = re.search(r'<body(.*?)>(.*?)</body>', pmc_file, re.M | re.I | re.DOTALL)
                    if searchBody:

                        # Subheadings
                        subheads = re.findall(r'<title(.*?)>(.*?)</title>', searchBody.group(2),
                                              re.M | re.I | re.DOTALL)
                        coma = ","
                        subheadings = []
                        if subheads:
                            for i in range(0, len(subheads)):
                                subheadings.append(subheads[i][1])
                            subheading = re.sub(r'<(.*?)>', ' ', coma.join(subheadings))
                            subheading = re.sub(r'\[(.*?)\]', ' ', subheading)
                            subheading = re.sub(r'</(.*?)>', ' ', subheading)
                            subheading = re.sub(r'&#.*?;', ' ', subheading)
                            subheading = re.sub(' +', ' ', subheading)
                            trec_file.write('<subheading>{0}</subheading>\n'.format(subheading))
                        else:
                            trec_file.write('<subheading></subheading>\n')

                        # Introduction para
                        intro = re.findall('</title>(.*?)<title', searchBody.group(2))
                        if intro:
                            introduction = re.sub(r'<(.*?)>', ' ', intro[0])
                            introduction = re.sub(r'\[(.*?)\]', ' ', introduction)
                            introduction = re.sub(r'</(.*?)>', ' ', introduction)
                            introduction = re.sub(r'&#.*?;', ' ', introduction)
                            introduction = re.sub(' +', ' ', introduction)
                            trec_file.write('<introduction>{0}</introduction>\n'.format(introduction))
                        elif len(intro) == 0:
                            introduction = searchBody.group(2)
                            introduction = re.sub(r'<(.*?)>', ' ', introduction)
                            introduction = re.sub(r'\[(.*?)\]', ' ', introduction)
                            introduction = re.sub(r'</(.*?)>', ' ', introduction)
                            introduction = re.sub(r'&#.*?;', ' ', introduction)
                            introduction = re.sub(' +', ' ', introduction)
                            trec_file.write('<introduction>{0}</introduction>\n'.format(introduction))
                        else:
                            trec_file.write('<introduction></introduction>\n')

                        # Conclusion para
                        if len(subheads) != 0:
                            sections = re.split('</title>', searchBody.group(2))
                            del sections[0]
                            cl_flag = 0
                            for i in range(len(subheads) - 1, 0, -1):
                                conclude1 = re.search(r'\bconclusions?\b', str(subheads[i]), re.IGNORECASE)
                                conclude2 = re.search(r'\bresults?\b', str(subheads[i]), re.IGNORECASE)
                                conclude3 = re.search(r'\bdiscussions?\b', str(subheads[i]), re.IGNORECASE)
                                if conclude1:
                                    conclusion = re.sub(r'<(.*?)>', ' ', sections[i])
                                    conclusion = re.sub(r'\[(.*?)\]', ' ', conclusion)
                                    conclusion = re.sub(r'</(.*?)>', ' ', conclusion)
                                    conclusion = re.sub(r'&#.*?;', ' ', conclusion)
                                    conclusion = re.sub(' +', ' ', conclusion)
                                    cl_flag = 1
                                    trec_file.write('<conclusion>{0}</conclusion>'.format(conclusion))
                                    break
                                elif conclude2:
                                    conclusion = re.sub(r'<(.*?)>', ' ', sections[i])
                                    conclusion = re.sub(r'\[(.*?)\]', ' ', conclusion)
                                    conclusion = re.sub(r'</(.*?)>', ' ', conclusion)
                                    conclusion = re.sub(r'&#.*?;', ' ', conclusion)
                                    conclusion = re.sub(' +', ' ', conclusion)
                                    cl_flag = 1
                                    trec_file.write('<conclusion>{0}</conclusion>'.format(conclusion))
                                    break
                                elif conclude3:
                                    conclusion = re.sub(r'<(.*?)>', ' ', sections[i])
                                    conclusion = re.sub(r'\[(.*?)\]', ' ', conclusion)
                                    conclusion = re.sub(r'</(.*?)>', ' ', conclusion)
                                    conclusion = re.sub(r'&#.*?;', ' ', conclusion)
                                    conclusion = re.sub(' +', ' ', conclusion)
                                    cl_flag = 1
                                    trec_file.write('<conclusion>{0}</conclusion>'.format(conclusion))
                                    break
                            if cl_flag == 0:
                                trec_file.write('<conclusion></conclusion>\n')
                        else:
                            trec_file.write('<conclusion></conclusion>\n')

                    else:
                        trec_file.write('<subheading></subheading>\n')
                        trec_file.write('<introduction></introduction>\n')
                        trec_file.write('<conclusion></conclusion>\n')
                    trec_file.write('</TEXT>\n')
                    trec_file.write('</DOC>\n')

#nxml_obj = NxmlConversion("/home/iialab/Bhanu/PythonFiles/2016TrecInput" , "/home/iialab/Bhanu/PythonFiles/2016_Trec_xml")
#nxml_obj.convert_nxml_to_xml()
#print("Conversion is Done")