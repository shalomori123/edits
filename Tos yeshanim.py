import re

path = '/sdcard/MyAppSharer/' + input('enter file name: ')
from os.path import isfile
while not isfile(path):
	print('wrong path')
	path = '/sdcard/MyAppSharer/' + input('enter file name: ')
masechet = input('מסכת: ')
parshan = 'תוספות ישנים'
if not parshan:
	parshan = input('לא ציינת פרשן. כתוב את שמו: ')

ALEPHBET = ('', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'יא', 'יב', 'יג', 'יד', 'טו', 'טז', 'יז', 'יח', 'יט', 'כ', 'כא', 'כב', 'כג', 'כד', 'כה', 'כו', 'כז', 'כח', 'כט', 'ל', 'לא', 'לב', 'לג', 'לד', 'לה', 'לו', 'לז', 'לח', 'לט', 'מ', 'מא', 'מב', 'מג', 'מד', 'מה', 'מו', 'מז', 'מח', 'מט', 'נ', 'נא', 'נב', 'נג', 'נד', 'נה', 'נו', 'נז', 'נח', 'נט', 'ס', 'סא', 'סב', 'סג', 'סד', 'סה', 'סו', 'סז', 'סח', 'סט', 'ע', 'עא', 'עב', 'עג', 'עד', 'עה', 'עו', 'עז', 'עח', 'עט', 'פ', 'פא', 'פב', 'פג', 'פד', 'פה', 'פו', 'פז', 'פח', 'פט', 'צ', 'צא', 'צב', 'צג', 'צד', 'צה', 'צו', 'צז', 'צח', 'צט', 'ק', 'קא', 'קב', 'קג', 'קד', 'קה', 'קו', 'קז', 'קח', 'קט', 'קי', 'קיא', 'קיב', 'קיג', 'קיד', 'קטו', 'קטז', 'קיז', 'קיח', 'קיט', 'קכ', 'קכא', 'קכב', 'קכג', 'קכד', 'קכה', 'קכו', 'קכז', 'קכח', 'קכט', 'קל', 'קלא', 'קלב', 'קלג', 'קלד', 'קלה', 'קלו', 'קלז', 'קלח', 'קלט', 'קמ', 'קמא', 'קמב', 'קמג', 'קמד', 'קמה', 'קמו', 'קמז', 'קמח', 'קמט', 'קנ', 'קנא', 'קנב', 'קנג', 'קנד', 'קנה', 'קנו', 'קנז', 'קנח', 'קנט', 'קס', 'קסא', 'קסב', 'קסג', 'קסד', 'קסה', 'קסו', 'קסז', 'קסח', 'קסט', 'קע', 'קעא', 'קעב', 'קעג', 'קעד', 'קעה', 'קעו', 'קעז', 'קעח', 'קעט', 'קפ', 'קפא', 'קפב', 'קפג', 'קפד', 'קפה', 'קפו', 'קפז', 'קפח', 'קפט', 'קצ', 'קצא', 'קצב', 'קצג', 'קצד', 'קצה', 'קצו', 'קצז', 'קצח', 'קצט')

