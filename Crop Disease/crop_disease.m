clc;
clear all
close all
% %OUTLOOK Configuration
% outlook = actxserver('outlook.Application');
% mapi=outlook.GetNamespace('mapi');
% INBOX=mapi.GetDefaultFolder(6);
% 
% %%%% Retrieving last email
% count = INBOX.Items.Count; 
% firstemail=INBOX.Items.Item(count); 
% subject = firstemail.get('Subject');
% body = firstemail.get('Body');
% 
% %%%% Saving attachments to current directory
% attachments = firstemail.get('Attachments');
% if attachments.Count >=1
%     fname = attachments.Item(1).Filename;
%     dir = pwd;
%     full = [pwd,'\',fname];
%     attachments.Item(1).SaveAsFile(full)
% end
image=imread('7.jpg');

image=imresize(image,[64 64]);
matlabroot='D:\Crop Diseases\code';
digitDatasetPath = fullfile(matlabroot,'Database1');
imds = imageDatastore(digitDatasetPath, ...
    'IncludeSubfolders',true,'LabelSource','foldernames');
layers = [imageInputLayer([64 64 3])
    
    convolution2dLayer(5,20);
          reluLayer
          maxPooling2dLayer(2,'Stride',2);
         convolution2dLayer(5,20);
         reluLayer
          maxPooling2dLayer(2,'Stride',2);
          fullyConnectedLayer(5);
          softmaxLayer
          classificationLayer()];

options = trainingOptions('sgdm', 'MaxEpochs', 40,'Plots', 'training-progress', 'initialLearnRate',0.0001);
imageSize = layers(1).InputSize;
augmentedTrainingSet = augmentedImageDatastore(imageSize, imds);
%convnet = trainNetwork(augmentedTrainingSet,layers,options);
load network;
YPred = classify(convnet,image);
output=char(YPred);
msgbox(output);
if strcmp(output,'Cercospora leaf spot- Watermelon')
    msgbox('Crop rotation, incorporation of old crop residue into the soil and crop rotation with non-cucurbit crops for three years are effective in limiting carryover of the pathogen.')
elseif strcmp(output,'BrownSpot')
    msgbox('The use of resistant varieties is the most economical means of control. Growing Resistant varieties like ADT 44,PY 4,CORH 1,CO 44,CAUVERY,BHAVANI,TPS 4 and Dhanu.')
elseif strcmp(output,'Hispa')
    msgbox('Avoid over fertilizing the field. Close plant spacing results in greater leaf densities that can tolerate higher hispa numbers.')
elseif strcmp(output,'LeafBlast')
    msgbox('Systemic fungicides like triazoles and strobilurins can be used judiciously for control to control blast.')
else
    msgbox('Switch to a balanced fertilizer, such as a 10-10-10, and only apply it in the fall, after the smut pathogen is dormant. Keeping your plants healthy will help them resist a smut infection, but if the disease is very severe in valuable plants, you may consider applying a fungicide.')
end