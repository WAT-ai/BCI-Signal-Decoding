function GetKinematicData(filePath)
    % Load the .mat file
    data = load(filePath);
    kinematicsData = data.Data.kinematics;

    [~, name, ~] = fileparts(filePath);
    parentFolder = fullfile('.', name);

    if ~exist(parentFolder, 'dir')
        mkdir(parentFolder);
    end

    % Define the column headers
    headers = {'x_position', 'y_position', 'x_velocity', 'y_velocity', ...
               'x_acceleration', 'y_acceleration', 'time_stamps'};

    % Create the folder if it doesn't exist
    outputFolder = fullfile(parentFolder, 'kinematic_data');
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    % Loop through each reach and save it as a CSV file
    numReaches = numel(kinematicsData);
    for i = 1:numReaches
        reachData = kinematicsData{i};
        filename = fullfile(outputFolder, sprintf('reach%d.csv', i));
        reachTable = array2table(reachData, 'VariableNames', headers);
        writetable(reachTable, filename);
    end
    disp('CSV files created for kinematics data.');
end