file = open(path, 'r')
lines = file.readlines()
file.close()
for index, line in enumerate(lines):
	print(index)
	if 'Daf' in line:
		daf = line.split(' ')[1]
		if daf[1].isnumeric():
			if not daf[2].isnumeric():
				num_daf = daf[:2]
				page = daf[2]
			elif daf[2].isnumeric():
				num_daf = daf[:3]
				page = daf[3]
		else:
			num_daf = daf[0]
			page = daf[1]
		if page == 'a' and num_daf != '1':
			prev_page = ALEPHBET[int(num_daf) - 1] + ' ב'
			current = ALEPHBET[int(num_daf)] + ' א'
			page_letter = 'א'
		elif page == 'a' and num_daf == '1':
			prev_page = ''
			current = ALEPHBET[int(num_daf)] + ' א'
			page_letter = 'א'
		elif page == 'b':
			prev_page = ALEPHBET[int(num_daf)] + ' א'
			current = ALEPHBET[int(num_daf)] + ' ב'
			page_letter = 'ב'
		daf_letter = ALEPHBET[int(num_daf)]
		lines[index] = '<קטע סוף=%s/>\n===[[%s %s %s|דף %s עמוד %s]]===\n<קטע התחלה=%s/>' % (prev_page, masechet, daf_letter, page_letter, daf_letter, page_letter, current)
		
	if 'Line' in line:
		lines[index] = ''
	
	while '<sup>' in lines[index] and '<i' in lines[index]:
		lines[index] = lines[index].replace('<sup>', ' {{קטן|')
		lines[index] = lines[index].replace('</sup>', '')
		lines[index] = lines[index].replace('<i class="footnote">', '\'\'\'הערת המדפיס:\'\'\' ')
		lines[index] = lines[index].replace('</i>', '}}')
	
	while re.search('\(([א-ת\s]*)[׳״]([א-ת]?):([א-ת]+)[׳״]([א-ת]?)([\)-])', lines[index]):
		lines[index] = re.sub('\(([א-ת\s]*)[׳״]([א-ת]?):([א-ת]+)[׳״]([א-ת]?)([\)-])', r'([[\1\2 \3\4]]\5', lines[index])
	
	while '\n ' in lines[index]:
		lines[index] = lines[index].replace('\n ', '\n')
	while ' \n' in lines[index]:
		lines[index] = lines[index].replace(' \n', '\n')
	while lines[index].startswith(' '):
		lines[index] = lines[index][1:]
	while lines[index].endswith(' '):
		lines[index] = lines[index][:-1]
	
	if '<br>' in lines[index]:
		lines[index] = lines[index].replace('<br>', '\n\n')
	if '<b>' in line:
		lines[index] = lines[index].replace('<b>', "'''")
		lines[index] = lines[index].replace('</b>', "'''")
	
	if not re.fullmatch('\s*', lines[index]):
		lines[index] += '\n'
	if index < len(lines) - 2:
		while lines[index] == '\n' and lines[index + 1] == '\n':
			lines.pop(index)
	
	while ' )' in lines[index]:
		lines[index] = lines[index].replace(' )', ')')
	while '( ' in lines[index]:
		lines[index] = lines[index].replace('( ', '(')
	while re.search('[^\s\(]\(', lines[index]):
		lines[index] = re.sub('([^\s\(])\(', r'\1 (',lines[index])
	while re.search('\)[^\s\)]', lines[index]):
		lines[index] = re.sub('\)([^\s\)])', r') \1', lines[index])
	
	while '׃' in lines[index]:
		lines[index] = lines[index].replace('׃', ':')
	while ' :' in lines[index]:
		lines[index] = lines[index].replace(' :', ':')
	while '  ' in lines[index]:
		lines[index] = lines[index].replace('  ', ' ')
	while ' .' in lines[index]:
		lines[index] = lines[index].replace(' .', '.')
	while ' ,' in lines[index]:
		lines[index] = lines[index].replace(' ,', ',')

'''for index, line in enumerate(lines):
	if line.startswith('==='):
		break
	else:
		lines.pop(index)'''

promo = """{{-stop-}}
{{-start-}}
\'\'\'%s על הש"ס/%s/פרק א\'\'\'
{{מפרשים למסכת %s|%s|א}}
{{תוכן עניינים שטוח}}
{{המרת או.סי.אר 2}}
""" % (parshan, masechet, masechet, parshan)

fixed_parshan = parshan
if '"' in parshan:
	fixed_parshan = parshan.replace('"', '')
new_file = open('/sdcard/MyAppSharer/' + fixed_parshan + ' ' + masechet + '.txt', 'w+')
new_file.write(promo)
new_file.writelines(lines)

new_file.seek(0)
content = new_file.readlines()
for i, line in enumerate(content):
	if i < len(content) - 2:
		while content[i] == '\n' and content[i + 1] == '\n':
			content.pop(i)
		while content[i].startswith('===') and content[i + 2].startswith('==='):
			content.pop(i)
			content.pop(i)
new_file.seek(0)
new_file.writelines(content)
new_file.truncate(new_file.tell())
new_file.close()
print('completed')
