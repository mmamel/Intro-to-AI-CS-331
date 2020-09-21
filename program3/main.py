import os
import string
import re
import copy
import math

vocab = {}

###################
#  Preprocessing  #
###################
#clean training text
training = open("trainingSet.txt", "r")
trainingText = training.read()
trainingText = re.sub(r'[^A-Za-z\s0-1]','',trainingText)
trainingText = trainingText.lower()
trainingList = re.sub(r'[0-1]','',trainingText).split()
trainingSentence = trainingText.split('\n')

#clean testing text
testing = open("testSet.txt","r")
testingText = testing.read()
testingSentence = re.sub(r'[^A-Za-z\s0-1]','',testingText).lower().split('\n')

#create dictionary to store unique words
for word in trainingList:
    if word in vocab:
        vocab[word] += 1
    else:
        vocab.update({word: 1})
training.close()
feature_string = []

#create list of feature words
for word in sorted(vocab):
    feature_string.append(word)
feature_string.append('classlabel')

#output training vectors
trainingOutput = open("preprocessed_training.txt", "a")
trainingOutput.write(','.join(feature_string))
trainingOutput.write('\n')

#initialize empty classifier
true_classifier = vocab.fromkeys(vocab, 0)
false_classifier = vocab.fromkeys(vocab, 0)
num_true = 0
num_false=0
boo = 0
clean_feature=vocab.fromkeys(vocab,0)
# classifier_matrix = [0 for x in range(len(true_classifier))]
# training_matrix = [[0 for x in range(len(true_classifier))] for y in range(len(trainingSentence)-1)]
#get feature vector for each sentence
for sentence in trainingSentence:
    if len(sentence) > 0:
        classi = '1'
        sentence = sentence.split()
        if(sentence[len(sentence)-1]=='0'):
            classi = '0'
            num_false+=1
        else:
            num_true+=1
        feature= clean_feature.copy()
        for word in sentence:
            if word in feature:
                if feature[word] == 0:
                    feature[word]+=1
                    #learn parameters
                    if classi == '0':
                        false_classifier[word]+=1
                    else:
                        true_classifier[word]+=1
        temp = ''
        #output parameters to preprocesed_training.txt
        for key, value in sorted(feature.items()):
            temp+=str(value)+','
        trainingOutput.write(str(temp))
        temp = classi + '\n'
        trainingOutput.write(temp)

#same but for preprocessed_test.txt
testing_matrix = [[0 for x in range(len(true_classifier))] for y in range(len(testingSentence)-1)]
clean_feature=vocab.fromkeys(vocab, 0)
testingOutput = open("preprocessed_test.txt", "a")
testingOutput.write(','.join(feature_string))
for sentence in testingSentence:
    if len(sentence)>0:
        classi = '1'
        sentence = sentence.split()
        if(sentence[len(sentence)-1]=='0'):
            classi = '0'
        feature= clean_feature.copy()
        # feature = clean_feature
        for word in sentence:
            if word in feature:
                if feature[word] == 0:
                    feature[word]+=1
        temp = ''
        for key in sorted(list(feature.values())):
            temp+= str(key)+','
        temp += classi + '\n'
        testingOutput.write(temp)

####################
#  Classification  #
####################

#test on trainingSet.txt
results = open("results.txt","a")
correct = 0
for sentence in trainingSentence:
    true_product = 0
    false_product = 0
    guess = 0
    if len(sentence) > 0:
        classi = 1
        sentence = sentence.split()
        if(sentence[len(sentence)-1]=='0'):
            classi = 0
        for word in sentence:
            #P(X=ui | Y=v)
            if word != '0' and word != '1':
                if word in true_classifier:
                    numerator = true_classifier[word] + 1
                    denominator = num_true + 2
                    true_product += math.log(numerator/denominator)

                if word in false_classifier:
                    numerator = false_classifier[word]+1
                    denominator = num_false + 2
                    false_product += math.log(numerator / denominator)

        true_product += math.log(num_true/(num_true+num_false))
        false_product += math.log(num_false/(num_true+num_false))
        #argmax
        if true_product > false_product:
            guess = 1
        if guess == classi:
            correct += 1
print("Accuracy = ", correct / (len(trainingSentence)-1))
results_str = "Accuracy = " + str(correct/(len(trainingSentence)-1)) + "\nTraining: trainingSet.txt Testing: trainingSet.txt\n"
results.write(results_str)
correct = 0
for sentence in testingSentence:
    true_product = 0
    false_product = 0
    guess = 0
    if len(sentence) > 0:
        classi = 1
        sentence = sentence.split()
        if(sentence[len(sentence)-1]=='0'):
            classi = 0
        for word in sentence:
            if word != '0' and word != '1':
                if word in true_classifier:
                    numerator = true_classifier[word] + 1
                    denominator = num_true + 2
                    true_product += math.log(numerator/denominator)
                if word in false_classifier:
                    numerator = false_classifier[word]+1
                    denominator = num_false + 2
                    false_product += math.log(numerator / denominator)
        true_product += math.log(num_true/(num_true+num_false))
        false_product += math.log(num_false/(num_true+num_false))

        if true_product > false_product:
            guess = 1

        if guess == classi:
            correct += 1

print("Accuracy = ", correct / (len(testingSentence)-1))
results_str = "Accuracy = " + str(correct/(len(trainingSentence)-1)) + "\nTraining: trainingSet.txt Testing: testSet.txt\n"
results.write(results_str)
trainingOutput.close()
testingOutput.close()
results.close()

