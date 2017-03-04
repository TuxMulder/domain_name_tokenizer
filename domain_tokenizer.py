#encoding=utf-8
import string
import re
import unicodedata
import tldextract


def get_host(domain):
	return str(domain.split('.')[0]).replace('-', '')

def normailize_text(text):
	#text = unicode(text)
	#text = u"{}".format(text)
	text = unicodedata.normalize('NFD', text.decode('utf-8')).encode('ascii', 'ignore')
	text = text.replace('-', ' ')
	text = text.replace('\n', '')
	text = text.replace('\r', '')
	text = text.translate(None, string.punctuation)
	text = re.sub( '\s+', ' ', text ).strip()#replace all whitespace including tabs, with single space
	return text.lower()

def whitespace_offsets(text):
	return [m.start() for m in re.finditer(' ', text)]

def domain_text_offsets(text, domain):
	return [m.start() for m in re.finditer(domain, text)]

def replace_whitespace(text):
	return text.replace(' ', '')

def adjust_ws(ws_offsets):
	adjusted = []
	for x in range(0, len(ws_offsets)):
		adjusted.append(ws_offsets[x] - x)
	return adjusted

def tokenize_domain_name(domain, text):
	try:
		domain = get_host(domain)
		domain_length = len(domain)
		text = normailize_text(text)
		ws_offsets = whitespace_offsets(text)
		ws_offsets_adjusted = adjust_ws(ws_offsets)
		search_space = replace_whitespace(text)

		domain_offsets = domain_text_offsets(search_space, domain)
		

		if len(domain_offsets) == 0:
		
			return None
		
		candidates = []

		for offset in domain_offsets:
			start = len([i for i in ws_offsets_adjusted if i <= offset]) + offset
			end = len([i for i in ws_offsets_adjusted if i <= offset + domain_length]) + domain_length + offset
			candidates.append(text[start:end].strip())

		return max(candidates, key=len)

	except Exception, e:
		print e
		return None


if __name__ == '__main__':
	real_example = 'Enhance customer-facingdashboards.comyour own applic\n\rations\n with powerful analytics and customer-facing dashboards using our award-winning technology, extensive SDK and easy API access.'
	##real_example = "Quoi charlevoixecomobilite.com de plus charlevoix eco mobilite sympathique que de découvrir les beautés de Charlevoix au rythme lent de ses marées, sans efforts et en toute liberté ? En route vers une planète verte, Charlevoix Éco-Mobilité met « l’épaule à la roue » en offrant une expérience à la fois ludique, enrichissante et respectueuse. Ne reste qu’à poser le pied à l’étrier. Du littoral jusqu’aux frontières de l’arrière-pays, Charlevoix réserve son lot de surprises à qui sait ouvrir l’œil et tendre l’oreille. À vélo, en vélo-taxi ou en moto - en formule solo ou en version guidée -, on entre en contact avec le paysage, les gens et le terroir régional, découvrant ainsi tous les secrets d’une région riche et inspirante, au cœur de la Réserve mondiale de la Biosphère."
	##real_example = 'some more text Against All Grain | Against All Grain some more text' #where domain name appears next to each other
	#real_example = 'some text forexample.com for example some more text'# should return for example, not forexample
	#real_example = 'some text mitch eccles mitch eccles some more text mitch eccles mitch eccles'
	domain = 'customer-facingdashboards.com'

	print "{} - {}".format(domain, tokenize_domain_name(domain, real_example))

	#print adjust_ws([4, 9, 15, 22, 28, 35, 40, 45, 50, 56, 63, 69])

	#print normailize_text('cuStomer-facing')
	#print normailize_text("abc.,-';:def\"><|!@^*?/{}()ghi")
	#print replace_whitespace(normailize_text(example_text))

