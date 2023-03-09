import re
from os import chdir
from tempfile import NamedTemporaryFile
import subprocess
import xml.etree.ElementTree as ET

import requests

from ALEPHBET import ALEPHBET


def get_file(link=''):
	while not link:
		link = input('put the link to xml file: ')
	headers = {'user-agent': 'mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/102.0.0.0 safari/537.36'}
	res = requests.get(link, headers=headers)
	if res.status_code != 200:
		raise Exception('Connection Error. status code:', res.status_code)
	return res.text

def creat_page(title, text):
	return {'title': title, 'text': text}

def change_format(root, book_name, by_sections=True):
	"""
	input: the book content on OYW xml format.
	output: list of pages to upload to wikisource, that any page is dict with two attributes - title and text.
	"""
	pages = []
	if by_sections:
		for chap in root:
			part = chap.attrib['n'].strip()
			text = '==' + part + '==\n' + ''.join(chap.itertext()).strip('\n')
			
			if part == '':
				title = book_name
			else:
				title = book_name + '/' + part
			page = creat_page(title, text)
			if text:
				pages.append(page)
		
	else:
		full_text = ''
		iterator = iter(range(1, 1000))
		for chap in root:
			part = chap.attrib['n'].strip()
			text = '==' + part + '==\n' + ''.join(chap.itertext()).strip('\n')
			full_text += text+'\n'
			
			if len(full_text) > 100000:
				page = creat_page(book_name+'/'+str(next(iterator)), full_text)
				pages.append(page)
				full_text = ''
		page = creat_page(book_name+'/'+str(next(iterator)), full_text)
		pages.append(page)
	return pages


def edit_spaces(text):
	while '\n ' in text:
		text = text.replace('\n ', '\n')
	while ' \n' in text:
		text = text.replace(' \n', '\n')
	
	while ' )' in text:
		text = text.replace(' )', ')')
	while '( ' in text:
		text = text.replace('( ', '(')
	while re.search('[^\s\(]\(', text):
		text = re.sub('([^\s\(])\(', r'\1 (',text)
	while re.search('\)[^\s\)]', text):
		text = re.sub('\)([^\s\)])', r') \1', text)
	
	while '׃' in text:
		text = text.replace('׃', ':')
	while ' :' in text:
		text = text.replace(' :', ':')
	while ' .' in text:
		text = text.replace(' .', '.')
	while ' ,' in text:
		text = text.replace(' ,', ',')
	while ' ;' in text:
		text = text.replace(' ;', ';')
	while '  ' in text:
		text = text.replace('  ', ' ')
	
	return text

