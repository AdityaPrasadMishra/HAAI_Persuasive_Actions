from sklearn import tree
from sklearn.metrics import accuracy_score
import sys



TEST_FILE = "../DATA_2/TEST_SET"
TRAIN_FILE = "../DATA_2/TRAIN_SET"

with open(TRAIN_FILE) as t_fd:
     full_train_data = [i.strip().split(' ') for i in t_fd.readlines()]

with open(TEST_FILE) as t_fd:
     full_test_data = [i.strip().split(' ') for i in t_fd.readlines()]


data = []
labels = []
test_data = []
test_labels = []

for it in full_train_data:
   tmp_list = []
   for i in it[:-1]:
      tmp_list.append(int(i))
   data.append(tmp_list)
   labels.append(it[-1])

for it in full_test_data:
   tmp_list = []
   for i in it[:-1]:
      tmp_list.append(int(i))
   test_data.append(tmp_list)
   test_labels.append(it[-1])




clf = tree.DecisionTreeClassifier()
clf = clf.fit(data, labels)
print (clf.score(data, labels))

predicted_labels = []
for it in test_data:
    predicted_labels.append(clf.predict([it])[0])
#for i in range(len(test_data)):
#    print ("predicted labels",test_data[i],predicted_labels[i],test_labels[i])

print "acc score",accuracy_score(test_labels, predicted_labels)


#print("plan_length",plan_length)


