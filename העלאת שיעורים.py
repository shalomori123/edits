import os
import shutil

CURRENT_YEAR = "התשפ''א"
ALEPHBET = ('א','ב','ג','ד','ה','ו','ז','ח','ט','י',
            'יא','יב','יג','יד','יהא','יוא','יז','יח','יט','כ',
            'כא','כב','כג','כד','כה','כו','כז','כח','כט','ל',
            'לא','לב','לג','לד','לה','לו','לז','לח','לט','מ',
            'מא','מב','מג','מד','מה')


def copy_to_edit(directory1, directory2):
        print('מעתיק קבצים...')
        for file in os.listdir(directory1):
                open_file = open(directory1 + file, 'rb')
                shutil.copy2(directory1 + file, directory2 + file)
                open_file.close()
                open(directory2 + file, 'rb').close()
                print('קובץ %s הועתק בהצלחה' % file)
        print('הסתיימה העתקת הקבצים!')


def define_recorder():
        recorder = input("מספר מקלט: ")
        if recorder in ["3", "מקלט 3"]:
                directory1=r"D:\dvr\hp\\"
        elif recorder in ["1", "מקלט 1", "2", "מקלט 2"]:
                directory1=r"D:\RECORD\\"
        elif recorder == "":
                dont_copy = input("האם לדלג על העתקה מהמקלט? ")
                if dont_copy == "כן":
                        directory1 = ""
                else:
                        directory1 = None
        else:
                directory1 = None
        return directory1


def full_rav_name(rav, directory4):
        short_names = [["מרן רה''י", "מרן", "הרב שבתי סבתו", "הרב סבתו", "הרב שבתי"],
                       ["רה''י הרב יצחק", "רהי", "רה''י", "הרב יצחק", "הרב יצחק סבתו", "יצחק"],
                       ["הרב אחיה סנדובסקי", "הרב אחיה", "הרב סנדובסקי", "אחיה", "סנדובסקי"],
                       ["הרב אליהו דורדק", "הרב אלי דורדק", "הרב אלי", "הרב דורדק", "דורדק"],
                       ["הרב אליסף יעקבסון", "הרב אליסף", "הרב יעקבסון", "הרב יעקובסון", "הרב אליסף יעקובסון", "יעקבסון"],
                       ["הרב גבריאל גולדמן", "הרב גולדמן", "גולדמן"],
                       ["הרב חיים גרינשפן", "הרב גרינשפן", "הגרח", "הגר''ח", "גרח", "גר''ח", "גרינשפן"],
                       ["הרב חיים סבתו", "הרב חיים", "חיים"],
                       ["הרב חן חלמיש", "הרב חן", "חן"],
                       ["הרב יובל אהרוני", "הרב יובל", "יובל"],
                       ["הרב יוסף מימון", "הרב יוסף", "יוסף"],
                       ["הרב יעקב חזן", "הרב חזן", "חזן"],
                       ["הרב יעקב סבתו", "הרב יעקב", "יעקב"],
                       ["הרב יצחק חי זאגא", "הרב יצחק זאגא", "הרב זאגא", "זאגא"],
                       ["הרב צבי אליהו סקולניק", "הרב צביאלי סקולניק", "הרב צביאלי", "הרב סקולניק", "צביאלי"],
                       ["הרב צדוק אליאס", "הרב צדוק", "צדוק"],
                       ["הרב ראובן פיירמן", "הרב פיירמן", "פיירמן"],
                       ["הרב ראובן ששון", "הרב ראובן", "ראובן"]]
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


def rav_directory(rav, directory4):
        if rav == "מרן רה''י":
                return directory4 + "\מרן רה''י - הרב שבתי סבתו"
        elif rav == "רה''י הרב יצחק":
                return directory4 + "\רה''י - הרב יצחק סבתו"
        else:
                return directory4 + "\\" + rav


def choose_topic(rav, directory4):
        if os.path.isdir(rav_directory(rav, directory4)):
                rav_directories = next(os.walk(rav_directory(rav, directory4)))[1]
                rav_directories.append("אחר")
                for i in range(len(rav_directories)):
                        if "עיון" in rav_directories[i]:
                                rav_directories[i] = "עיון"
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


