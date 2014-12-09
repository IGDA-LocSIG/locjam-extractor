import sys
import requests
import json 

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup

def export(url, langs):
	old_t = requests.get(url).text
	soup = BeautifulSoup(old_t)
	store = soup.find(id="storeArea")
	rows = []
	row = 0
	for twee in store.find_all("div"):
		if not twee.string.startswith("data:") and not "background-size" in twee.string and not "\"requires jQuery\"" in twee.string and not "(function (" in twee.string:
			#t = t.replace(twee.string, "twine_trans(%s);" % str(row))
			tw = twee.string
			twee["data-trans"] = "twine_trans(%s);" % str(row)
			#twee.string = "twine_trans(%s);" % str(row)
			rows.append(tw)
			row += 1
	t = soup.prettify();


	j_script = open("jquery.min.js").read()
	t_script = open("translate.js").read()
	t = t.replace(
		"</title>", 
		"</title>\n<script title=\"jquery\">\n\n"+j_script+"\n\n</script>\n<script title=\"translation\">\n\n//magic\n\nvar langs="+json.dumps(langs)+";\n\n"+t_script+"\n\n</script>"
	)

	file_name = url.split("/")[-1]	
	with open(file_name, "wb") as h: 
		h.write(t)
	origin = file_name.split(".")[:-1]
	origin.append("original")
	origin.append(file_name.split(".")[-1])
	with open(".".join(origin), "wb") as h: 
		h.write(old_t)
	for lang in langs:
		with open(lang+".txt", "wb") as h:
			h.write("\n".join(rows))

	return ".".join(origin), file_name

import zipfile
import uuid

def compress(origin, file, langs):

	mongooses = ["mongoose-lua-sqlite-ssl-static-x86_64-5.2", "Mongoose-free-5.5.dmg", "mongoose-free-5.5.exe"]
	zname = str(uuid.uuid4())+".zip"
	with zipfile.ZipFile(zname, 'w', zipfile.ZIP_DEFLATED) as myzip:
		myzip.write(origin)
		myzip.write(file)
		for lang in langs:
			myzip.write(lang+".txt")
		for mongoose in mongooses:
			myzip.write(mongoose)
	return zname
	
if __name__ == "__main__":
	origin, file_name = export (sys.argv[1], sys.argv[2:])
	print compress(origin, file_name, sys.argv[2:])
