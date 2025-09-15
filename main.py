import re
from pypdf import PdfReader, PdfWriter,PaperSize, Transformation

class PdfMoney:
    def __init__(self):
        pass

    def gotValue(self,text,key):
        num = text.find(key)
        if num==-1:
            print(f"can not fond {key}")
            return None
        num +=len(key)
        num_end = text.find("\n",num)    
        value = text[num:num_end]
        value = value.replace("：","").replace(" ","").replace("）","").replace("¥","").replace("￥","").replace(":","").replace(")","")
        
        return value

    def getPdfMoney(self,path):
        print("\n getPdfMoney "+path)
        self.pdf_reader = PdfReader(path)
        money_pattern = r'[￥$]?\d+(,\d{3})*(\.\d{1,2})?'  # 匹配金额的正则表达式
        found_money = []
        for page in self.pdf_reader.pages:
            text = page.extract_text()
            #print(text)
            
            num1 = "None" #self.gotValue(text,"发票代码")

            num2 = self.gotValue(text,"发票号码")

        
            num3 = self.gotValue(text,"小写")

            if text:
                money_list= re.findall(r'\d+\.\d+', text)
            print(money_list)
            print(num1,num2,num3)
        
        

        return self.pdf_reader.get_page(0).extract_text()
class MergedPdf:
    def __init__(self):
       self.pdf_writer = PdfWriter()

    def getPdfMoney(self,pdf_reader):
        for page in pdf_reader.pages:
                print(page.extract_text())
        
        return pdf_reader.get_page(0).extract_text() 
    def merge_twoPdfs_to_one(self,path1, path2,ty=450):
        pdf_reader = PdfReader(path1)
        srcA = pdf_reader.get_page(0)
        srcB=None
        if path2!=None:
            pdf_reader = PdfReader(path2)
            srcB = pdf_reader.get_page(0)
            self.getPdfMoney(pdf_reader)

            
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

def DoMerge():
    a = findPdf('.//11')
    meger = MergedPdf()
    print(len(a))
    for i in range(0,len(a),2):
        b=None
        if i+1 < len(a):
            b = a[i+1]
        meger.merge_twoPdfs_to_one(a[i],b)

    meger.save('merged.pdf')

def doGetMoney():
    a= findPdf('.//11')
    money = PdfMoney()
    for i in range(0,len(a)):
        money.getPdfMoney(a[i])

doGetMoney()
#DoMerge()