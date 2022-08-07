import json
import re
from os.path import isfile

from ALEPHBET import ALEPHBET


def get_path(path = ''):
	while not isfile(path):
		if path:
			print('wrong path!')
		path = input('put the path to json file: ')
	return path

def join_paragraphs(lst):
	return '\n\n'.join(lst)

def creat_page(title, text):
	return {'title': title, 'text': text}

def join_to_list(page, lst):
	lst.append(page)

def change_format(content, book_name):
	"""
	input: the book content in sefaria json format.
	output: list of pages to upload to wikisource, that any page is dict with two attributes - title and text.
	exception: when the json have more than two levels of content.
	"""
	pages = []
	counter = 0 #del
	for part in content.keys():
		if len(content[part]) and not all(isinstance(x, str) for x in content[part]) and not (isinstance(content[part][0], list) and all(isinstance(x, str) for x in content[part][0])):
			raise TypeError(f'json["text"]["{part}"][0] is not str and not list of strs')
		
		if part == '':
			title = book_name
		else:
			title = book_name + '/' + part
		
		if all(isinstance(x, str) for x in content[part]):
			text = join_paragraphs(content[part])
			page = creat_page(title, text)
			if text:
				join_to_list(page, pages)
			continue
		
		for i,perek in enumerate(content[part]):
			text = join_paragraphs(content[part][i])
			page = creat_page(title + '/' + ALEPHBET[i+1], text)
			if text:
				join_to_list(page, pages)
	
		counter += 1
		if counter >= 5:
			break #del
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
	while '  ' in text:
		text = text.replace('  ', ' ')
	while ' .' in text:
		text = text.replace(' .', '.')
	while ' ,' in text:
		text = text.replace(' ,', ',')
	while ' ;' in text:
		text = text.replace(' ;', ';')
	
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
		perek_regex = '\('+books_reg+',? (?:פ[\'׳] |פרק |פ[״"]?|)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])),?'
		text = re.sub(perek_regex+'\)', '{{מ"מ|\\1|\\3\\4\\5\\6|ק={{שם הדף}}}}', text)
		text = re.sub(perek_regex+'[ :](?:פס[\'׳] |פסוק |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט]))\)', '{{מ"מ|\\1|\\3\\4\\5\\6|\\8\\9\\10\\11|ק={{שם הדף}}}}', text)
		text = re.sub(perek_regex+'[ :](?:פס[\'׳] |פסוקים |)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])) ?- ?((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט]))\)', '{{הפניה לפסוקים|\\1|\\3\\4\\5\\6|\\8\\9\\10\\11|\\13\\14\\15\\16}}', text)

		perek_regex = books_reg+' \((?:פ[\'׳] |פרק |פ[״"]?|)((ק?)[״"]?([א-צ])[׳\']?|(ק?[ט-צ])[״"]?([א-ט])),?'
		text = re.sub(perek_regex+'\)', '\\1 {{מ"מ|\\1|\\3\\4\\5\\6|ק={{שם הדף}}}}', text)
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
	
	
def edit_footnotes(text):
	if '<sup>' in text and '<i class="footnote">' in text:
		text = text.replace('<sup>', ' {{הערה|')
		text = text.replace('</sup>', '')
		text = text.replace('<i class="footnote">', '\'\'\'הערת המדפיס:\'\'\' ')
		text = text.replace('</i>', '}}')
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
	new_text = edit_footnotes(new_text)
	new_text = edit_html_to_wiki(new_text)
	return new_text

def edit_pages(pages):
	new_pages = []
	for page in pages:
		page['text'] = edit_page(page['text'])
		new_pages.append(page)
	return new_pages

def edit_titles(pages, schema={}):
	print('titles edit:')
	if schema:
		for title in schema['nodes']:
			for page in pages:
				page['title'] = page['title'].replace(title['enTitle'], title['heTitle'])
		
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
	input_to_edit = input('Do you want to edit (also) hebrew titles? (y/n) ')
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
		
	import tempfile
	import subprocess
	from os import chdir
	
	temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.txt')
	for page in pages:
		file_format = "{{-start-}}\n'''" + page['title'] + "'''\n" + page['text'] + "\n{{-stop-}}\n"
		temp_file.write(file_format)
	
	chdir(pwb_dir)
	subprocess.run(['python', 'pwb.py', 'pagefromfile', '-file:'+temp_file.name, '-notitle', '-autosummary', '-showdiff'])
	
	temp_file.close()
	
	
def main():
	#path = get_path('/storage/emulated/0/download/Netivot Olam - he - OYW.json')
	path = get_path('/storage/emulated/0/download/Gevurot Hashem - he - OYW.json')
	
	with open(path, "r") as read_file:
		data = json.load(read_file)
	
	book_name = data['schema']['heTitle']
	pages = change_format(data['text'], book_name)
	pages = edit_pages(pages)
	pages = edit_titles(pages, data['schema'])
	pages = add_navigation(pages)
	upload_pwb(pages, pwb_dir='/storage/emulated/0/python/pywikibot')

if __name__ == '__main__':
	main()