def edit_names(directory2, directory4, month):
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
                rav_name = full_rav_name(short_rav_name, directory4)
                general_topic = choose_topic(rav_name, directory4)
                extension = os.path.splitext(directory2 + file)[1]
                name = rav_name + ' - ' + general_topic + ' - ' + fixed_day + month + " " + CURRENT_YEAR + ' - ' + lesson_title + extension
                os.rename(directory2 + file, directory2 + name)
                print('שם הקובץ שונה.\nהבא בתור:')


def cut_at_the_end(directory2, directory3, directory4):
        to_move = input('כל השמות שונו, האם להעביר לתיקיות? ')
        input("סגור את הנגן.")
        while to_move != 'כן':
                to_move = input('האם להעביר לתיקיות? ')
        delete_old = input("האם לפנות את תיקיית שיעורים מהשבוע האחרון? ") # פינוי תיקיית שיעורים מהשבוע האחרון
        if delete_old == "כן":
                for old_file in os.listdir(directory3):
                        os.remove(directory3 + old_file)
        for file in os.listdir(directory2):
                open_file = open(directory2 + file, 'rb+')
                shutil.copy2(directory2 + file, directory3 + file)
                open_file.close()
                
                name_list = file.split(' - ')# העברה לתיקיות של כל רב ורב אם אפשר ואם לא לתיקיית השנה
                if os.path.isdir(rav_directory(name_list[0], directory4) + '/' + name_list[1]):
                        check_prev = os.listdir(rav_directory(name_list[0], directory4) + '/' + name_list[1]) # הוספת אות האינדקס בתחילת שם הקובץ
                        check_prev.sort()
                        prev_index = check_prev[-1].split(" - ", 1)[0]
                        index_letter = "א"
                        for index, letter in enumerate(ALEPHBET):
                                if letter == prev_index:
                                        index_letter = ALEPHBET[index + 1]
                        if index_letter == "א":
                                print("\n\n\nשים לב! האות התחילית בתיקיית %s היא א'! תקן זאת בהקדם!\n\n\n\n" % rav_directory(name_list[0]))
                        shutil.copy2(directory2 + file, rav_directory(name_list[0], directory4) + '/' + name_list[1] + "/" + index_letter + " - " + file)
                        """החלטתי לבטל את ההעברה לתיקיית הרב אם אי אפשר לתוך נושא ספציפי כדי לרכז הכל בתיקיית השנה:
                        elif os.path.isdir(directory4 + '/' + name_list[0]):
                        os.replace(directory2 + "/" + file, rav_directory(name_list[0]) + "/" + file)"""
                else:
                        shutil.copy2(directory2 + file, directory4 + file)
                os.remove(directory2 + file)
                print('הקובץ %s הועבר והועתק בהצלחה' % file)
        print('כל הקבצים הועתקו בהצלחה!')


def delete_recorder(directory1):
        to_delete = input("האם לרוקן את המקלט? ")
        if to_delete == "כן":
                for old_file in os.listdir(directory1):
                        os.remove(directory1 + old_file)


def main():
        print('ברוך הבא לתוכנת העלאת השיעורים!\n אשריך!')
        to_start = input('כדי להתחיל כתוב "התחל": ')
        while to_start != 'התחל':
                to_start = input('כדי להתחיל כתוב "התחל": ')
                
        directory2=r"C:\Users\Administrator\Desktop\הקלטות חדשות\\" #תיקיית הקלטות חדשות
        directory3=r"C:\Users\Administrator\Desktop\שיעורי הישיבה הגבוהה\שיעורים מהשבוע האחרון\\" #תיקיית שיעורים מהשבוע האחרון
        directory4=r"C:\Users\Administrator\Desktop\שיעורי הישיבה הגבוהה\שיעורי הישיבה הגבוהה\שיעורים תשפ''א 81\\" #תיקיית השנה הנוכחית

        directory1 = define_recorder() #המיקום של הקבצים במקלט
        while directory1 is None:
                directory1 = define_recorder()
        if directory1:
                copy_to_edit(directory1, directory2)
        
        current_month = input('מה החודש עכשיו? (אם משתנה נא להשאיר ריק) ')
        if current_month:
                current_month = " " + current_month
        
        edit_names(directory2, directory4, current_month)
        cut_at_the_end(directory2, directory3, directory4)
        if directory1:
                delete_recorder(directory1)
        print('\nפעולת התוכנה הסתיימה.\nאנא לא לשכוח לעבור לתיקיית שנת %s כדי לסיים את המלאכה.\nאשריך וטוב לך ובהצלחה במשמר!' % CURRENT_YEAR)

main()
