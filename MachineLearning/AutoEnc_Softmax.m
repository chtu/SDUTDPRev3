%This code trains an autoencoder to solve classification problem. 
%There are four matrixes: Xtrain, Ytrain, Xtest, Ytest
%Xtrain: training set of features. Each column contains the features for a
%training sample. The number of rows is equal to the number of features. 
%The number of columns is equal to the number of training samples. 
%Ytrain: training set of labels. In each column a single element will be 1 
%to indicate the class that this sample belongs to, and all other elements 
%in the column will be 0. The number of rows is equal to the total number of
%classes, and the number of columns is equal to the number of training
%samples. 
%Xtest: testing set of features. The definitions of row and column are the
%same as those for Xtrain. 
%Ytest: testing set of labels. The definitions of row and column are the
%same as those for Ytrain. 

%More info: https://www.mathworks.com/help/deeplearning/examples/train-stacked-autoencoders-for-image-classification.html;jsessionid=e2c6b437d7419978da9412d0b897
Atrain = table2array(readtable('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/ProcessedData/trainVectorsProcessed.csv'));
Btrain = table2array(readtable('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/ProcessedData/trainLabelsProcessed.csv'));
Atest = table2array(readtable('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/ProcessedData/testVectorsProcessed.csv'));
Btest = table2array(readtable('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/ProcessedData/testLabelsProcessed.csv'));
%aTableT = array2table(aTableArray.');

Xtrain = Atrain.';
Ytrain = Btrain.';
Xtest = Atest.';
Ytest = Btest.';


rng('default')
hiddenSize = 5; %this value should be smaller than the input size (i.e., 
% number of features)

autoenc = trainAutoencoder(Xtrain,hiddenSize, ...
    'MaxEpochs',400, ...
    'L2WeightRegularization',0.004, ...
    'SparsityRegularization',4, ...
    'SparsityProportion',0.15, ...
    'ScaleData', true);

feat = encode(autoenc,Xtrain);

softnet = trainSoftmaxLayer(feat,Ytrain,'MaxEpochs',400,'LossFunction','mse');

stackednet = stack(autoenc,softnet);
stackednet = train(stackednet,Xtrain,Ytrain);

Pred = stackednet(Xtest);
figure(1) %the second figure shows the confusionmatrix of the testing data
plotconfusion(Ytest,Pred);
