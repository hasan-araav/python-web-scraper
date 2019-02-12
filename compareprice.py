import requests
from bs4 import BeautifulSoup
import lxml
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import flask_excel as excel

app = Flask(__name__)
api = Api(app)

myWebsiteUrl = ['https://www.mobile-mart.com.au/product/iphone-x-battery/',
					'https://www.mobile-mart.com.au/product/iphone-x-antenna-flex/',
					'https://www.mobile-mart.com.au/product/iphone-x-vibrator/',
					'https://www.mobile-mart.com.au/product/iphone-x-loud-speaker/',
					'https://www.mobile-mart.com.au/product/lcd-assembly-with-force-touch-panel-for-iphone-x-premium-quality/'
					]

compWebsitUrl = ['https://www.easyphix.com.au/battery-for-iphone-x',
					'https://www.easyphix.com.au/loud-speaker-for-iphone-x',
					'https://www.easyphix.com.au/vibrator-for-iphone-x',
					'https://www.easyphix.com.au/loud-speaker-for-iphone-x~40963',
					'https://www.easyphix.com.au/lcd-and-digitizer-touch-screen-assembly-for-iphone~44599'
					]
data = []

def getPageContent(url):
	headers = {'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}
	result = requests.get(url, headers = headers)
	src = result.content
	return BeautifulSoup(src, "lxml")

def getContent():
	for idx,url in enumerate(myWebsiteUrl):
		myPageContent = getPageContent(url)
		compPageContent = getPageContent(compWebsitUrl[idx])

		datas = [
			myPageContent.select('.sku')[0].get_text(),
			myPageContent.select('h2.product_title.entry-title.show-product-nav')[0].get_text(),
			myPageContent.select('span.woocommerce-Price-amount.amount')[0].get_text(),
			compPageContent.select('#specifications > table > tbody > tr:nth-child(1) > td:nth-child(2)')[0].get_text(),
			compPageContent.select('.page-header > h1')[0].get_text(),
			compPageContent.select('.productprice')[0].get_text()
		]
		data.append(datas)

class Data(Resource):
	def get(self):
		getContent()
		return jsonify(data)

class Download(Resource):
	def get(self):
		return excel.make_response_from_array(data, "csv",file_name="export_data")

api.add_resource(Data, '/')
api.add_resource(Download, '/download')

if __name__ == '__main__':
	excel.init_excel(app)
	app.run()

# dfd