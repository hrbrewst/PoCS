import re 

def ACCESSING():
#Paths to files containing novels
	paths = { "pride":"/Users/haleybrewster/Desktop/PoCS_2/pride_prejudice.txt" , frank":"/Users/haleybrewster/Desktop/PoCS_2/frankenstein.txt",
		"moby":"/Users/haleybrewster/Desktop/PoCS_2/moby_dick.txt" , "les_mis":"/Users/haleybrewster/Desktop/PoCS_2/les_mis.txt"}

	books = {}
# since paths is a tuple (contains two items per token in our case name and path) we use a comma in the for loop to iterate through both.
	for name,path in paths:
		with open(path , "r", encoding="utf-8") as f:
			books[name] = f.read()
	return books

def CROPPING(books):
	cropped_text = []
	for i in books:
		start = i.find("*** START OF THE PROJECT GUTENBERG EBOOK")
		end = i.find("*** END OF THE PROJECT GUTENBERG EBOOK")
		if start != -1:
			raw = i[start:]
		if end != -1:
			raw = raw[:end]
		cropped_text.append(raw)
	return cropped_text



# Example usage:
books = ACCESSING()
cropped_books = CROPPING(books)

# Peek at one:
print(cropped_books[frank][:300])

