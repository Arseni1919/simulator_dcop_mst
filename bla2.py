import pickle


# graphs = {'DSA': [1,2,3,4]}
# # Save the results
# file_Name = "testfile"
# # open the file for writing
# with open(file_Name, 'wb') as fileObject:
#     # this writes the object a to the file named 'testfile'
#     pickle.dump(graphs, fileObject)

file_Name = "testfile"
fileObject = open(file_Name,'rb')
# load the object from the file into var b
b = pickle.load(fileObject)
print(b)