def add_sources(text):
	def bavli(text):
		options = '''אפשרויות בבלי:
(ברכות ד', א')
(בבלי ברכות מ"ד, א׳)
(ברכות קמ״ד ע"ב)
(קדושין, דף קמד ע"א)
(ברכות ד' קמד, ע"א)
(ב"ק דף קמ"ד עמוד א)
(ברכות ק"ד עמוד א)
(ברכות ד.)
(ברכות, דף קמד:)
כנ"ל כשהסוגריים רק מהדף:
ברכות (ד', א')
ברכות (מ"ד, א׳)
ברכות (קמ״ד ע"ב)
קדושין (דף קמד ע"א)
ברכות (ד' קמד, ע"א)
ב"ק (דף קמ"ד עמוד א)
ברכות (ק"ד עמוד א)
ברכות (ד.)
ברכות (דף קמד:)'''
		masechtot = ["ברכות", "שבת", "עירובין", "פסחים", "ראש השנה", "יומא", "סוכה",
"ביצה", "תענית", "מגילה", "מועד קטן", "חגיגה", "יבמות", "כתובות", "נדרים",
"נזיר", "גיטין", "סוטה", "קידושין", "בבא קמא", "בבא מציעא", "בבא בתרא",
"סנהדרין", "מכות", "שבועות", "עבודה זרה", "הוריות", "זבחים", "מנחות",
"חולין", "בכורות", "ערכין", "תמורה", "כריתות", "מעילה", "תמיד", "נדה",
"ערובין", "קדושין", "נידה", 'ע"ז', 'עכו"ם', "סנהד'", "פסח'", 'ב"ק', 'ב"מ', 'ב"ב',
'מו"ק', 'ר"ה', "הורי'", "גטין", 'מ"ק']
		masech_reg = '(' + '|'.join(masechtot) + ')'
		
		daf_regex = '\((?:בבלי,? )?'+masech_reg+',?(?: ד[\'׳]| דף|) ((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])),?'
		text = re.sub(daf_regex+' (?:עמוד |עמ[׳\'] |ע[״"]|)([אב])[\'׳]?\)', '{{הפניה-גמ|\\1|\\3\\4\\5\\6|\\7|מסכת=כן}}', text)
		text = re.sub(daf_regex+'\.\)', '{{הפניה-גמ|\\1|\\3\\4\\5\\6|א|מסכת=כן}}', text)
		text = re.sub(daf_regex+'\:\)', '{{הפניה-גמ|\\1|\\3\\4\\5\\6|ב|מסכת=כן}}', text)
		
		daf_regex = masech_reg+' \((?:ד[\'׳] |דף |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])),?'
		text = re.sub(daf_regex+' (?:עמוד |עמ[׳\'] |ע[״"]|)([אב])[\'׳]?\)', '\\1 {{הפניה-גמ|\\1|\\3\\4\\5\\6|\\7}}', text)
		text = re.sub(daf_regex+'\.\)', '\\1 {{הפניה-גמ|\\1|\\3\\4\\5\\6|א}}', text)
		text = re.sub(daf_regex+'\:\)', '\\1 {{הפניה-גמ|\\1|\\3\\4\\5\\6|ב}}', text)
		return text

	def bible(text):
		options = '''אפשרויות פסוקים:
(קהלת ג ד)
(משלי ד', א')
(משלי מ"ד, א׳)
(משלי קמ״ד ע"ב)
(דברים, פרק קמד ע"א)
(משלי פ' קמד, ע"א)
(תהלים פקמ"ד פסוק א)
(משלי ק"ד פס' א)
(משלי ל"א, כ"ג-כ״ד)
(משלי לא כג - כד)
(משלי ד)
(משלי, פרק קמד)
(בראשית כ״ג:מ״ד)
כנ"ל כשהסוגריים רק מהפרק:
משלי (ד', א')
משלי (מ"ד, א׳)
משלי (קמ״ד ע"ב)
יהושע (פרק קמד ע"א)
משלי (פ' קמד, ע"א)
תהלים (פרק קמ"ד פסוק א)
משלי (ק"ד פס' א)
משלי (ד)
משלי (פרק קמד)'''
		books = ["בראשית", "שמות", "ויקרא", "במדבר", "דברים",
"יהושע", "שופטים", "שמואל א", "שמואל ב", "מלכים א", "מלכים ב",
"ישעיהו", "ירמיהו", "יחזקאל", "הושע", "יואל", "עמוס", "עובדיה", "יונה",
"מיכה", "נחום", "חבקוק", "צפניה", "חגי", "זכריה", "מלאכי",
"תהלים", "משלי", "איוב", "שיר השירים", "רות", "איכה", "קהלת", "אסתר",
"דניאל", "עזרא", "נחמיה", "דברי הימים א", "דברי הימים ב",
"ישעיה", "ירמיה", "תהילים", "קוהלת", 'ש"א', 'ש"ב', 'מ"א', 'מ"ב', 'דה"א', 'דה"ב', 'שה"ש',
"שמואל א'", "שמואל ב'", "מלכים א'", "מלכים ב'", "דברי הימים א'", "דברי הימים ב'"
"ישעי'", "ירמי'", "ד\"ה א'", "ד\"ה ב'", "ד\"ה א", "ד\"ה ב"]
		books_reg = '(' + '|'.join(books) + ')'
		#book inside ()
		perek_regex = '\('+books_reg+',? (?:פ[\'׳] |פרק |פ[״"]?|)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])),?'
		text = re.sub(perek_regex+'\)', '{{מ"מ|\\1|\\3\\4\\5\\6}}', text)
		text = re.sub(perek_regex+'[ :](?:פס[\'׳] |פסוק |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט]))\)', '{{מ"מ|\\1|\\3\\4\\5\\6|\\8\\9\\10\\11|ק={{שם הדף}}}}', text)
		text = re.sub(perek_regex+'[ :](?:פס[\'׳] |פסוקים |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])) ?- ?((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט]))\)', '{{הפניה לפסוקים|\\1|\\3\\4\\5\\6|\\8\\9\\10\\11|\\13\\14\\15\\16}}', text)
		
		#book outside ()
		perek_regex = books_reg+' \((?:פ[\'׳] |פרק |פ[״"]?|)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])),?'
		text = re.sub(perek_regex+'\)', '\\1 {{מ"מ|\\1|\\3\\4\\5\\6}}', text)
		text = re.sub(perek_regex+'[: ](?:פס[\'׳] |פסוק |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט]))\)', '\\1 {{מ"מ|\\1|\\3\\4\\5\\6|\\8\\9\\10\\11|ק={{שם הדף}}}}', text)
		text = re.sub(perek_regex+'[: ](?:פס[\'׳] |פסוקים |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])) ?- ?((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט]))\)', '\\1 {{הפניה לפסוקים|\\1|\\3\\4\\5\\6|\\8\\9\\10\\11|\\13\\14\\15\\16}}', text)
		return text
	
	def midrash(text):
		#TODO
		'''
מדרש:
ויק"ר
ילקו"ש
ב"ר
מכילתא
במ"ר
תנחומא

פ"א
פ' א'
'''
		text = re.sub('', '', text)
		return text
	
	text = bavli(text)
	text = bible(text)
	text = midrash(text)
	return text
	

