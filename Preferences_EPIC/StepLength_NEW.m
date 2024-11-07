clc;
clear;
close all;

% Define base path
base_path = '/Users/katiepeterka/Downloads/HipExoLab';

% Define subjects and conditions in the specified order
subjects = {'IRLHEAB05'}; % Add 'IRLHEAB06' if needed
conditions = {'S2D3', 'S1D5', 'S1D3', 'S2D4', 'S2D5', 'S2D2', 'S1D0', ...
              'S2D0', 'S1D1', 'S1D2', 'S1D4', 'S2D1', 'S0D0'};

% Set Vicon camera frequency (e.g., 100 Hz)
cf_vicon = 100;

% Initialize structure to hold data tables and right step lengths
dataTables = struct();
avgRightStepLengths = zeros(1, length(conditions)); % To store average right step length for each condition

% Loop through each subject and condition
for i = 1:length(subjects)
    subject = subjects{i};
    
    for j = 1:length(conditions)
        condition = conditions{j};
        
        % Define .trc and .mot file paths
        trc_file = fullfile(base_path, sprintf('%s_V1_TM_LG_%s_t1_filled.trc', subject, condition));
        mot_file = fullfile(base_path, sprintf('%s_V1_TM_LG_%s_t1_filled_FP.mot', subject, condition));
        
        % Load and process the .trc file if it exists
        if isfile(trc_file)
            trc_data = readtable(trc_file, 'FileType', 'text', 'VariableNamingRule', 'preserve');
            trc_data = redefineHeaders(trc_data);
            dataTables.(subject).(condition).trc = trc_data;
        else
            fprintf('File not found: %s\n', trc_file);
            continue;
        end
        
        % Load and process the .mot file if it exists
        if isfile(mot_file)
            mot_data = readtable(mot_file, 'FileType', 'text', 'VariableNamingRule', 'preserve');
            dataTables.(subject).(condition).mot = mot_data;
            
            % Detect heel strikes and get heelStrikeTable for the current condition
            heelStrikeTable = detectHeelStrikes(mot_data);
            dataTables.(subject).(condition).heelStrikeTable = heelStrikeTable;
            
            % Calculate step lengths and other metrics
            [l_step_length, r_step_length, l_step_dur, r_step_dur, stride_length, stride_dur, len_asym, dur_asym] = ...
                calculateStepLength_NEW(trc_data, heelStrikeTable, cf_vicon);
            
            % Store calculated parameters
            dataTables.(subject).(condition).l_step_length = l_step_length;
            dataTables.(subject).(condition).r_step_length = r_step_length;
            dataTables.(subject).(condition).l_step_dur = l_step_dur;
            dataTables.(subject).(condition).r_step_dur = r_step_dur;
            dataTables.(subject).(condition).stride_length = stride_length;
            dataTables.(subject).(condition).stride_dur = stride_dur;
            dataTables.(subject).(condition).len_asym = len_asym;
            dataTables.(subject).(condition).dur_asym = dur_asym;
            
            % Calculate and store the average right step length for the condition
            avgRightStepLengths(j) = mean(r_step_length, 'omitnan');
        else
            fprintf('File not found: %s\n', mot_file);
        end
    end
end

% Plot the average right step length for each condition in specified order
figure;
for j = 1:length(conditions)
    subplot(3, 5, j); % Arrange subplots in a 3x5 grid
    bar(avgRightStepLengths(j));
    title(conditions{j});
    ylabel('Average Right Step Length');
    ylim([0 max(avgRightStepLengths) + 10]); % Adjust y-axis limit for readability
    xticks([]); % Remove x-ticks as each bar represents a condition
end
sgtitle('Average Right Step Length for Each Condition (Preference Order)'); % Super title for all subplots
