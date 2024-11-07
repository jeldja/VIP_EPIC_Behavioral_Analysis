function trc_data = redefineHeaders(trc_data)
    % Get the original headers
    headers = trc_data.Properties.VariableNames;

    % Initialize an empty cell array for the new headers
    new_headers = headers;

    % Loop through headers to rename 'Var' columns based on the preceding named header
    for i = 1:length(headers)
        % Check if the current header is not a 'Var' entry
        if ~startsWith(headers{i}, 'Var')
            % This is a named header, e.g., 'LASI'
            base_name = headers{i};

            % Rename the current base name to include '_X'
            new_headers{i} = [base_name '_X'];

            % Rename the next two 'Var' entries (if they exist) to base_name_Y and base_name_Z
            if i+1 <= length(headers) && startsWith(headers{i+1}, 'Var')
                new_headers{i+1} = [base_name '_Y'];
            end
            if i+2 <= length(headers) && startsWith(headers{i+2}, 'Var')
                new_headers{i+2} = [base_name '_Z'];
            end
        end
    end

    % Apply the new headers to the table
    trc_data.Properties.VariableNames = new_headers;

end
