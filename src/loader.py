import sqlite3

# This script is used to load WORDNET data from the sqlite database into a json file

QUERY = '''
select senses.wordid, lemma, senses.sensekey, pos, position
from senses
join words
	using (wordid)
join senses30
	using (sensekey)
left join adjpositions 
	using (wordid,synsetid);
'''


con = sqlite3.connect("sqlite-31.db")
cur = con.cursor()
res = cur.execute(QUERY.strip())

with open("vocab.json", "w") as f:
	f.write('[')
	x = res.fetchone()
	while x is not None:
		f.write(f'{{"wordid":{x[0]}, "lemma":"{x[1]}", "sensekey":"{x[2]}", "pos":"{x[3]}", "position":"{x[4]}"}},\n')
		x =res.fetchone()
	f.write(']')
con.close()
