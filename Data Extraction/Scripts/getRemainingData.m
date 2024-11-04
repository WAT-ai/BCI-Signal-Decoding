function getRemainingData(filePath)
    data = load(filePath);

    [~, name, ~] = fileparts(filePath);
    parentFolder = fullfile('.', name);

    if ~exist(parentFolder, 'dir')
        mkdir(parentFolder);
    end

    baseFolder = parentFolder;  % Placeholder path
    dataTypes = {'trial_num', 'reach_num', 'reach_st', 'cue_on', 'reach_end', ...
                 'reach_pos_st', 'reach_pos_end', 'reach_dir', 'reach_len', ...
                 'target_on', 'time_window'};

    for i = 1:length(dataTypes)
        dataTypeFolder = fullfile(parentFolder, dataTypes{i});
        if ~exist(dataTypeFolder, 'dir')
            mkdir(dataTypeFolder);
        end
    end

    numReaches = numel(data.Data.trial_num);
    for reachIndex = 1:numReaches
        % Extract each data type and write to CSV files
        writetable(array2table(data.Data.trial_num{reachIndex}, 'VariableNames', {'TrialNumber'}), ...
            fullfile(baseFolder, 'trial_num', sprintf('trial_num_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.reach_num{reachIndex}, 'VariableNames', {'ReachNumber'}), ...
            fullfile(baseFolder, 'reach_num', sprintf('reach_num_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.reach_st{reachIndex}, 'VariableNames', {'ReachStartTime'}), ...
            fullfile(baseFolder, 'reach_st', sprintf('reach_st_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.cue_on{reachIndex}, 'VariableNames', {'CueOnTime'}), ...
            fullfile(baseFolder, 'cue_on', sprintf('cue_on_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.reach_end{reachIndex}, 'VariableNames', {'ReachEndTime'}), ...
            fullfile(baseFolder, 'reach_end', sprintf('reach_end_reach%d.csv', reachIndex)));
        
        reach_pos_st_table = array2table(data.Data.reach_pos_st{reachIndex}, 'VariableNames', {'StartPositionX', 'StartPositionY'});
        writetable(reach_pos_st_table, ...
            fullfile(baseFolder, 'reach_pos_st', sprintf('reach_pos_st_reach%d.csv', reachIndex)));
        
        reach_pos_end_table = array2table(data.Data.reach_pos_end{reachIndex}, 'VariableNames', {'EndPositionX', 'EndPositionY'});
        writetable(reach_pos_end_table, ...
            fullfile(baseFolder, 'reach_pos_end', sprintf('reach_pos_end_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.reach_dir{reachIndex}, 'VariableNames', {'ReachDirection'}), ...
            fullfile(baseFolder, 'reach_dir', sprintf('reach_dir_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.reach_len{reachIndex}, 'VariableNames', {'ReachLength'}), ...
            fullfile(baseFolder, 'reach_len', sprintf('reach_len_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.target_on{reachIndex}, 'VariableNames', {'TargetOn'}), ...
            fullfile(baseFolder, 'target_on', sprintf('target_on_reach%d.csv', reachIndex)));
        
        writetable(array2table(data.Data.time_window{reachIndex}, 'VariableNames', {'TimeWindow'}), ...
            fullfile(baseFolder, 'time_window', sprintf('time_window_reach%d.csv', reachIndex)));
    end
    disp('CSV files created for other data types and reaches.');
end
