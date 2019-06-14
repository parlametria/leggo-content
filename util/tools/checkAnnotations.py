import sys
import os
import nltk
import pdb

class DocAnn:

    def __init__(self, filename = None, ann_lst = []):

        self.filename = filename
        self.annotations = ann_lst
        self.vocab = {}

    def read(self, filename):
        fd = open(filename, 'r')
        self.filename = filename
        self.annotations = []
        for line in fd:
            line_split = line.split('\t')
            id_ann = line_split[0]

            info_ann = line_split[1]
            info_ann_lst = info_ann.split()

            tag = info_ann_lst[0]
            start = int(info_ann_lst[1])
            end = int(info_ann_lst[-1])

            self.annotations.append((tag, start, end))

            txt_ann = line_split[2]
            tok_lst = nltk.word_tokenize(txt_ann.replace('\n',''))
            for tok in tok_lst:
                if tok in self.vocab:
                    self.vocab[tok] = self.vocab[tok] + 1
                else:
                    self.vocab[tok] = 1

    def countDiffAnnotations(self, doc):

        count = 0
        totalW = sum([ doc.vocab[w] for w in doc.vocab])

        for w in doc.vocab:

            if w in self.vocab:
                count = count + abs(self.vocab[w] - doc.vocab[w])
            else:
                count = count + doc.vocab[w]

        if totalW != 0:
            return count / totalW

        return totalW

def read_ann(dir_ann):

    file_lst = os.listdir(dir_ann)
    doc_lst = []

    for f in file_lst:
        if f.endswith('.ann'):
            doc = DocAnn()
            doc.read(os.path.join(dir_ann, f))
            doc_lst.append(doc)

    return doc_lst

def convert2Bio(docann_lst):
    # from the stand-off format to bio format
    docTags = []
    for doc in docann_lst:
        fname_txt = "%s.txt" % os.path.splitext(doc.filename)[0]
        fd_txt = open(fname_txt, "r")
        txt_ = fd_txt.read()
        bioTags = []

        idx = 0
        start = None
        end = None
        startAnn = None
        endAnn = None
        currentTag = 'O'

        if len(doc.annotations) > 0:
            startAnn = doc.annotations[0][1]
            endAnn = doc.annotations[0][2]
            start = 0
            end = startAnn


        while start < len(txt_):
            chunk = txt_[start:end]
            tok_lst = nltk.word_tokenize(chunk)

            if currentTag == 'O':
                bioTags = bioTags + [(tok, 'O') for tok in tok_lst]

                currentTag = doc.annotations[idx][0]
                start = end
                end = doc.annotations[idx][2]
            else:
                if len(tok_lst) > 0:
                    bioTags = bioTags + [(tok_lst[0], "B-%s" % currentTag)]

                idx_tok = 1
                while idx_tok < len(tok_lst) - 1:
                    bioTags.append((tok_lst[idx_tok],"I-%s" % currentTag))
                    idx_tok = idx_tok + 1

                if len(tok_lst) > 1:
                    bioTags = bioTags + [(tok_lst[-1], "E-%s" % currentTag)]

                # update indexes

                # still have some annotations
                if idx + 1 < len(doc.annotations):

                    startAnn = doc.annotations[idx + 1][1]
                    endAnn = doc.annotations[idx + 1][2]

                    # some out annotations to process
                    if (end - startAnn > 1):
                        currentTag = 'O'
                        start = end
                        end = startAnn
                    else:
                        currentTag = doc.annotations[idx + 1][0]
                        start = startAnn
                        end = endAnn
                else:
                    start = end
                    end = len(txt_)

            idx = idx + 1
        docTags.append(bioTags)
        if len(docTags) == 2:
            break

    return docTags

def compare_annotations(annotations1, annotations2):

    annotations1.sort(key=lambda x:x.filename)
    annotations2.sort(key=lambda x:x.filename)
    diff_lst = []

    n1 = len(annotations1)
    n2 = len(annotations2)
    n = min(n1, n2)
    j = 0
    while j < n1:
       k = 0
       while k < n2:
           fname1 = os.path.basename(annotations1[j].filename)
           fname2 = os.path.basename(annotations2[k].filename)
           if fname1 == fname2:
              diff = annotations1[j].countDiffAnnotations(annotations2[k])
              diff_lst.append(diff)
              break
           k = k + 1
       j = j + 1

    
    return sum(diff_lst)/ len(diff_lst)

if __name__ == '__main__':
    dir_ann1 = sys.argv[1]
    dir_ann2 = None

    doc_lst_ann1 = read_ann(dir_ann1)
    if len(sys.argv) > 2:
        dir_ann2 = sys.argv[2]
        doc_lst_ann2 = read_ann(dir_ann2)
        print(compare_annotations(doc_lst_ann1, doc_lst_ann2))
    else:
        doctags = convert2Bio(doc_lst_ann1)
        for doc in doctags:
           print()
           for (tok, tag) in doc:
               print("%s\t%s" % (tok, tag))
           print()
