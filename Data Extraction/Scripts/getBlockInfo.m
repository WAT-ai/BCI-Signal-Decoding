function getBlockInfo(filePath)
    data = load(filePath);
    block_info = data.Data.block_info;
    block_info_table = array2table(block_info);

    block_info_table.Properties.VariableNames = { ...
        'TrialStartTime', 'Target1AppearanceTime', 'Target1MovementOnsetTime', ...
        'Target1PeakVelocityTime', 'Target1XLocation', 'Target1YLocation', ...
        'Target2AppearanceTime', 'Target2MovementOnsetTime', 'Target2PeakVelocityTime', ...
        'Target2XLocation', 'Target2YLocation', 'Target3AppearanceTime', ...
        'Target3MovementOnsetTime', 'Target3PeakVelocityTime', 'Target3XLocation', ...
        'Target3YLocation', 'Target4AppearanceTime', 'Target4MovementOnsetTime', ...
        'Target4PeakVelocityTime', 'Target4XLocation', 'Target4YLocation', ...
        'TrialEndTime', 'TrialResult' ...
    };

    [~, name, ~] = fileparts(filePath);
    parentFolder = fullfile('.', name);

    if ~exist(parentFolder, 'dir')
        mkdir(parentFolder);
    end

    blockInfoFolder = fullfile(parentFolder, 'block_info');

    if ~exist(blockInfoFolder, 'dir')
        mkdir(blockInfoFolder);
    end
    writetable(block_info_table, fullfile(blockInfoFolder, 'block_info.csv'));
    disp('CSV file created for block_info with specified column names.');
end
