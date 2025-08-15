from pypdf import PdfReader, PdfWriter,PaperSize, Transformation


def merge_pdfs(paths, output):
    pdf_writer = PdfWriter()

    for path in paths:
        pdf_reader = PdfReader(path)
        
        newPage = pdf_writer.add_blank_page(PaperSize.A4.width, PaperSize.A4.height)

        pdf_writer.add_page(pdf_reader.get_page(0))

    with open(output, 'wb') as out:
        pdf_writer.write(out)

class MergedPdf:
    def __init__(self):
       self.pdf_writer = PdfWriter() 
    def merge_twoPdfs_to_one(self,path1, path2,ty=450):
        pdf_reader = PdfReader(path1)
        srcA = pdf_reader.get_page(0)
        
        if path2!=None:
            pdf_reader = PdfReader(path2)
            srcB = pdf_reader.get_page(0)
        
        newPage = self.pdf_writer.add_blank_page(PaperSize.A4.width, PaperSize.A4.height)
        
        newPage.merge_translated_page(srcA,
                                      tx=0,#PaperSize.A4.width,
                ty=0,
                expand=True,
                over=True,)
        if srcB:
            newPage.merge_translated_page(srcB,
                                        tx=0,#PaperSize.A4.width,
                    ty=ty,
                    expand=True,
                    over=True,)
        
        
        

    def save(self, path):
        self.pdf_writer.write(path)

        


import os

def findPdf(rootPath):
    result=[]
    for root,ds,fs  in os.walk(rootPath):
        for f in fs:
            a=os.path.join(root,f)
            result.append(a)
    return result

a = findPdf('.//11')
meger = MergedPdf()
print(len(a))
for i in range(0,len(a),2):
    if i+1 < len(a):
        b = a[i+1]
    meger.merge_twoPdfs_to_one(a[i],b)
meger.save('merged.pdf')