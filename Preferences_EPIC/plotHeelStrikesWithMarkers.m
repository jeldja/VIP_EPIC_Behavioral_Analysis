function plotHeelStrikesWithMarkers(trc_data, heelStrikeTable)
    % Extract data from trc_data
    trcTime = trc_data.Time_X;
    RCAL_Z = trc_data.RCAL_Z;
    LCAL_Z = trc_data.LCAL_Z;

    % Extract heel strike times from heelStrikeTable
    rightHeelStrikeTimes = heelStrikeTable.RightHeelStrikeTime;
    leftHeelStrikeTimes = heelStrikeTable.LeftHeelStrikeTime;

    % Create the figure
    figure;

    % Plot RCAL_Z with right heel strike markers
    subplot(2, 1, 1);
    plot(trcTime, RCAL_Z, 'b-');  % Plot RCAL_Z data in blue
    hold on;
    % Plot markers for right heel strikes
    rightHeelIndices = arrayfun(@(t) findClosestIndex(trcTime, t), rightHeelStrikeTimes, 'UniformOutput', false);
    rightHeelIndices = cell2mat(rightHeelIndices(~cellfun('isempty', rightHeelIndices)));
    plot(trcTime(rightHeelIndices), RCAL_Z(rightHeelIndices), 'ro', 'MarkerFaceColor', 'r');  % Red circles for right heel strikes
    title('Right Heel Z-Position (RCAL\_Z) with Heel Strike Markers');
    xlabel('Time (s)');
    ylabel('RCAL\_Z Position');
    grid on;
    hold off;

    % Plot LCAL_Z with left heel strike markers
    subplot(2, 1, 2);
    plot(trcTime, LCAL_Z, 'r-');  % Plot LCAL_Z data in red
    hold on;
    % Plot markers for left heel strikes
    leftHeelIndices = arrayfun(@(t) findClosestIndex(trcTime, t), leftHeelStrikeTimes, 'UniformOutput', false);
    leftHeelIndices = cell2mat(leftHeelIndices(~cellfun('isempty', leftHeelIndices)));
    plot(trcTime(leftHeelIndices), LCAL_Z(leftHeelIndices), 'bo', 'MarkerFaceColor', 'b');  % Blue circles for left heel strikes
    title('Left Heel Z-Position (LCAL\_Z) with Heel Strike Markers');
    xlabel('Time (s)');
    ylabel('LCAL\_Z Position');
    grid on;
    hold off;
end

% Helper function to find the closest index
function idx = findClosestIndex(timeArray, targetTime)
    [~, idx] = min(abs(timeArray - targetTime));
    if isempty(idx) || isnan(targetTime)
        idx = [];
    end
end
