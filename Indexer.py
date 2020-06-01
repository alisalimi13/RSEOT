# In The Name Of Allah

import os

#variables
DocsDir = 'E:\Working\Python\SearchEngineOnTxt\RankingSEOT\MyDocs'
IndexDir = 'E:\Working\Python\SearchEngineOnTxt\RankingSEOT\Index.txt'
DocIDDir = 'E:\Working\Python\SearchEngineOnTxt\RankingSEOT\DocID.txt'
Index = []
DocID = []
StopList = [ '', 'a', 'an', 'the', 'this', 'that', 'these', 'those', 'there' ]
StopChars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
				'.', ';', ':', ',', '?', '!', '"', "'",
				'{', '}', '[', ']', '(', ')', '<', '>',
				'+', '-', '*', '/', '%', '=', 
				'&', '|', '^', '~',
				'`', '@', '#', '$', '\\', '_', '“', '”' ]

def manipulate( t ):
	for c in StopChars:
		t = t.replace( c, '' )
	while True:
		if t.endswith( ('s', 'e', 'l') ):
			t = t[:-1]
			continue
		if t.endswith( ('ed', 'ly') ):
			t = t[:-2]
			continue
		if t.endswith( 'ing' ):
			t = t[:-3]
			continue
		break
	return t
			

for root, dirs, files in os.walk(DocsDir):
	print( files, end='\n\n' )
	DocID = files
	print( DocID, end='\n\n' )
	
	for fname in files:
	
		#open
		f = open( DocsDir + '\\' + fname , 'r' )
		
		#extracting
		s = f.read()
		print(s, end='\n\n')
		s = s.replace( '\n', ' ' )
		s = s.replace( '\t', ' ' )
		print(s, end='\n\n')
		ss = s.split(' ')
		print(ss, end='\n\n')
		
		l = []
		for token in ss:
			token = token.lower()
			token = manipulate(token)
			if token in StopList:
				continue
			l.append( token )
		
		#indexing
		for tname in l:
			#if tname == '':
			#	continue
			for i in Index:
				if tname == i[0]:
					for j in i:
						if j == DocID.index(fname):
							break
					else:
						i.append(DocID.index(fname))
				if tname == i[0]:
					break
			else:
				Index.append([tname, DocID.index(fname)])
				
		#close
		f.close()

Index.sort()				
print(Index, end='\n\n')

DocIDFile = open( DocIDDir, 'w' )
for i in DocID:
	DocIDFile.write( i + ' ')
DocIDFile.close()

IndexFile = open( IndexDir, 'w' )
for i in Index:
	for j in i:
		IndexFile.write( str(j) + ' ')
	IndexFile.write('\n')
IndexFile.close()