def edit_html_to_wiki(text):
	if '<br>' in text:
		text = text.replace('<br>', '\n\n')
	if '<b>' in text:
		text = text.replace('<b>', "'''")
		text = text.replace('</b>', "'''")
	return text

def edit_page(page_text):
	new_text = page_text
	new_text = edit_spaces(new_text)
	new_text = add_sources(new_text)
	new_text = edit_html_to_wiki(new_text)
	return new_text

def edit_pages(pages):
	new_pages = []
	for page in pages:
		page['text'] = edit_page(page['text'])
		new_pages.append(page)
	return new_pages

def edit_titles(pages):
	print('titles edit:')
	titles = [page['title'] for page in pages]
	titles_str = '|'.join(titles)
	while re.search('[a-zA-Z]', titles_str):
		eng_titles = set(re.findall('[^א-ת\|]+', titles_str))
		for title in eng_titles:
			print(title)
			right_title = input('which title you want instead? ')
			for page in pages:
				page['title'] = page['title'].replace(title, right_title)
		titles = [page['title'] for page in pages]
		titles_str = '|'.join(titles)
	
	print('titles:\n', titles)
	input_to_edit = input('Do you want to edit titles? (y/n) ')
	if input_to_edit in ['y', 'Y']:
		to_edit = True
	else:
		to_edit = False
	while to_edit:
		current_str = input('you have to insert current pattern to replace in the titles: (to stop press enter twice)\ncurrent: ')
		required_str = input('required: ')
		if not (current_str or required_str):
			to_edit = False
			break
		for page in pages:
			page['title'] = page['title'].replace(current_str, required_str)
	print('edit finished!')
	return pages

def add_navigation(pages):
	#TODO
	again = True
	while again:
		ask_user = input('do you want to add navigation temp? (y/n) ')
		if ask_user in ['y', 'Y', 'כן']:
			print('בחר תבנית לעבוד איתה.\n1. סרגל ניווט (לא נתמך)\n2. ניווט ספר (לא נתמך)\n3. תבנית קבועה')
			choose_temp = input('מספר: ')
			if choose_temp == '3':
				temp = input('enter temp name: ')
				for page in pages:
					page['text'] = '{{'+temp+'}}\n\n'+page['text']
				again = False
		elif ask_user in ['n', 'N', 'לא']:
			again = False
		else:
			pass
	return pages

def upload_pwb(pages, pwb_dir):
	ask = input('do you want to upload this book to wikisource? (y/n) ')
	if ask in ['n', 'N', 'לא']:
		print(pages)
		return
	
	temp_file = NamedTemporaryFile(mode='w+', suffix='.txt')
	for page in pages:
		file_format = "{{-start-}}\n'''" + page['title'] + "'''\n" + page['text'] + "\n{{-stop-}}\n"
		temp_file.write(file_format)
	
	chdir(pwb_dir)
	subprocess.run(['python', 'pwb.py', 'pagefromfile', '-file:'+temp_file.name, '-notitle', '-autosummary', '-showdiff'])
	temp_file.close()
	
	
def main():
	file = get_file(link='http://mobile.tora.ws/xml/15301.xml')
	
	root = ET.fromstring(file) #./book/chap/p/d
	book_name = root.attrib['n'].replace('ספר', '').strip()
	pages = change_format(root, book_name, by_sections=False)
	#print(pages[:2])
	
	pages = edit_pages(pages)
	pages = edit_titles(pages)
	pages = add_navigation(pages)
	upload_pwb(pages, pwb_dir='/storage/emulated/0/python/pywikibot')

if __name__ == '__main__':
	main()