import re
import MySQLdb
from collections import Counter
db = MySQLdb.connect("localhost","root","akku","opptest" )
cursor = db.cursor()
cursor.execute("SELECT * FROM message")
results = cursor.fetchall()
string=""
for row in results:
      msg = row[0]
      string = string + " "+ msg
words = re.findall(r'\w+', string)
orignal_word_list = [word.lower() for word in words]
remove_words_list = ['i','am','to','are','is','will']
new_list = [x for x in orignal_word_list if x not in remove_words_list]

word_counts = Counter(new_list)
print word_counts
db.commit()
db.close()