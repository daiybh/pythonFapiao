

import os

from qqOcr import TencentOCR

from dotenv import load_dotenv
load_dotenv()

def findPdf(rootPath):
    result=[]
    for root,ds,fs  in os.walk(rootPath):
        for f in fs:
            a=os.path.join(root,f)
            result.append(a)
    return result

import csv
if __name__ == '__main__':  
   
    pdfs = findPdf(os.environ.get('LOCAL_SEARCH_FOLDER'))
    
    ocr = TencentOCR()
    with open('result.csv', 'w',newline='', encoding='utf-8-sig') as f:
        IwriteCount=0
        for pdf in pdfs:
            print(pdf)    
            b = ocr.recognize_general_invoice(pdf)
            print(b)
            if b is None:
                print("无法识别该发票")
                continue
            #b is  {'发票号码': '25142000000063736402', '开票日期': '2025年08月08日', '合计金额': '195.00', '类型': '*餐饮服务*餐费', 'BuyerTaxID': '91510100MA6DEAAJ2E', 'Buyer': '盛利来(成都)科技有限公司'}
            # need save b into a  csv file
            if IwriteCount==0:
                fieldnames = b.keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            IwriteCount+=1
            writer.writerow(b)

    
    