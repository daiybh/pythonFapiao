from pypdf import PdfReader, PdfWriter,PaperSize, Transformation

from dotenv import load_dotenv

from qqOcr import TencentOCR
load_dotenv()

class MergedPdf:
    def __init__(self):
       self.pdf_writer = PdfWriter()

    
    def merge_twoPdfs_to_one(self,path1, path2,ty=450):
        pdf_reader = PdfReader(path1)
        srcA = pdf_reader.get_page(0)
        srcB=None
        if path2!=None:
            print(path2)
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
            if 'pdf' in f:
                a=os.path.join(root,f)
                result.append(a)
    return result

def DoMerge():
    a = findPdf(os.environ.get('LOCAL_SEARCH_FOLDER'))
    meger = MergedPdf()
    print(len(a))
    ocr = TencentOCR()
    totalMoney = 0
    for i in range(0,len(a),2):
        b=None
        aocr = ocr.recognize_general_invoice(a[i])
        totalMoney += float(aocr['合计金额'])
        if i+1 < len(a):
            b = a[i+1]
            bocr = ocr.recognize_general_invoice(b)
            totalMoney += float(bocr['合计金额'])
        meger.merge_twoPdfs_to_one(a[i],b)
    print(totalMoney)
    meger.save(f'merged-{totalMoney}.pdf')


DoMerge()