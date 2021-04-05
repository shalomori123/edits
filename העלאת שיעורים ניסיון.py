import os
import shutil

print('ברוך הבא לתוכנת העלאת השיעורים!\n אשריך!')
to_start = input('כדי להתחיל כתוב "התחל": ')


directory1=r"C:\Users\Administrator\Desktop\ניסיון\ט1\\" #המיקום של הקבצים במקלט
directory2=r"C:\Users\Administrator\Desktop\ניסיון\ט2\\" #תיקיית הקלטות חדשות
directory3=r"C:\Users\Administrator\Desktop\ניסיון\ט3\\" #תיקיית שיעורים מהשבוע האחרון
directory4=r"C:\Users\Administrator\Desktop\ניסיון\ט4\\" #תיקיית השנה הנוכחית

current_year = "התשפ''א"
current_month = input('מה החודש עכשיו? (אם משתנה נא להשאיר ריק) ')
if current_month != "":
	current_month = " " + current_month
ALEPHBET = ('א','ב','ג','ד','ה','ו','ז','ח','ט','י',
	    'יא','יב','יג','יד','יהא','יוא','יז','יח','יט','כ',
	    'כא','כב','כג','כד','כה','כו','כז','כח','כט','ל',
	    'לא','לב','לג','לד','לה','לו','לז','לח','לט','מ',
	    'מא','מב','מג','מד','מה')


def copy_to_edit():
	print('מעתיק קבצים...')
	for file in os.listdir(directory1):
		open_file = open(directory1 + file, 'rb')
		shutil.copy2(directory1 + file, directory2)
		open_file.close()
		open(directory2 + file, 'rb').close()
		print('קובץ %s הועתק בהצלחה' % file)
	print('הסתיימה העתקת הקבצים!')


def full_rav_name(rav):
	short_names = [["מרן רה''י", "מרן", "הרב שבתי סבתו", "הרב סבתו", "הרב שבתי"],
		       ["רה''י הרב יצחק", "רהי", "רה''י", "הרב יצחק", "הרב יצחק סבתו", "יצחק"],
		       ["הרב אחיה סנדובסקי", "הרב אחיה", "הרב סנדובסקי", "אחיה", "סנדובסקי"],
		       ["הרב אליהו דורדק", "הרב אלי דורדק", "הרב אלי", "הרב דורדק", "דורדק"],
		       ["הרב אליסף יעקבסון", "הרב אליסף", "הרב יעקבסון", "הרב יעקובסון", "הרב אליסף יעקובסון", "יעקבסון"],
		       ["הרב גבריאל גולדמן", "הרב גולדמן", "גולדמן"],
		       ["הרב חיים גרינשפן", "הרב גרינשפן", "הגרח", "הגר''ח", "גרינשפן"],
		       ["הרב חיים סבתו", "הרב חיים"],
		       ["הרב חן חלמיש", "הרב חן", "חן"],
		       ["הרב יובל אהרוני", "הרב יובל", "יובל"],
		       ["הרב יוסף מימון", "הרב יוסף", "יוסף"],
		       ["הרב יעקב חזן", "הרב חזן", "חזן"],
		       ["הרב יעקב סבתו", "הרב יעקב", "יעקב"],
		       ["הרב יצחק חי זאגא", "הרב יצחק זאגא", "הרב זאגא", "זאגא"],
		       ["הרב צבי אליהו סקולניק", "הרב צביאלי סקולניק", "הרב צביאלי", "הרב סקולניק", "צביאלי"],
		       ["הרב צדוק אליאס", "הרב צדוק", "צדוק"],
		       ["הרב ראובן פיירמן", "הרב פיירמן", "פיירמן"],
		       ["הרב ראובן ששון", "הרב ראובן"]]
	name_exist = False
	for list in short_names:
		if rav in list:
			name_exist = True
	while not name_exist:
		other_rav = input("השם שכתבת אינו מופיע ברשימה. האם זה השם הנכון? ")
		if other_rav == "כן":
			return rav
		rav = input("בחר שם חדש: ")
		name_exist = False
		for list in short_names:
			if rav in list:
				name_exist = True
	for i, list in enumerate(short_names):
		if rav in list:
			full = list[0]
	return full


def rav_directory(rav):
	if rav == "מרן רה''י":
		return directory4 + "\מרן רה''י - הרב שבתי סבתו"
	elif rav == "רה''י הרב יצחק":
		return directory4 + "\רה''י - הרב יצחק סבתו"
	else:
		return directory4 + "\\" + rav


