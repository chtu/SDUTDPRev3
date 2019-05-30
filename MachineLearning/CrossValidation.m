all_bins = [1;2;3;4;5;];
threshold = 0.1;
ResultMatrix = zeros(4,9);
while threshold <= 0.9
    totalAccuracy = 0;
    totalPrecision = 0;
    totalRecall = 0;
    for n = 1:5
        accuracy = 0;
        precision = 0;
        recall = 0;
        testVector = table2array(readtable(append('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/Set2/bins/VectorBin',int2str(n),'.csv')));
        testLabel = table2array(readtable(append('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/Set2/bins/LabelBin',int2str(n),'.csv')));

        train_bins = all_bins(all_bins~=n);
        trainVector = [];
        trainLabel = [];
        for k1 = 1:length(train_bins)
            trainVector = [trainVector; table2array(readtable(append('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/Set2/bins/VectorBin',int2str(train_bins(k1)),'.csv')))];
            trainLabel = [trainLabel; table2array(readtable(append('/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/MachineLearning/Set2/bins/LabelBin',int2str(train_bins(k1)),'.csv')))];
        end

        Xtest = testVector.';
        Ytest = testLabel.';
        Xtrain = trainVector.';
        Ytrain = trainLabel.';
        Xtest(1,:) = [];
        Ytest(1,:) = [];
        Xtrain(1,:) = [];
        Ytrain(1,:) = [];
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
        for i = 1:2
            for j = 1:89
                if Pred(i,j) <= threshold
                    Pred(i,j) = 0;
                else 
                    Pred(i,j) = 1;
                end
            end
        end
        TP=0;FP=0;TN=0;FN=0;

        for j=1:89
          if(Pred(1,j)==1 && Ytest(1,j)==1)
              TP=TP+1;
          elseif(Pred(1,j)==0 && Ytest(1,j)==1)
              FP=FP+1;
          elseif(Pred(1,j)==0 && Ytest(1,j)==0)
              TN=TN+1;
          else
              FN=FN+1;
          end
        end
        accuracy = (TP+TN)/(TP+TN+FP+FN);
        precision = TP/(TP+FP);
        recall = TP/(TP+FN);
        totalAccuracy = totalAccuracy + accuracy;
        totalPrecision = totalPrecision + precision;
        totalRecall = totalRecall + recall;
    end
    avgAccuracy = totalAccuracy/5;
    avgPrecision = totalPrecision/5;
    avgRecall = totalRecall/5;
    disp(threshold*10)
    ResultMatrix(1,round(threshold*10)) = threshold;
    ResultMatrix(2,round(threshold*10)) = avgAccuracy;
    ResultMatrix(3,round(threshold*10)) = avgPrecision;
    ResultMatrix(4,round(threshold*10)) = avgRecall;
    threshold = threshold + 0.1;
end