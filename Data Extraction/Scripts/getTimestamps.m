function getTimestamps(filePath)
    data = load(filePath);
    timestampsData = data.Data.timestamps;

    [~, name, ~] = fileparts(filePath);
    parentFolder = fullfile('.', name);

    if ~exist(parentFolder, 'dir')
        mkdir(parentFolder);
    end

    outputFolder = fullfile(parentFolder, 'timestamps_data');
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    numReaches = numel(timestampsData);
    for i = 1:numReaches
        reachTimestamps = timestampsData{i};
        filename = fullfile(outputFolder, sprintf('timestamps_reach%d.csv', i));
        reachTable = array2table(reachTimestamps, 'VariableNames', {'TimeStamp'});
        writetable(reachTable, filename);
    end
    disp('CSV files created for timestamps data.');
end
