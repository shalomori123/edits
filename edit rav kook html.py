from os.path import isfile
path = '/sdcard/MyAppSharer/assets/' + input('enter directory: ')
for num in range(1, 18):
	if not isfile(path + '/%d.html' % num):
		break
	file = open(path + '/%d.html' % num, 'r+')
	read_lines = file.readlines()
	lines = [line for line in read_lines if '<div' not in line and '</div>' not in line]
	for index, line in enumerate(lines):
		print(index)
		if '<h1' in line:
			lines[index] = line.replace('<h1 class="entry-title">', '==')
			lines[index] = lines[index].replace('</h1>', '==')
		elif '<p>' in line or '</p>' in line:
			lines[index] = line.replace('<p>', '')
			lines[index] = lines[index].replace('</p>', '')
		while lines[index].startswith(' '):
			lines[index] = lines[index][1:]
		while '\t' in lines[index]:
			lines[index] = lines[index].replace('\t', '')
		"""if True:
			lines[index] += '\n'"""
		if index < len(lines) - 1:
			if lines[index] == '\n' and lines[index + 1] == '\n':
				lines.pop(index)
	file.seek(0)
	file.writelines(lines)
	file.truncate(file.tell())
	file.close()
print('completed')