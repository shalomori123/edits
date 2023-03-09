def full_rav_name(rav):
	short_names = [["מרן רה''י", "מרן", "הרב שבתי סבתו", "הרב סבתו", "הרב שבתי"], ["רה''י הרב יצחק", "רהי", "רה''י", "הרב יצחק", "הרב יצחק סבתו", "יצחק"]]
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
		rav_directories = os.walk(rav_directory(rav))[1]
		rav_directories.append("אחר")
		for count, item in enumerate(rav_directories, 1):
			print(count + ". " + item)
		choose_num = input("בחר מספר: ")
		while not choose_num.isnumeric() and int(choose_num) <= len(rav_directories):
			choose_num = input("בחר מספר: ")
		if int(choose_num) < len(rav_directories):
			return rav_directories[int(choose_num) - 1]
		elif int(choose_num) == len(rav_directories):
			enter_topic = input("נושא השיעור: ")
			return enter_topic
	else:
		enter_topic = input("נושא השיעור: ")
		return enter_topic