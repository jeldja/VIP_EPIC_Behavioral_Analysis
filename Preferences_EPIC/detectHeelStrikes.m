function heelStrikeTable = detectHeelStrikes(mot_data)
    % Extract headers from the data
    headers = mot_data.Properties.VariableNames;

    % Find the indices for 'time', 'FPR_vy', and 'FPL_vy'
    timeIndex = find(strcmp(headers, 'time'));
    FPR_vyIndex = find(strcmp(headers, 'FPR_vy'));
    FPL_vyIndex = find(strcmp(headers, 'FPL_vy'));

    % Check if the indices are valid
    if isempty(timeIndex) || isempty(FPR_vyIndex) || isempty(FPL_vyIndex)
        error('Could not find the required columns "time", "FPR_vy", or "FPL_vy" in the header');
    end

    % Extract the 'time', 'FPR_vy', and 'FPL_vy' columns
    time = mot_data{:, timeIndex};
    FPR_vy = mot_data{:, FPR_vyIndex};
    FPL_vy = mot_data{:, FPL_vyIndex};

    % Initialize arrays to store the heel strike times for right and left feet
    rightHeelStrikeTimes = [];
    leftHeelStrikeTimes = [];

    % Detect right heel strikes
    for i = 2:length(FPR_vy)
        if FPR_vy(i-1) == 0 && FPR_vy(i) > 0
            rightHeelStrikeTimes = [rightHeelStrikeTimes; time(i)];
        end
    end

    % Detect left heel strikes
    for i = 2:length(FPL_vy)
        if FPL_vy(i-1) == 0 && FPL_vy(i) > 0
            leftHeelStrikeTimes = [leftHeelStrikeTimes; time(i)];
        end
    end

    % Ensure both arrays have the same length by padding with NaNs
    maxLength = max(length(rightHeelStrikeTimes), length(leftHeelStrikeTimes));
    rightHeelStrikeTimes = [rightHeelStrikeTimes; NaN(maxLength - length(rightHeelStrikeTimes), 1)];
    leftHeelStrikeTimes = [leftHeelStrikeTimes; NaN(maxLength - length(leftHeelStrikeTimes), 1)];

    % Calculate time between consecutive heel strikes
    timeBetweenRightStrikes = [NaN; diff(rightHeelStrikeTimes)];
    timeBetweenLeftStrikes = [NaN; diff(leftHeelStrikeTimes)];

    % Calculate the average time between heel strikes
    avgTimeBetweenRightStrikes = mean(timeBetweenRightStrikes(~isnan(timeBetweenRightStrikes)));
    avgTimeBetweenLeftStrikes = mean(timeBetweenLeftStrikes(~isnan(timeBetweenLeftStrikes)));

    % Set threshold for identifying outliers
    thresholdRight = 1.5 * avgTimeBetweenRightStrikes;
    thresholdLeft = 1.5 * avgTimeBetweenLeftStrikes;

    % Identify outliers
    outliersRight = find(timeBetweenRightStrikes > thresholdRight) - 1;
    outliersLeft = find(timeBetweenLeftStrikes > thresholdLeft) - 1;

    % Create heel strike table
    heelStrikeTable = table(rightHeelStrikeTimes, timeBetweenRightStrikes, ...
                            leftHeelStrikeTimes, timeBetweenLeftStrikes, ...
                            'VariableNames', {'RightHeelStrikeTime', 'TimeBetweenRightStrikes', ...
                                              'LeftHeelStrikeTime', 'TimeBetweenLeftStrikes'});

    % Remove outliers and adjust heel strikes
    for i = 1:length(outliersRight)
        nextLeftIndex = find(leftHeelStrikeTimes > rightHeelStrikeTimes(outliersRight(i)), 1);
        if ~isempty(nextLeftIndex)
            heelStrikeTable.LeftHeelStrikeTime(nextLeftIndex) = NaN;
        end
        heelStrikeTable.RightHeelStrikeTime(outliersRight(i)) = NaN;
    end

    for i = 1:length(outliersLeft)
        nextRightIndex = find(rightHeelStrikeTimes > leftHeelStrikeTimes(outliersLeft(i)), 1);
        if ~isempty(nextRightIndex)
            heelStrikeTable.RightHeelStrikeTime(nextRightIndex) = NaN;
        end
        heelStrikeTable.LeftHeelStrikeTime(outliersLeft(i)) = NaN;
    end

    % Plot the heel strikes
    figure;
    subplot(2,1,1); % Right foot plot
    plot(time, FPR_vy);
    hold on;
    plot(heelStrikeTable.RightHeelStrikeTime, zeros(size(heelStrikeTable.RightHeelStrikeTime)), 'ro');
    xlabel('Time');
    ylabel('FPR_vy');
    title('Cleaned Right Foot Heel Strikes');
    grid on;
    hold off;

    subplot(2,1,2); % Left foot plot
    plot(time, FPL_vy);
    hold on;
    plot(heelStrikeTable.LeftHeelStrikeTime, zeros(size(heelStrikeTable.LeftHeelStrikeTime)), 'ro');
    xlabel('Time');
    ylabel('FPL_vy');
    title('Cleaned Left Foot Heel Strikes');
    grid on;
    hold off;
end
