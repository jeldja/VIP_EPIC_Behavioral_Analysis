function [l_step_length, r_step_length, l_step_dur, r_step_dur, stride_length, stride_dur, len_asym, dur_asym] = calculateStepLength_NEW(trc_data, heelStrikeTable, cf_vicon)
    % Extract necessary columns from trc_data
    trcTime = trc_data.Time_X;
    RCAL_Z = trc_data.RCAL_Z;
    LCAL_Z = trc_data.LCAL_Z;

    % Extract heel strike times from heelStrikeTable
    rightHeelStrikeTimes = heelStrikeTable.RightHeelStrikeTime;
    leftHeelStrikeTimes = heelStrikeTable.LeftHeelStrikeTime;

    % Find indices in trc_data that correspond to heel strike times, removing NaNs
    lhs_indices = arrayfun(@(t) findClosestIndex(trcTime, t), leftHeelStrikeTimes);
    rhs_indices = arrayfun(@(t) findClosestIndex(trcTime, t), rightHeelStrikeTimes);
    lhs_indices = lhs_indices(~isnan(lhs_indices));
    rhs_indices = rhs_indices(~isnan(rhs_indices));

    % Ensure there is an equal number of indices for left and right strikes
    min_length = min(length(lhs_indices), length(rhs_indices)) - 1;

    % Initialize arrays for output
    l_step_length = zeros(1, min_length);
    r_step_length = zeros(1, min_length);
    l_step_dur = zeros(1, min_length);
    r_step_dur = zeros(1, min_length);
    stride_length = zeros(1, min_length);
    stride_dur = zeros(1, min_length);
    len_asym = zeros(1, min_length);
    dur_asym = zeros(1, min_length);

    % Loop to calculate step lengths, durations, and asymmetries
    for k = 1:min_length
        % Ensure indices are within bounds
        if k <= length(lhs_indices) && k <= length(rhs_indices) && k + 1 <= length(rhs_indices)
            % Calculate left step length and duration (left heel to right heel)
            l_step_length(k) = abs(LCAL_Z(lhs_indices(k)) - RCAL_Z(lhs_indices(k)));
            l_step_dur(k) = (trcTime(lhs_indices(k)) - trcTime(rhs_indices(k))) / cf_vicon;

            % Calculate right step length and duration (right heel to left heel)
            r_step_length(k) = abs(RCAL_Z(rhs_indices(k + 1)) - LCAL_Z(rhs_indices(k + 1)));
            r_step_dur(k) = (trcTime(rhs_indices(k + 1)) - trcTime(lhs_indices(k))) / cf_vicon;

            % Calculate stride length and duration
            stride_length(k) = l_step_length(k) + r_step_length(k);
            stride_dur(k) = l_step_dur(k) + r_step_dur(k);

            % Calculate asymmetry in length and duration
            len_asym(k) = l_step_length(k) / (l_step_length(k) + r_step_length(k));
            dur_asym(k) = l_step_dur(k) / (l_step_dur(k) + r_step_dur(k));
        end
    end

    % Display the calculated values for debugging
    disp('Left Step Lengths:'); disp(l_step_length);
    disp('Right Step Lengths:'); disp(r_step_length);
    disp('Left Step Durations:'); disp(l_step_dur);
    disp('Right Step Durations:'); disp(r_step_dur);
    disp('Stride Lengths:'); disp(stride_length);
    disp('Stride Durations:'); disp(stride_dur);
    disp('Length Asymmetries:'); disp(len_asym);
    disp('Duration Asymmetries:'); disp(dur_asym);
end

% Helper function to find the closest index
function idx = findClosestIndex(timeArray, targetTime)
    [~, idx] = min(abs(timeArray - targetTime));
    if isempty(idx) || isnan(targetTime)
        idx = NaN;
    end
end
