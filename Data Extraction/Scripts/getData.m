function getDataFromMat(filePath)
    % Call each extraction function
    GetKinematicData(filePath);
    getNeuralData(filePath);
    getTimestamps(filePath);
    getRemainingData(filePath);
    getBlockInfo(filePath);
    
    fprintf('All data extraction processes completed successfully. For File %s\n', filePath);
end

getDataFromMat('MT_S1.mat');
getDataFromMat('MT_S2.mat');
getDataFromMat('MT_S3.mat');
getDataFromMat('MM_S1.mat');