def choose_topic(rav):
	if os.path.isdir(rav_directory(rav)):
		rav_directories = next(os.walk(rav_directory(rav)))[1]
		rav_directories.append("אחר")
		for i in range(len(rav_directories)):
			if rav_directories[i] == "עיון - ב''מ פרק ראשון":
				rav_directories.append("עיון")
			if rav_directories[i] == "כולל - הלכות נידה":
				rav_directories[i] = "הלכות נידה"
		
		for count, item in enumerate(rav_directories, 1):
			print(str(count) + ". " + item)
		choose_num = input("בחר מספר: ")
		while not choose_num.isnumeric() or int(choose_num) > len(rav_directories):
			choose_num = input("בחר מספר: ")
		if int(choose_num) < len(rav_directories):
			return rav_directories[int(choose_num) - 1]
		elif int(choose_num) == len(rav_directories):
			enter_topic = input("נושא כללי: ")
			return enter_topic
	else:
		enter_topic = input("נושא כללי: ")
		return enter_topic


def edit_names():
	for file in os.listdir(directory2):
		open_file = open(directory2 + file, 'rb+')
		print('האזן לשיעור') # פתיחת הקובץ
		os.startfile(directory2 + file)
		open_file.close()
		
		is_valid_file = input('האם השיעור תקין? ') # בדיקה אם למחוק את הקובץ או לדלג עליו
		if is_valid_file == 'לא':
			statinfo = os.stat(directory2 + file)
			print('גודל הקובץ: ' + str(statinfo.st_size / 1000000) + 'Mb')
			to_remove = input('האם למחוק אותו? ')
			if to_remove == 'כן':
				os.remove(directory2 + file)
				print('הקובץ נמחק.')
			continue
			
		lesson_title = input("נושא השיעור: ") # שינוי השם עצמו
		day_in_month = input("תאריך (היום בחודש בלבד בלי מרכאות, אם לא הגדרת חודש בהתחלה הוסף אותו עכשיו): ")
		if len(day_in_month) == 1:
			fixed_day = day_in_month + "'"
		elif day_in_month[1] == " ":
			fixed_day = day_in_month[0] + "'" + day_in_month[1:]
		else:
			fixed_day = day_in_month[0] + "''" + day_in_month[1:]
		short_rav_name = input('שם הרב: ')
		rav_name = full_rav_name(short_rav_name)
		general_topic = choose_topic(rav_name)
		extension = os.path.splitext(directory2 + file)[1]
		name = rav_name + ' - ' + general_topic + ' - ' + fixed_day + current_month + " " + current_year + ' - ' + lesson_title + extension
		os.rename(directory2 + file, directory2 + name)
		print('שם הקובץ שונה.\nהבא בתור:')


def cut_at_the_end():
	to_move = input('כל השמות שונו, האם להעביר לתיקיות? ')
	input("סגור את הקובץ.")
	while to_move != 'כן':
		to_move = input('האם להעביר לתיקיות? ')
	delete_old = input("האם לפנות את תיקיית שיעורים מהשבוע האחרון? ") # פינוי תיקיית שיעורים מהשבוע האחרון
	if delete_old == "כן":
		for old_file in os.listdir(directory3):
			os.remove(directory3 + old_file)
	for file in os.listdir(directory2):
		open_file = open(directory2 + file, 'rb+')
		shutil.copy2(directory2 + file, directory3)
		open_file.close()
		
		name_list = file.split(' - ')# העברה לתיקיות של כל רב ורב אם אפשר ואם לא לתיקיית השנה
		if os.path.isdir(rav_directory(name_list[0]) + '/' + name_list[1]):
			check_prev = os.listdir(rav_directory(name_list[0]) + '/' + name_list[1]) # הוספת אות האינדקס בתחילת שם הקובץ
			check_prev.sort()
			prev_index = check_prev[-1].split(" - ", 1)[0]
			for index, letter in enumerate(ALEPHBET):
				if letter == prev_index:
					index_letter = ALEPHBET[index + 1]
			os.replace(directory2 + file, rav_directory(name_list[0]) + '/' + name_list[1] + "/" + index_letter + " - " + file)
			"""החלטתי לבטל את ההעברה לתיקיית הרב אם אי אפשר לתוך נושא ספציפי כדי לרכז הכל בתיקיית השנה:
			elif os.path.isdir(directory4 + '/' + name_list[0]):
			os.replace(directory2 + "/" + file, rav_directory(name_list[0]) + "/" + file)"""
		else:
			os.replace(directory2 + file, directory4 + file)
		print('הקובץ %s הועבר והועתק בהצלחה' % file)
	print('כל הקבצים הועתקו בהצלחה!\nפעולת התוכנה הסתיימה.\nאנא לא לשכוח לעבור לתיקיית שנת %s כדי לסיים את המלאכה.\nאשריך וטוב לך ובהצלחה במשמר!' % current_year)


if to_start == 'התחל':
	copy_to_edit()
	edit_names()
	cut_at_the_end()
