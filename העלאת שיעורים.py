 import​ ​os 
 ​import​ ​shutil 
 ​from​ ​re​ ​import​ ​match 
  
 ​CURRENT_YEAR​ ​=​ ​"התשפ''א" 
 ​ALEPHBET​ ​=​ (​'א'​,​'ב'​,​'ג'​,​'ד'​,​'ה'​,​'ו'​,​'ז'​,​'ח'​,​'ט'​,​'י'​, 
 ​            ​'יא'​,​'יב'​,​'יג'​,​'יד'​,​'יהא'​,​'יוא'​,​'יז'​,​'יח'​,​'יט'​,​'כ'​, 
 ​            ​'כא'​,​'כב'​,​'כג'​,​'כד'​,​'כה'​,​'כו'​,​'כז'​,​'כח'​,​'כט'​,​'ל'​, 
 ​            ​'לא'​,​'לב'​,​'לג'​,​'לד'​,​'לה'​,​'לו'​,​'לז'​,​'לח'​,​'לט'​,​'מ'​, 
 ​            ​'מא'​,​'מב'​,​'מג'​,​'מד'​,​'מה'​) 
  
 ​RAV_NAMES​ ​=​ [[​"מרן רה''י"​, ​"מרן"​, ​"הרב שבתי סבתו"​, ​"הרב סבתו"​, ​"הרב שבתי"​], 
 ​             [​"רה''י הרב יצחק"​, ​"רהי"​, ​"רה''י"​, ​"הרב יצחק"​, ​"הרב יצחק סבתו"​, ​"יצחק"​], 
 ​             [​"הרב אחיה סנדובסקי"​, ​"הרב אחיה"​, ​"הרב סנדובסקי"​, ​"אחיה"​, ​"סנדובסקי"​], 
 ​             [​"הרב אליהו דורדק"​, ​"הרב אלי דורדק"​, ​"הרב אלי"​, ​"הרב דורדק"​, ​"דורדק"​], 
 ​             [​"הרב אליסף יעקבסון"​, ​"הרב אליסף"​, ​"הרב יעקבסון"​, ​"הרב יעקובסון"​, ​"הרב אליסף יעקובסון"​, ​"יעקבסון"​], 
 ​             [​"הרב גבריאל גולדמן"​, ​"הרב גולדמן"​, ​"גולדמן"​], 
 ​             [​"הרב חיים גרינשפן"​, ​"הרב גרינשפן"​, ​"הגרח"​, ​"הגר''ח"​, ​"גרח"​, ​"גר''ח"​, ​"גרינשפן"​], 
 ​             [​"הרב חיים סבתו"​, ​"הרב חיים"​, ​"חיים"​], 
 ​             [​"הרב חן חלמיש"​, ​"הרב חן"​, ​"חן"​], 
 ​             [​"הרב יובל אהרוני"​, ​"הרב יובל"​, ​"יובל"​], 
 ​             [​"הרב יוסף מימון"​, ​"הרב יוסף"​, ​"יוסף"​], 
 ​             [​"הרב יעקב חזן"​, ​"הרב חזן"​, ​"חזן"​], 
 ​             [​"הרב יעקב סבתו"​, ​"הרב יעקב"​, ​"יעקב"​], 
 ​             [​"הרב יצחק חי זאגא"​, ​"הרב יצחק זאגא"​, ​"הרב זאגא"​, ​"זאגא"​], 
 ​             [​"הרב צבי אליהו סקולניק"​, ​"הרב צביאלי סקולניק"​, ​"הרב צביאלי"​, ​"הרב סקולניק"​, ​"צביאלי"​], 
 ​             [​"הרב צדוק אליאס"​, ​"הרב צדוק"​, ​"צדוק"​], 
 ​             [​"הרב ראובן פיירמן"​, ​"הרב פיירמן"​, ​"פיירמן"​], 
 ​             [​"הרב ראובן ששון"​, ​"הרב ראובן"​, ​"ראובן"​]] 
  
 ​class​ ​Lesson​: 
 ​        ​"""class to define one file of record.""" 
 ​        ​def​ ​__init__​(​self​, ​dir​, ​file_name​): 
 ​                ​self​.​dir​ ​=​ ​dir 
 ​                ​self​.​fname​ ​=​ ​file_name 
 ​                ​self​.​path​ ​=​ ​os.path.join(self​.​dir​, self​.​fname)
 ​                ​self​.​index_letter​ ​=​ ​'' 
 ​                ​self​.​rav​ ​=​ ​'' 
 ​                ​self​.​rav_dir​ ​=​ ​'' 
 ​                ​self​.​topic​ ​=​ ​'' 
 ​                ​self​.​day​ ​=​ ​'' 
 ​                ​self​.​month​ ​=​ ​'' 
 ​                ​self​.​year​ ​=​ ​CURRENT_YEAR 
 ​                ​self​.​date​ ​=​ ​self​.​day​ ​+​ ​' '​ ​+​ ​self​.​month​ ​+​ ​' '​ ​+​ ​self​.​year 
 ​                ​self​.​title​ ​=​ ​'' 
 ​                ​self​.​extension​ ​=​ ​os​.​path​.​splitext​(​self​.​path​)[​1​] 
 ​                ​self​.​name​ ​=​ ​' - '​.​join​([​self​.​index_letter​ ​+​ ​self​.​rav​, ​self​.​topic​, ​self​.​date​, ​self​.​title​]) 
  
 ​        ​def​ ​listen​(​self​): 
 ​                ​open_file​ ​=​ ​open​(​self​.​path​, ​'rb+'​) 
 ​                ​print​(​'האזן לשיעור'​) 
 ​                ​os​.​startfile​(​self​.​path​) 
 ​                ​open_file​.​close​() 
  
 ​        ​def​ ​delete_file​(​self​): 
 ​                ​os​.​remove​(​self​.​path​) 
 ​                ​print​(​'הקובץ נמחק.'​) 
  
 ​        ​def​ ​copy_file​(​self​, ​to_dir​): 
 ​                ​shutil​.​copy2​(​self​.​path​, ​os.path.join(to_dir​, self​.​fname​)) 
  
 ​        ​def​ ​move_file​(​self​, ​to_dir​): 
 ​                ​self​.​copy_file​(​to_dir​) 
 ​                ​self​.​delete_file​() 
 ​                ​self​.​dir​ ​=​ ​to_dir 
  
  
 ​        ​def​ ​parse_name​(​self​): 
 ​                ​pass 
  
 ​        ​def​ ​change_name​(​self​, ​name​=​None​): 
 ​                ​if​ ​name​ ​is​ ​None​: 
 ​                        ​name​ ​=​ ​self​.​name 
 ​                ​os​.​rename​(​self​.​path​, ​os.path.join(self​.​dir​, name​)) 
 ​                ​print​(​'שם הקובץ שונה.'​) 
 ​                ​self​.​fname​ ​=​ ​name 
  
 ​        ​def​ ​set_rav​(​self​, ​short_name​, ​directory4​): 
 ​                ​self​.​rav​ ​=​ ​self​.​full_rav_name​(​short_name​) 
 ​                ​self​.​rav_dir​ ​=​ ​self​.​rav_directory​(​self​.​rav​, ​directory4​) 
  
 ​        ​def​ ​full_rav_name​(​self​, ​short_name​): 
 ​                ​while​ ​True​: 
 ​                        ​for​ ​list​ ​in​ ​RAV_NAMES​: 
 ​                                ​if​ ​short_name​ ​in​ ​list​: 
 ​                                        ​return​ ​list​[​0​] 
 ​                        ​other_rav​ ​=​ ​input​(​"השם שכתבת אינו מופיע ברשימה. האם זה השם הנכון? (כן/כלום) "​) 
 ​                        ​if​ ​other_rav​ ​==​ ​"כן"​: 
 ​                            ​return​ ​short_name 
 ​                        ​short_name​ ​=​ ​input​(​"בחר שם חדש: "​) 
  
 ​        ​def​ ​rav_directory​(​self​, ​rav​, ​directory4​): 
 ​                ​if​ ​rav​ ​==​ ​"מרן רה''י"​: 
 ​                        ​return​ ​os.path.join(directory4​, "\מרן רה''י - הרב שבתי סבתו" )
 ​                ​elif​ ​rav​ ​==​ ​"רה''י הרב יצחק"​: 
 ​                        ​return​ ​os.path.join(directory4​, "\רה''י - הרב יצחק סבתו" )
 ​                ​else​: 
 ​                        ​return​ ​os.path.join(directory4​, rav) 
  
 ​        ​def​ ​set_topic​(​self​): 
 ​                ​if​ ​os​.​path​.​isdir​(​self​.​rav_dir​): 
 ​                        ​rav_directories​ ​=​ ​next​(​os​.​walk​(​self​.​rav_dir​))[​1​] 
 ​                        ​rav_directories​.​append​(​"אחר"​) 
 ​                        ​for​ ​i​ ​in​ ​range​(​len​(​rav_directories​)): 
 ​                                ​if​ ​"עיון"​ ​in​ ​rav_directories​[​i​]: 
 ​                                        ​rav_directories​[​i​] ​=​ ​"עיון" 
 ​                                ​if​ ​rav_directories​[​i​] ​==​ ​"כולל - הלכות נידה"​: 
 ​                                        ​rav_directories​[​i​] ​=​ ​"הלכות נידה" 
  
 ​                        ​for​ ​count​, ​item​ ​in​ ​enumerate​(​rav_directories​, ​1​): 
 ​                                ​print​(​str​(​count​) ​+​ ​". "​ ​+​ ​item​) 
 ​                        ​choose_num​ ​=​ ​input​(​"בחר מספר: "​) 
 ​                        ​while​ ​not​ ​choose_num​.​isnumeric​() ​or​ ​int​(​choose_num​) ​>​ ​len​(​rav_directories​): 
 ​                                ​choose_num​ ​=​ ​input​(​"בחר מספר: "​) 
 ​                        ​if​ ​int​(​choose_num​) ​<​ ​len​(​rav_directories​): 
 ​                                ​self​.​topic​ ​=​ ​rav_directories​[​int​(​choose_num​) ​-​ ​1​] 
 ​                        ​elif​ ​int​(​choose_num​) ​==​ ​len​(​rav_directories​): 
 ​                                ​enter_topic​ ​=​ ​input​(​"נושא כללי: "​) 
 ​                                ​self​.​topic​ ​=​ ​enter_topic 
 ​                ​else​: 
 ​                        ​enter_topic​ ​=​ ​input​(​"נושא כללי: "​) 
 ​                        ​self​.​topic​ ​=​ ​enter_topic 
  
 ​        ​def​ ​set_day​(​self​, ​day​): 
 ​                ​if​ ​len​(​day​.​split​(​' '​)[​-​1​]) ​==​ ​1​: 
 ​                        ​self​.​day​ ​=​ ​day​ ​+​ ​"'" 
 ​                ​else​: 
 ​                        ​self​.​day​ ​=​ ​day​[:​-​1​] ​+​ ​"''"​ ​+​ ​day​[​-​1​] 
  
 ​        ​def​ ​set_month​(​self​, ​month​): 
 ​                ​self​.​month​ ​=​ ​month 
  
 ​        ​def​ ​set_title​(​self​, ​title​): 
 ​                ​self​.​title​ ​=​ ​title 
  
 ​        ​def​ ​set_index​(​self​): 
 ​                ​if​ ​os​.​path​.​isdir​(​os.path.join(self​.​rav_dir​, self​.​topic​)): 
 ​                        ​check_prev​ ​=​ ​os​.​listdir​(​os.path.join(self​.​rav_dir​, self​.​topic​)) ​# הוספת אות האינדקס בתחילת שם הקובץ 
 ​                        ​check_prev​.​sort​() 
 ​                        ​prev_index​ ​=​ ​check_prev​[​-​1​].​split​(​" - "​, ​1​)[​0​] 
 ​                        ​# TODO parse_name method 
 ​                        ​# prev_lesson = Lesson(os.path.join(lesson.rav_dir, lesson.topic), check_prev[-1]) 
 ​                        ​# prev_lesson.parse_name() 
 ​                        ​# prev_index = prev_lesson.index_letter 
 ​                        ​self.index_letter​ ​=​ ​"א - " 
 ​                        ​for​ ​counter​, ​letter​ ​in​ ​enumerate​(​ALEPHBET​): 
 ​                                ​if​ ​letter​ ​==​ ​prev_index​: 
 ​                                        ​self​.​index_letter​ ​=​ ​ALEPHBET​[​counter​ ​+​ ​1​] ​+​ ​' - ' 
 ​                        ​if​ ​self.index_letter​ ​==​ ​"א - "​: 
 ​                                ​print​(​"​\n​\n​\n​שים לב! האות התחילית בתיקיית %s היא א'! תקן זאת בהקדם!​\n​\n​\n​\n​"​ ​%​ \ 
 ​                                      os.path.join(self​.​rav_dir​, self​.​topic​)) 
  
  
  
 ​def​ ​copy_to_edit​(​directory1​, ​directory2​): 
 ​        ​print​(​'מעתיק קבצים...'​) 
 ​        ​for​ ​file​ ​in​ ​os​.​listdir​(​directory1​): 
 ​                ​open_file​ ​=​ ​open​(​os.path.join(directory1​, file​), ​'rb'​) 
 ​                ​shutil​.​copy2​(​os.path.join(directory1​, file)​, ​os.path.join(directory2​, file​))
 ​                ​open_file​.​close​() 
 ​                ​open​(​os.path.join(directory2​, file​), ​'rb'​).​close​() 
 ​                ​print​(​'קובץ %s הועתק בהצלחה'​ ​%​ ​file​) 
 ​        ​print​(​'הסתיימה העתקת הקבצים!'​) 
  
  
 ​def​ ​define_recorder​(): 
 ​        ​recorder​ ​=​ ​input​(​"מספר מקלט: "​) 
 ​        ​if​ ​recorder​ ​in​ [​"3"​, ​"מקלט 3"​]: 
 ​                ​directory1​=​r"D:\dvr\hp\\" 
 ​        ​elif​ ​recorder​ ​in​ [​"1"​, ​"מקלט 1"​, ​"2"​, ​"מקלט 2"​]: 
 ​                ​directory1​=​r"D:\RECORD\\" 
 ​        ​elif​ ​recorder​ ​==​ ​""​: 
 ​                ​dont_copy​ ​=​ ​input​(​"האם לדלג על העתקה מהמקלט? "​) 
 ​                ​if​ ​dont_copy​ ​==​ ​"כן"​: 
 ​                        ​directory1​ ​=​ ​"" 
 ​                ​else​: 
 ​                        ​directory1​ ​=​ ​None 
 ​        ​else​: 
 ​                ​directory1​ ​=​ ​None 
 ​        ​return​ ​directory1 
  
  
 ​def​ ​edit_names​(​directory2​, ​directory4​, ​month​): 
 ​        ​for​ ​file​ ​in​ ​os​.​listdir​(​directory2​): 
 ​                ​lesson​ ​=​ ​Lesson​(​directory2​, ​file​) 
 ​                ​lesson​.​listen​() 
 ​                 
 ​                ​is_valid_file​ ​=​ ​input​(​'האם השיעור תקין? (לא/דלג/כלום) '​) ​# בדיקה אם למחוק את הקובץ או לדלג עליו 
 ​                ​if​ ​is_valid_file​ ​==​ ​"דלג"​: 
 ​                        ​continue 
 ​                ​if​ ​is_valid_file​ ​==​ ​'לא'​: 
 ​                        ​statinfo​ ​=​ ​os​.​stat​(​os.path.join(directory2​, file​)) 
 ​                        ​print​(​'גודל הקובץ: '​ ​+​ ​str​(​statinfo​.​st_size​ ​/​ ​1000000​) ​+​ ​'Mb'​) 
 ​                        ​to_remove​ ​=​ ​input​(​'האם למחוק אותו? (כן/כלום) '​) 
 ​                        ​if​ ​to_remove​ ​==​ ​'כן'​: 
 ​                                ​lesson​.​delete_file​() 
 ​                                ​continue 
 ​                         
 ​                ​lesson_title​ ​=​ ​input​(​"נושא השיעור: "​) ​# שינוי השם עצמו 
 ​                ​lesson​.​set_title​(​lesson_title​) 
  
 ​                ​day_in_month​ ​=​ ​input​(​"תאריך (היום בחודש בלבד בלי מרכאות, אם לא הגדרת חודש בהתחלה הוסף אותו עכשיו): "​) 
 ​                ​split_day​ ​=​ ​day_in_month​.​split​(​' '​) 
 ​                ​if​ ​match​(​'[ט-ל][א-ט]'​, ​split_day​[​0​]): 
 ​                        ​fixed_day​ ​=​ ​split_day​[​0​] 
 ​                        ​if​ ​len​(​split_day​) ​>​ ​1​: 
 ​                                ​month​ ​=​ ​split_day​[​1​] 
 ​                ​elif​ ​match​(​'[ט-ל][א-ט]'​, ​split_day​[​1​]): 
 ​                        ​fixed_day​ ​=​ ​' '​.​join​(​split_day​[:​-​1​]) 
 ​                        ​if​ ​len​(​split_day​) ​>​ ​2​: 
 ​                                ​month​ ​=​ ​split_day​[​-​1​] 
 ​                ​else​: 
 ​                        ​fixed_day​ ​=​ ​day_in_month 
 ​                ​lesson​.​set_day​(​fixed_day​) 
 ​                ​lesson​.​set_month​(​month​) 
  
 ​                ​short_rav_name​ ​=​ ​input​(​'שם הרב: '​) 
 ​                ​lesson​.​set_rav​(​short_rav_name​, ​directory4​) 
 ​                ​lesson​.​set_topic​() 
  
 ​                ​lesson​.​change_name​() 
  
  
 ​def​ ​cut_at_the_end​(​directory2​, ​directory3​, ​directory4​): 
 ​        ​to_move​ ​=​ ​input​(​'כל השמות שונו, האם להעביר לתיקיות? (כן) '​) 
 ​        ​input​(​"סגור את הנגן."​) 
 ​        ​while​ ​to_move​ ​!=​ ​'כן'​: 
 ​                ​to_move​ ​=​ ​input​(​'האם להעביר לתיקיות? (כן) '​) 
 ​        ​delete_old​ ​=​ ​input​(​"האם לפנות את תיקיית שיעורים מהשבוע האחרון? (כן/כלום) "​) ​# פינוי תיקיית שיעורים מהשבוע האחרון 
 ​        ​if​ ​delete_old​ ​==​ ​"כן"​: 
 ​                ​for​ ​old_file​ ​in​ ​os​.​listdir​(​directory3​): 
 ​                        ​os​.​remove​(​os.path.join(directory3​, old_file​)) 
 ​        ​for​ ​file​ ​in​ ​os​.​listdir​(​directory2​): 
 ​                ​lesson​ ​=​ ​Lesson​(​directory2​, ​file​) 
 ​                ​lesson​.​copy_file​(​directory3​) 
 ​                 
 ​                ​# העברה לתיקיות של כל רב ורב אם אפשר ואם לא לתיקיית השנה 
 ​                ​lesson​.​set_index​() 
 ​                ​lesson​.​change_name​() 
 ​                ​if​ ​os​.​path​.​isdir​(​os.path.join(lesson​.​rav_dir​, lesson​.​topic​)): 
 ​                        ​lesson​.​move_file​(​os.path.join(lesson​.​rav_dir​, lesson​.​topic​)) 
 ​                ​else​: 
 ​                        ​lesson​.​move_file​(​directory4​) 
 ​                ​print​(​'הקובץ %s הועבר והועתק בהצלחה'​ ​%​ ​file​) 
 ​        ​print​(​'כל הקבצים הועתקו בהצלחה!'​) 
  
  
 ​def​ ​delete_recorder​(​directory1​): 
 ​        ​to_delete​ ​=​ ​input​(​"האם לרוקן את המקלט? "​) 
 ​        ​if​ ​to_delete​ ​==​ ​"כן"​: 
 ​                ​for​ ​old_file​ ​in​ ​os​.​listdir​(​directory1​): 
 ​                        ​os​.​remove​(​os.path.join(directory1​, old_file​)) 
  
  
 ​def​ ​main​(): 
 ​        ​print​(​'ברוך הבא לתוכנת העלאת השיעורים!​\n​ אשריך!'​) 
 ​        ​to_start​ ​=​ ​input​(​'כדי להתחיל כתוב "התחל": '​) 
 ​        ​while​ ​to_start​ ​!=​ ​'התחל'​: 
 ​                ​to_start​ ​=​ ​input​(​'כדי להתחיל כתוב "התחל": '​) 
 ​                 
 ​        ​directory2​=​r"C:\Users\Administrator\Desktop\הקלטות חדשות\\"​ ​#תיקיית הקלטות חדשות 
 ​        ​directory3​=​r"C:\Users\Administrator\Desktop\שיעורי הישיבה הגבוהה\שיעורים מהשבוע האחרון\\"​ ​#תיקיית שיעורים מהשבוע האחרון 
 ​        ​directory4​=​r"C:\Users\Administrator\Desktop\שיעורי הישיבה הגבוהה\שיעורי הישיבה הגבוהה\שיעורים תשפ''א 81\\"​ ​#תיקיית השנה הנוכחית 
  
 ​        ​directory1​ ​=​ ​define_recorder​() ​#המיקום של הקבצים במקלט 
 ​        ​while​ ​directory1​ ​is​ ​None​: 
 ​                ​directory1​ ​=​ ​define_recorder​() 
 ​        ​if​ ​directory1​: 
 ​                ​copy_to_edit​(​directory1​, ​directory2​) 
 ​         
 ​        ​current_month​ ​=​ ​input​(​'מה החודש עכשיו? (אם משתנה נא להשאיר ריק) '​) 
 ​         
 ​        ​edit_names​(​directory2​, ​directory4​, ​current_month​) 
 ​        ​cut_at_the_end​(​directory2​, ​directory3​, ​directory4​) 
 ​        ​if​ ​directory1​: 
 ​                ​delete_recorder​(​directory1​) 
 ​        ​print​(​'​\n​פעולת התוכנה הסתיימה.​\n​אנא לא לשכוח לעבור לתיקיית שנת %s כדי לסיים את המלאכה.​\n​אשריך וטוב לך ובהצלחה במשמר!'​ ​%​ ​CURRENT_YEAR​) 
  
 ​main​()