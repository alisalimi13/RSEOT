#In The Name Of Allah

import tkinter as tk

#variables
DocsDir = 'MyDocs'
IndexDir = 'Index.txt'
DocIDDir = 'DocID.txt'
Index = []
DocID = []
StopList = [ '', 'a', 'an', 'the', 'this', 'that', 'these', 'those', 'there' ]
StopChars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
				'.', ';', ':', ',', '?', '!', '"', "'",
				'{', '}', '[', ']', '(', ')', '<', '>',
				'+', '-', '*', '/', '%', '=', 
				'&', '|', '^', '~',
				'`', '@', '#', '$', '\\', '_', '“', '”' ]
Query = ''
ResultList = []
ReqResDir = ''
ReqResCon = ''

#functions

def Search(w):
	w.title('RankingSEOT')
	#w.minsize(500, 500)
	welcome = tk.Label( w, text='Welcome' ).pack()
	query = tk.Entry( w, textvariable = EnteredText ).pack()
	search = tk.Button(w, text='Search', command = SearchButton).pack(side = tk.BOTTOM)
	w.mainloop()
	
def SearchButton():
	SearchWindow.quit()
	SearchWindow.destroy()
	
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
	
def ResultShow(w, l):
	w.title('RankingSEOT')
	#w.minsize(500, 500)
	welcome = tk.Label( w, text='Results' ).pack()
	ButtonList = []
	for r in l:
		ButtonList.append( tk.Button(w, text = r, command = lambda t = l[l.index(r)]: DocButton(t)) )
	for b in ButtonList:
		b.pack()
	w.mainloop()
		
def DocButton(n):
	global ReqResDir
	ReqResDir = DocsDir + '\\' + n
	print('\nRequsted Result: {}\n'.format(n))
	ResulWindow.quit()
	ResulWindow.destroy()
	
def ChoosenResultShow( w, s ):
	w.title('RankingSEOT')
	#w.minsize(500, 500)
	welcome = tk.Label( w, text='Content' ).pack()
	t = tk.Label( w, text = s ).pack()
	w.mainloop()
	


#reading DocID
print('\n')
DocIDFile = open( DocIDDir, 'r' )
for line in DocIDFile:
	line = line.replace( ' \n', '' )
	print(line)
	DocID = line.split(' ')
DocID.remove('')
print()
print(DocID)
DocIDFile.close()
print('\n')

#reading Index
IndexFile = open( IndexDir, 'r' )
for line in IndexFile:
	line = line.replace( ' \n', '' )
	print(line)
	Index.append(line.split(' '))
for i in Index:
	first = True
	for j in i:
		if first:
			first = not first
		else:
			Index[Index.index(i)][i.index(j)] = int(j)		
print()
print(Index)
IndexFile.close()
print('\n')

#query processing

#get query
SearchWindow = tk.Tk()
EnteredText = tk.StringVar()
Search( SearchWindow )
Query = EnteredText.get()

#query to result
temp = Query.split( ' ' )
QuEl = []
for token in temp:
			token = token.lower()
			token = manipulate(token)
			if token in StopList:
				continue
			QuEl.append( token )
print(QuEl, end='\n\n')
for e in QuEl:
	for i in Index:
		if i[0] == e:
			QuEl[QuEl.index(e)] = i[1:]
			break
	else:
		QuEl[QuEl.index(e)] = []
print(QuEl, end='\n\n')
Answer = []
for e in QuEl:
	for d in e:
		if d not in Answer:
			Answer.append(d)
Answer.sort()
print(Answer, end='\n\n')

#ranking
prox = 0.0
proxList = []
temp = Query.split( ' ' )
QuEl = []
for token in temp:
			token = token.lower()
			token = manipulate(token)
			if token in StopList:
				continue
			QuEl.append( token )
print(QuEl, end='\n\n')
for e in QuEl:
	for i in Index:
		if e == i[0]:
			break
	else:
		QuEl.remove( e )
print(QuEl, end='\n\n')
#caculating proximities
for d in Answer:
	for t in QuEl:
		for i in Index:
			if t == i[0] and d in i:
				prox += 1 / len(i[1:])
	proxList.append( [d, prox] )
	prox = 0.0
print( proxList, end='\n\n' )
#sorting
Answer = []
while len( proxList ) > 0:
	max = [0, 0]
	for d in proxList:
		if d[1] > max[1]:
			max = d
	Answer.append( DocID[max[0]] )
	proxList.remove( max )


#show list of results
ResulWindow = tk.Tk()
#for id in Answer:
#	ResultList.append(DocID[id])
ResultList = Answer
ResultShow( ResulWindow, ResultList )
print('Direction: {}\n\n'.format(ReqResDir))

#show requested result
#write to string
ReqResFile = open( ReqResDir, 'r' )
ReqResCon = ReqResFile.read()
print(ReqResCon)
#write to window
ChoosenResultWindow = tk.Tk()
ChoosenResultShow( ChoosenResultWindow, ReqResCon )