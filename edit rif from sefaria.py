import re

from os.path import isfile
path = r'C:\Users\דנינו\שלום אורי\python\edits\MyAppSharer\\' + input('enter file name: ')

masechet = input('מסכת: ')
ALEPHBET = ('', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י',
			'יא', 'יב', 'יג', 'יד', 'טו', 'טז', 'יז', 'יח', 'יט', 'כ',
			'כא', 'כב', 'כג', 'כד', 'כה', 'כו', 'כז', 'כח', 'כט', 'ל',
			'לא', 'לב', 'לג', 'לד', 'לה', 'לו', 'לז', 'לח', 'לט', 'מ',
			'מא', 'מב', 'מג', 'מד', 'מה', 'מו', 'מז', 'מח', 'מט', 'נ',
			'נא', 'נב', 'נג', 'נד', 'נה', 'נו', 'נז', 'נח', 'נט', 'ס',
			'סא', 'סב', 'סג', 'סד', 'סה', 'סו', 'סז', 'סח', 'סט', 'ע',
			'עא', 'עב', 'עג', 'עד', 'עה', 'עו', 'עז', 'עח', 'עט', 'פ',
			'פא', 'פב', 'פג', 'פד', 'פה', 'פו')

if isfile(path):
	file = open(path, 'r')
	content = file.read()
	read_units = content.split('\nפרק')
	file.close()
	read_units.pop(0)
	input(str(len(read_units)) + 'פרקים')
	for unit in read_units:
		lines = unit.split('\n')
		for index, line in enumerate(lines):
			print(index)
			if 'Daf' in line:
				daf_rif = line.split(' ')[1]
				if daf_rif[1].isnumeric():
					num_daf = daf_rif[:2]
					page = daf_rif[2]
				else:
					num_daf = daf_rif[0]
					page = daf_rif[1]
				if page == 'a' and num_daf != '1':
					prev_page = ALEPHBET[int(num_daf) - 1] + ' ב'
					current = ALEPHBET[int(num_daf)] + ' א'
				elif page == 'a' and num_daf == '1':
					prev_page = ''
					current = ALEPHBET[int(num_daf)] + ' א'
				elif page == 'b':
					prev_page = ALEPHBET[int(num_daf)] + ' א'
					current = ALEPHBET[int(num_daf)] + ' ב'
				lines[index] = '<קטע סוף=%s/>{{דף רי"ף|%s}} <קטע התחלה=%s/>' % (prev_page, current, current)
				lines.pop(index + 1)
			
			elif '(דף' in line:
				lines[index] = line.replace('(דף ', '{{הפניה-גמ|%s|' % masechet)
				lines[index] = lines[index].replace('.)', '|א}} ')
				lines[index] = lines[index].replace(':)', '|ב}} ')
			elif line.startswith('דף '):
				lines[index] = line.replace('דף ', '{{הפניה-גמ|%s|' % masechet, 1)
				if line.split(' ', 2)[1].endswith('.'):
					lines[index] = lines[index].replace('.', '|א}} ', 1)
				elif line.split(' ', 2)[1].endswith(':'):
					lines[index] = lines[index].replace(':', '|ב}} ', 1)
				else:
					a = lines[index].split(' ', 1)
					a.insert(1, '}}')
					lines[index] = ' '.join(a)
			
			while re.search('״[א-פ]:[י-כ]״', lines[index]) or re.search('׳:[א-ת]׳', lines[index]) \
				or re.search('״[א-פ]:[א-ת]׳', lines[index]) or re.search('׳:[א-ת]״', lines[index]):
				lines[index] = lines[index].replace('׳', '')
				lines[index] = lines[index].replace('״', '')
				lines[index] = lines[index].replace(':', ' ')
				lines[index] = lines[index].replace('(', '([[', 1)
				lines[index] = lines[index].replace(')', ']])', 1)
			
			while '  ' in lines[index]:
				lines[index] = lines[index].replace('  ', ' ')
			while ' )' in lines[index]:
				lines[index] = lines[index].replace(' )', ')')
			while '( ' in lines[index]:
				lines[index] = lines[index].replace('( ', '(')
			while re.search('[^ ]\(', lines[index]):
				lines[index] = lines[index].replace('(', ' (')
			while re.search('\)[^ ]', lines[index]):
				lines[index] = lines[index].replace(')', ') ')
			
			if line.startswith('מתני\''):
				lines[index] = lines[index].replace('מתני', "'''מתני'''", 1)
			if line.startswith('גמ\''):
				lines[index] = lines[index].replace('גמ', "'''גמ'''", 1)
			if len(line.split(' ')) == 1 and line.isalpha():
				lines[index] = "'''" + lines[index] + "''' "
			
			if len(line.split(' ')) > 1 and not lines[index].startswith('<קטע סוף') \
				and not (lines[index].startswith('{{הפניה')
					and (lines[index].endswith('}}') or lines[index].endswith('}} '))):
				lines[index] += '\n\n'
			if index < len(lines) - 2:
				if lines[index] == '\n' and lines[index + 1] == '\n':
					lines.pop(index)
		
		perek = lines[0].split(' ')[1]
		new_file = open(r'C:\Users\דנינו\שלום אורי\python\edits\MyAppSharer\\' + masechet + ' פרק ' + perek + '.txt', 'w')
		new_file.writelines(lines)
		new_file.close()
else:
	print('file path error')
print('completed')
