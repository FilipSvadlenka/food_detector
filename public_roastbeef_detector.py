from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import smtplib
from datetime import date

day = date.today()
today = day.strftime("%d/%m/%Y")
# Python program for KMP Algorithm
def KMPSearch(pat, txt):
	M = len(pat)
	N = len(txt)
	lps = [0]*M
	j = 0 # index for pat[]
	computeLPSArray(pat, M, lps)

	i = 0 # index for txt[]
	while i < N:
		if pat[j] == txt[i]:
			i += 1
			j += 1

		if j == M:
			return i-j
			j = lps[j-1]

		elif i < N and pat[j] != txt[i]:

			if j != 0:
				j = lps[j-1]
			else:
				i += 1

def computeLPSArray(pat, M, lps):
	len = 0
	lps[0]
	i = 1
	while i < M:
		if pat[i]== pat[len]:
			len += 1
			lps[i] = len
			i += 1
		else:

			if len != 0:
				len = lps[len-1]
			else:
				lps[i] = 0
				i += 1

urls = ["https://agata.suz.cvut.cz/jidelnicky/indexTyden.php?clPodsystem=2&lang=cs", "https://agata.suz.cvut.cz/jidelnicky/indexTyden.php?clPodsystem=3&lang=cs"]
menzy = ["Technická: ", "Studentská: "]
roastbeef = False
menza_str = ""

# vyber tuto druhou definici proměnné pattern, aby jsi mohl ovládát název jídla na inputu
# pattern = input(str("Co za chálky tě zajímá? Zadej přesný stringze stránek menzy:"))

"Zde zadej string jídla, které hledáš"
pattern = "Anglický roastbeef, hranolky, tatarská omáčka"

"A zde svůj mail, či seznam mailů. Svůj vždy dej jako první"
my_mail = ["jan.novak@tvojemama.cz"]

"Host mail, ze kterého posíláš maily. Nedoporučuji používat svůj vlastní. Založit nový je za free!"
host_mail = ""
host_mail_heslo = ""

for m, url in enumerate(urls):
	page = urlopen(url)
	html_bytes = page.read()
	html = html_bytes.decode("utf-8")
	match_results = re.search(pattern, html, re.IGNORECASE)

	if match_results:
		title = match_results.group()
		title = re.sub("<.*?>", "", title)
		roastbeefindex = KMPSearch(pattern, html)
		reversed_html = html[roastbeefindex::-1]
		dateindex = KMPSearch("202", reversed_html)
		date = reversed_html[dateindex -1:dateindex + 10]
		date = date[::-1]
		if date[0] == '>':
			date = date[1:]
		date = date.split('.')
		for i in range(2):
			if len(date[i].strip()) == 1:
				date[i] = '0' + date[i].strip()
			else:
				date[i] = date[i].strip()
		dateformated = date[0] + '/' + date[1] + '/' + date[2].strip()

		if dateformated == today:
			roastbeef = True
			menza_str += menzy[m]

if roastbeef:
	print(today)
	print("V", menza_str, "je dnes", pattern)
	for dest in my_mail:
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.starttls()
		s.login(host_mail, host_mail_heslo)
		message = "Srdecne ti oznamujeme, ze dnes je tva oblibena pochutina", pattern," je dnes v", menza_str, \
			". Mnam do pici a dobrou chut!"
		s.sendmail(host_mail, dest, message)
		s.quit()
else:
	print("Nope, dnes", pattern, "neni.")
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(host_mail, host_mail_heslo)
	message = "Dneska neni roastbeef"
	s.sendmail(host_mail, my_mail[0], message)
	s.quit()