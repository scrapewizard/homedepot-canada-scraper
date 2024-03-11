import requests
import json
import csv
import os


def add_product(filename,product_details):

	if not os.path.exists(filename):

		columns=[
			"sku",
			"category name",
			"model_number",
			"name",
			"currency",
			"original price",
			"original stock",
			"max_order_quantity",
			"total_reviews",
			"average_rating",
			"image",
			"url",
			]

		file=open(filename,"w",encoding="utf-8",newline="")
		writer=csv.writer(file)
		writer.writerow(columns)
		writer.writerow(product_details)
		file.close()

	else:

		file=open(filename,"a",encoding="utf-8",newline="")
		writer=csv.writer(file)
		writer.writerow(product_details)
		file.close()




def unescape(str):

	unescapedText = {
		'&a;': '&',
		'&q;': '"',
		'&s;': '\'',
		'&l;': '<',
		'&g;': '>',
	}
	for key, value in unescapedText.items():
		str = str.replace(key, value)
	return str
	
def get_category_id(category_url):

	response = requests.get(category_url,headers=headers)

	html=response.text
	
	raw_json=html.split('<script id="hdca-state" type="application/json">')[1].split('</script>')[0]
	
	unescaped_raw_json=unescape(raw_json)
	
	category_id=unescaped_raw_json.split('"categoryId":"')[1].split('",')[0].strip()
	
	category_name=json.loads(html.split('<script type="application/ld+json">')[1].split('</script>')[0])["name"]
	
	return category_id,category_name
	
def get_products(category_id,category_name,output_file):

	ids=[]

	page=1
	
	
	while True:
		params={
			
			"category":category_id,
			"page":str(page),
			"pageSize":"40",
			"lang":"en",
			"store":STORE_ID,
		
		}
		
		
		response=requests.get("https://www.homedepot.ca/api/search/v1/search",headers=headers,params=params)
		
		try:
			new_products=response.json()["products"]
		except:
			return 
		
			
		for product in new_products:
		
			
			sku=product["code"]
			
			url="https://www.homedepot.ca"+product["url"]
			
			model_number=product["modelNumber"]
			
			
			try:
				price=product["pricing"]["displayPrice"]["value"]
			except:
				price=None
				
				
			try:
				currency=product["pricing"]["displayPrice"]["currencyIso"]
			except:
				currency=None
				
			try:
				stock=product["storeStock"]["stockLevel"]
			except:
				stock=None
				
			try:
				max_order_quantity=product["maxOrderQuantity"]
			except:
				max_order_quantity=None
			
			
			try:
				total_reviews=product["productRating"]["totalReviews"]
			except:
				total_reviews=None
				
			try:
				average_rating=product["productRating"]["averageRating"]
			except:
				average_rating=None
				
				
			name=product["name"]
			
			image=product["imageUrl"]
			

		
			product_details=[
			
				sku,
				category_name,
				model_number,
				name,
				currency,
				price,
				stock,
				max_order_quantity,
				total_reviews,
				average_rating,
				image,
				url,
			
			
			]
			
			
			
			if sku not in ids:
				print(product_details)
				add_product(output_file,product_details)
				

			
			
		page+=1
	

	
	

if __name__=='__main__':


	global headers,STORE_ID

	STORE_ID="7249"
	
	headers = {
		'authority': 'www.homedepot.ca',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-language': 'en-US,en;q=0.9,ar-TN;q=0.8,ar;q=0.7',
		'cache-control': 'no-cache',
		'pragma': 'no-cache',
		'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	}
	
	search_url=input("\n Please provide a category URL: ")

	output_file=input("\n Save as? (eg data.csv): ")
		
	category_id,category_name=get_category_id(search_url)

	print(" Category ID: "+category_id)

	get_products(category_id,category_name,output_file)
