import json 


with open('quotes.json', 'r') as file:
  data = json.load(file)

for book in data:
  print(book['title'])
  print("------------------")
  for index, quote in enumerate(book['quotes']):
    print(index, quote)
  print("-----------------------------------------\n")