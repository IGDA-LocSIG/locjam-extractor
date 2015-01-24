import sys
import requests
import json 

import argparse

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup

def export(url, langs, splitline=None):
	old_t = requests.get(url).text
	soup = BeautifulSoup(old_t)
	if splitline:
		splitline = splitline[0]
	store = soup.find(id="storeArea")
	rows = []
	split_stuff = []
	split_row = 0
	row = 0
	for twee in store.find_all("div"):
		if not twee.string.startswith("data:") and not "background-size" in twee.string and not "\"requires jQuery\"" in twee.string and not "(function (" in twee.string and not "#storyTitle" in twee.string:
			#t = t.replace(twee.string, "twine_trans(%s);" % str(row))
			tw = twee.string
			if splitline in tw:
				stw = tw.split(splitline)
				try:
					i = split_stuff.index(stw[1])
					twee["data-split"] = i
				except:
					split_stuff.append(stw[1])
					twee["data-split"] = split_row
					split_row += 1
				rows.append(stw[0])
			else:
				rows.append(tw)
			twee["data-trans"] = "twine_trans(%s);" % str(row)

			row += 1
	t = soup.prettify();

	j_script = open("jquery.min.js").read()
	t_script = open("translate.js").read()
	t = t.replace(
		"</title>", 
		"</title>\n<script title=\"jquery\">\n\n"+j_script+"\n\n</script>\n<script title=\"translation\">\n\n//magic\n\nvar langs="+json.dumps(langs)+"; var splitline="+str(row)+";\n\n"+t_script+"\n\n</script>"
	)

	file_name = url.split("/")[-1]	
	with open(file_name, "wb") as h: 
		h.write(t)
	origin = file_name.split(".")[:-1]
	origin.append("original")
	origin.append(file_name.split(".")[-1])
	with open(".".join(origin), "wb") as h: 
		h.write(old_t)

	translateable = "\n".join(rows)
	if splitline:
		translateable += "\n" + splitline + "\n" + "\n".join(split_stuff)
	for lang in langs:
		with open(lang+".txt", "wb") as h:
			h.write(translateable)

	return ".".join(origin), file_name

import zipfile
import uuid

def compress(origin, file, langs):
	mongooses = ["mongoose-linux", "mongoose-osx.dmg", "mongoose-win.exe"]
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
	parser = argparse.ArgumentParser(description='Twine Translation Extractor')
	parser.add_argument("url", metavar="URL", nargs=1, action="store", help="The url of the twine game to translate")
	parser.add_argument("langs", metavar="LANG", nargs="+", action='store', help="The target languages of the translation")
	
	parser.add_argument("--fromlang", metavar="LANG", nargs="?", default="eng", action='store', help="The starting language of the translation")

	parser.add_argument("--splitline", metavar="SYMBOLS", nargs=1, action="store", help="if a certain part of the line is repeated, you might want to have it in a separate part of the translation file. ")

	args = parser.parse_args()
	langs_list = [args.fromlang]
	for lang in args.langs:
		langs_list.append(lang)
	print args.splitline
	origin, file_name = export (args.url[0], langs_list, args.splitline)
	print compress(origin, file_name, args.langs)

	
	