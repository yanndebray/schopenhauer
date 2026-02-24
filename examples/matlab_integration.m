% Schopenhauer MATLAB Integration Example
% This script demonstrates how to call Schopenhauer from MATLAB

%% 1. Run Analysis
fprintf('Running analysis...
');
results = struct('model_name', 'BrakingController_v2', 'accuracy', 0.985, 'latency_ms', 12.4);

%% 2. Export Data
fprintf('Exporting data...
');
% Export to YAML (requires a YAML library or just write simple text)
fid = fopen('data/model_results.yaml', 'w');
fprintf(fid, 'model_name: %s
', results.model_name);
fprintf(fid, 'accuracy: %.3f
', results.accuracy);
fprintf(fid, 'latency: %.1f
', results.latency_ms);
fclose(fid);

% Save a plot
plot(rand(1,100));
title('Controller Performance');
saveas(gcf, 'figures/performance_plot.png');

%% 3. Generate Report via CLI
fprintf('Generating report via Schopenhauer CLI...
');
% Using the 'will render' command
[status, cmdout] = system('will render report.md -o validation_report.docx -t report');

if status == 0
    fprintf('Report generated successfully!
');
    disp(cmdout);
else
    fprintf('Error generating report:
');
    disp(cmdout);
end

%% 4. Alternative: Call via Python API
% Requires MATLAB configured with a Python interpreter: pyenv('Version', 'path/to/venv')
% fprintf('Generating report via Python API...
');
% py.will.render('report.md', output='validation_report.docx', template='report');
