#
#	Author : Ashwin
#	
#	A simple product matcher
#


import sys
import json

# Rabin Karp for string matching
def Rabin_Karp_Matcher(text, pattern, d, q):
    n = len(text)
    m = len(pattern)
    h = pow(d,m-1)%q
    if n < m:
    	return []
    p = 0
    t = 0
    result = []
    for i in range(m): # preprocessing
        p = (d*p+ord(pattern[i]))%q
        t = (d*t+ord(text[i]))%q
    for s in range(n-m+1):
        if p == t: # check character by character
            match = True
            for i in range(m):
                if pattern[i] != text[s+i]:
                    match = False
                    break
            if match:
                result = result + [s]
        if s < n-m:
            t = (t - h*ord(text[s]))%q # remove letter s
            t = (t*d + ord(text[s+m]))%q # add letter s+m
            t = (t + q)%q
    return result
    
if __name__  == "__main__":    
	
	prod_f = open(sys.argv[1])		# products file
	list_f = open(sys.argv[2])		# listing file
	res_file = open(sys.argv[3], 'w')	# result is written to this file
	
	result = {}
	prod_dict = {}
	
	# Get a { manufacturer: array[products] } dictionary
	for line in prod_f:
		line = line.strip()
		pr = json.loads(line)
		try:
			prod_dict[pr["manufacturer"]].append(pr);
		except KeyError:
			l = []
			l.append(pr)
			prod_dict[pr["manufacturer"]] = l
	
	# list of all manufacturers 
	manu_list = list(prod_dict.keys())
		
	for line in list_f:
		line = line.strip()
		item = json.loads(line)
		# Find the manufacturer of the item by looking at all the manufacturers
		for m in manu_list:
			# Remove spaces and convert to lowercase before pattern matching
			match_list = Rabin_Karp_Matcher(item['manufacturer'].replace(" ", "").lower(), m.replace(" ", "").lower(), 301, 1000000007)
			if len(match_list) != 0:
				ma = 0
				p_name = ""
				# Find the matching item among all the items manufactured by that manufacturer
				for it in prod_dict[m]:
					# Remove spaces and convert to lowercase before pattern matching
					m_list = Rabin_Karp_Matcher(item['title'].replace(" ", "").lower(), it['model'].replace(" ", "").lower(), 301, 1000000007)
					if len(m_list) != 0:
						# Find the model name with maximum matching length
						if len(it['model'].replace(" ", "")) > ma:
							ma = len(it['model'].replace(" ", ""))
					 		p_name = it['product_name']
				# If there is a product, add the item to the listing of that product	 		
				if p_name != "":		
					try:
						result[p_name].append(item)
					except KeyError:
						l = []
						l.append(item)
						result[p_name] = l
	
	# convert the result to the required {'listing': array[item], 'product_name': string} format	
	result_format = ({'product_name':k, 'listings':v} for (k, v) in result.items())
	# write result to file
	for item in result_format:
		res_file.write(str(json.dumps(item))+'\n')
	
	res_file.close()
	prod_f.close()
	list_f.close()	
