# -*- coding: utf-8 -*-

import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

from dotenv import load_dotenv
load_dotenv()
    
class TencentOCR:
    def __init__(self,  region="ap-guangzhou"):
        """
        初始化腾讯云OCR客户端
        
        Args:
            secret_id: 腾讯云SecretId
            secret_key: 腾讯云SecretKey
            region: 区域，默认为ap-guangzhou
        """
        # 从环境变量获取
        secret_id = os.environ.get('TENCENT_SECRET_ID')
        secret_key = os.environ.get('TENCENT_SECRET_KEY')  

        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """初始化OCR客户端"""
        try:
            cred = credential.Credential(secret_id=self.secret_id, secret_key=self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"
            
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            
            return ocr_client.OcrClient(cred, self.region, clientProfile)
        except TencentCloudSDKException as err:
            print(f"初始化OCR客户端失败: {err}")
            return None
    
    
    def recognize_general_invoice(self, image_path):
        """
        识别通用发票
        :param image_path: 图片路径
        :return: 识别结果
        """
        
        if not self.client:
            return None
            
        try:
            req = models.RecognizeGeneralInvoiceRequest()
            params = {
                "ImageBase64": self._get_file_content(image_path),
                "ItemNamesShowMode": True,
                "ReturnFullText": False,
                "ConfigId": "General",
                "EnableCoord": False

            }
            req.from_json_string(json.dumps(params))
            
            resp = self.client.RecognizeGeneralInvoice(req)
            return self._pickFapiaoInfo(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(f"发票识别失败: {err}")
            return None
    

    def _pickFapiaoInfo(self,str_invoice_info):
        # 电子发票（铁路电子客票）
        #MixedInvoiceItems SingleInvoiceInfos ElectronicTrainTicketFull Fare
        invoice_info = json.loads(str_invoice_info)
        #print(invoice_info)
        MixedInvoiceItems= invoice_info['MixedInvoiceItems'][0]
        SingleInvoiceInfos  = MixedInvoiceItems['SingleInvoiceInfos']
        ElectronicTrainTicketFull = SingleInvoiceInfos['ElectronicTrainTicketFull']
        if ElectronicTrainTicketFull:
            return {
                "发票号码": f"{ElectronicTrainTicketFull['ElectronicTicketNum']}",
                "开票日期": f"{ElectronicTrainTicketFull['Date']}",
                "合计金额": f"{ElectronicTrainTicketFull['Fare']}",
                "类型": f"电子发票(铁路电子客票)",
                "BuyerTaxID":f"{ElectronicTrainTicketFull['BuyerTaxID']}",
                "Buyer":f"{ElectronicTrainTicketFull['Buyer']}",
            }
        VatElectronicInvoiceFull = SingleInvoiceInfos['VatElectronicInvoiceFull']
        if VatElectronicInvoiceFull:    
            VatElectronicItems = VatElectronicInvoiceFull['VatElectronicItems'][0]
            return {
                 "发票号码": f"{VatElectronicInvoiceFull['Number']}",
                 "开票日期": f"{VatElectronicInvoiceFull['Date']}",
                 "合计金额": f"{VatElectronicInvoiceFull['Total']}",
                 "类型": f"{VatElectronicItems['Name']}",
                "BuyerTaxID":f"{VatElectronicInvoiceFull['BuyerTaxID']}",
                "Buyer":f"{VatElectronicInvoiceFull['Buyer']}",
            }
        return None


    def _get_file_content(self,file_path):
        """读取文件并转换为base64编码"""
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

import os
if __name__ == '__main__':
    ocr = TencentOCR()
    b = ocr.recognize_general_invoice(r"D:\Codes\myGithub\pythonFapiao\11\未标题-1.png")
    print(b)
    
    
    b = ocr.recognize_general_invoice(r"D:\Codes\myGithub\pythonFapiao\11\盛利来(成都)科技有限公司_1279-pdf.pdf")
    print(b)