function getNeuralData(filePath)
    data = load(filePath);
    [~, name, ~] = fileparts(filePath);
    parentFolder = fullfile('.', name);

    if ~exist(parentFolder, 'dir')
        mkdir(parentFolder);
    end

    % Extract neural data for PMd
    processNeuralData(data.Data.neural_data_PMd, 'neural_data_PMd', parentFolder);

    % Check if the file is MM_S1.mat and contains neural_data_M1
    if strcmp(name, 'MM_S1') && isfield(data.Data, 'neural_data_M1')
        processNeuralData(data.Data.neural_data_M1, 'neural_data_M1', parentFolder);
    end

    disp('CSV files created for neural data.');
end

function processNeuralData(neuralData, folderName, parentFolder)
    outputFolder = fullfile(parentFolder, folderName);
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    numReaches = numel(neuralData);
    for i = 1:numReaches
        reachData = neuralData{i};
        filename = fullfile(outputFolder, sprintf('%s_reach%d.csv', folderName, i));
        
        % Determine the size of the data
        numNeurons = size(reachData, 1);
        timeBins = size(reachData, 2);
        
        % Create variable names and format the data into a table
        variableNames = arrayfun(@(x) sprintf('Neuron%d', x), 1:numNeurons, 'UniformOutput', false);
        reachTable = array2table(reachData', 'VariableNames', variableNames);
        reachTable.TimeBin = (1:timeBins)';
        
        % Move TimeBin column to the beginning
        reachTable = [reachTable(:, end), reachTable(:, 1:end-1)];
        
        % Write to CSV
        writetable(reachTable, filename);
    end
end
