## Function: generate_pxx_file(filepath, filename, extension, results_path)

Generates a Pxx file.

### Parameters:

- `filepath` (string): The path of the input file.
- `filename` (string): The name of the output file.
- `extension` (string): The file extension.
- `results_path` (string): The path to save the output file.

## Function: create_daily_pxx(folder_path, output_folder, extension)

Creates daily Pxx files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.

## Function: generate_daily_msp(folder_path, output_folder, extension, freq_min=None, freq_max=None)

Generates daily MSP (Mean Spectral Power) files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.
- `freq_min` (int, optional): The minimum frequency for filtering. Defaults to None.
- `freq_max` (int, optional): The maximum frequency for filtering. Defaults to None.

## Function: generate_daily_spl(folder_path, output_folder, extension)

Generates daily SPL (Sound Pressure Level) files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.

## Function: generate_long_time_fb_spl(folder_path, output_folder, extension)

Generates long-time A-weighted SPL (Sound Pressure Level) files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.

## Function: generate_long_time_fb_spl_gram(folder_path, output_folder, extension, title)

Generates long-time A-weighted SPL spectrogram files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.
- `title` (string): The title for the generated spectrogram.

## Function: generate_daily_spectrogram_images(folder_path, output_folder, extension)

Generates daily spectrogram image files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.

## Function: generate_weekly_pxx(folder_path, output_folder, extension)

Generates weekly Pxx files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.

## Function: generate_weekly_spectrogram_images(folder_path, output_folder, extension)

Generates weekly spectrogram image files.

### Parameters:

- `folder_path` (string): The path to the folder containing the input files.
- `output_folder` (string): The path to save the output files.
- `extension` (string): The file extension.
