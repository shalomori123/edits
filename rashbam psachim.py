import re

path = '/sdcard/MyAppSharer/' + input('enter file name: ')
from os.path import isfile
while not isfile(path):
	print('wrong path')
	path = '/sdcard/MyAppSharer/' + input('enter file name: ')
masechet = 'פסחים'
parshan = 'רשב"ם'

file = open(path, 'r')
lines = file.readlines()
file.close()
for index, line in enumerate(lines):
	print(index)
	while "''" in lines[index]:
		lines[index] = lines[index].replace("''", '"')
	
	if line.startswith('~ דף'):
		line = line.replace('~ דף ', '')
		line = line.replace(' - ', ' ')
		line = line.replace('\n', '')
		lines[index] = '<קטע סוף=רשבם/>{{-stop-}}\n{{-start-}}\n\'\'\'פסחים %s\'\'\'\n\n==רשב"ם==\n<קטע התחלה=רשבם/>' % line
	
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
	while '<B>' in lines[index]:
		lines[index] = lines[index].replace('<B>', "\n\n'''")
		lines[index] = lines[index].replace('</B>', "'''")
	
	if not re.fullmatch('\s*', lines[index]):
		lines[index] += '\n'
	if index < len(lines) - 2:
		while lines[index] == '\n' and lines[index + 1] == '\n':
			lines[index] = ''
	
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

fixed_parshan = parshan
if '"' in parshan:
	fixed_parshan = parshan.replace('"', '')
new_file = open('/sdcard/MyAppSharer/' + fixed_parshan + ' ' + masechet + '.txt', 'w+')
new_file.writelines(lines)

new_file.seek(0)
content = new_file.readlines()
for i, line in enumerate(content):
	if i < len(content) - 2:
		while content[i] == '\n' and content[i + 1] == '\n':
			content[i] = ''
new_file.seek(0)
new_file.writelines(content)
new_file.truncate(new_file.tell())
new_file.close()
print('completed')
