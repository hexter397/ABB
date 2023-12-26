import json
a = []
with open('product_abb_china_25may2023.json' , 'r') as f:
    urls = json.load(f)

for url in urls:
    a.append({'product_link' : url})

with open('products_abb_china_25may2023.json' , 'w') as f:
    json.dump(a, f)