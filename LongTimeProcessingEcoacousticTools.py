# Importing Libs
import os
import h5py
import numpy as np
import soundfile as sf
import scipy.signal as sg
import matplotlib.pyplot as plt
import matplotlib.style as stl
import utils
stl.use('default')

# adding constants

# defining project constants
SAMPLE_RATE = 32000  # 96kHz
CHUNK_STEP_IN_SECONDS = 60  # 60 seconds each signal_chunk
CHUNK_SIZE = CHUNK_STEP_IN_SECONDS * SAMPLE_RATE
NFFT = 2048
NPERSEG = (NFFT/2) + 1


class LongTimeProcessingEcoacousticTools:

    def generate_pxx_file(filepath, filename, extension, results_path):
        # Create the results directory if it doesn't exist
        os.makedirs(results_path, exist_ok=True)

        # Calculate the duration of the audio in minutes
        duration_audio = utils.get_duration_audio(filepath)
        duration_audio -= duration_audio % CHUNK_STEP_IN_SECONDS
        duration_audio_in_minutes = int(duration_audio / CHUNK_STEP_IN_SECONDS)

        total_samples = duration_audio * SAMPLE_RATE

        # Initialize the spectrogram matrix
        matrix_spec = np.zeros(((NFFT/2)+1, duration_audio_in_minutes))

        count = 0
        start_sample = 0
        end_sample = CHUNK_SIZE

        while end_sample <= total_samples:
            # Capture a chunk of audio
            audio_chunk, _ = sf.read(
                filepath, start=start_sample, stop=end_sample)

            # Compute the spectrogram using Welch's method
            _, Pxx_spec = sg.welch(audio_chunk, SAMPLE_RATE, 'hann',
                                   nperseg=NPERSEG, nfft=NFFT, scaling='spectrum')

            # Reverse the order of the spectrogram values
            Pxx_spec_order = Pxx_spec[::-1]

            # Assign the reversed spectrogram values to the matrix
            matrix_spec[:, count] = Pxx_spec_order

            # Update the start and end samples for the next chunk
            start_sample = end_sample
            end_sample = start_sample + CHUNK_SIZE
            count += 1

        # Generate the output filename
        output_file_name = f"Pxx_{filename}.{extension}"
        output_file_path = os.path.join(results_path, output_file_name)

        # Create a file
        with h5py.File(output_file_path, 'w') as file:
            # Create a dataset and save the spectrogram matrix
            file.create_dataset('Pxx', data=matrix_spec)

    def create_daily_pxx(folder_path, output_folder, extension):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the list of files in the folder
        file_list = os.listdir(folder_path)

        # Dictionary to store the daily Pxx matrices
        daily_pxx = {}

        for file_name in file_list:
            # Check if the file is a spectrogram file
            if file_name.startswith("PXX_") and file_name.endswith(extension):
                # Extract the date from the file name
                # file name format -> PXX_<YEAR><MONTH><DAY>_<HOUR><MINUTE><SECOND>
                # Assume the file name format is consistent
                date_str = file_name[4:12]

                # Open the HDF5 file
                file_path = os.path.join(folder_path, file_name)
                with h5py.File(file_path, "r") as file:
                    # Get the Pxx matrix from the file
                    pxx = file["Pxx"][:]

                # Check if there is already a matrix for the current date
                if date_str not in daily_pxx:
                    daily_pxx[date_str] = pxx
                else:
                    # Concatenate the current Pxx matrix with the existing matrix for the day
                    daily_pxx[date_str] = np.concatenate(
                        (daily_pxx[date_str], pxx), axis=1)

        # Save the daily matrices to files
        for date_str, pxx in daily_pxx.items():
            output_file_name = f"DailyPxx_{date_str}.{extension}"
            output_file_path = os.path.join(output_folder, output_file_name)
            with h5py.File(output_file_path, "w") as output_file:
                output_file.create_dataset("Pxx", data=pxx)

    def generate_daily_msp(folder_path, output_folder, extension, freq_min=None, freq_max=None):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the list of files in the folder
        file_list = os.listdir(folder_path)

        if(freq_min and freq_max):
            # Get the frequencies corresponding to Pxx
            frequencies = np.fft.rfftfreq(NFFT, d=1 / SAMPLE_RATE)
            # Encontrando os índices correspondentes à faixa de frequência desejada
            idx = (frequencies > freq_min) & (frequencies < freq_max)

        for file_name in file_list:
            # Check if the file is a spectrogram file
            if file_name.startswith("DailyPxx_") and file_name.endswith(extension):
                # Extract the date from the file name
                # Format of file name -> DailyPxx_<YEAR>.<MONTH>.<DAY>.extension
                # Assume the file name format is consistent
                date_str = file_name[9:19]

                # Open the HDF5 file
                file_path = os.path.join(folder_path, file_name)
                with h5py.File(file_path, "r") as file:
                    # Get the Pxx matrix from the file
                    pxx = file["Pxx"][:]

                # Calc the energy x time
                energy = pxx[idx, :].sum(
                    axis=0) if freq_min and freq_max else pxx.sum(axis=0)

                energy_smoothed = utils.moving_average_filter(energy, 5)
                output_file_name = f"DailyMSP_{date_str}.{extension}"
                output_file_path = os.path.join(
                    output_folder, output_file_name)

                with h5py.File(output_file_path, "w") as file:
                    file.create_dataset("Msp", data=energy_smoothed)

    def generate_daily_spl(folder_path, output_folder, extension):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the list of files in the folder
        file_list = os.listdir(folder_path)

        for file_name in file_list:
            # Check if the file is a spectrogram file
            if file_name.startswith("DailyPSD_") and file_name.endswith(extension):
                # Extract the date from the file name
                # Format of file name -> DailyPSD_<YEAR>.<MONTH>.<DAY>.extension
                # Assume the file name format is consistent
                date_str = file_name[9:19]

                # Open the file
                file_path = os.path.join(folder_path, file_name)
                with h5py.File(file_path, "r") as file:
                    # Get the Pxx matrix from the file
                    msp = file["Msp"][:]

                spl = 10*np.log10(msp/1e-12)
                output_file_name = f"DailySPL_{date_str}.{extension}"
                output_file_path = os.path.join(
                    output_folder, output_file_name)

                with h5py.File(output_file_path, "w") as file:
                    file.create_dataset("Spl", data=spl)

    def generate_long_time_fb_spl(folder_path, output_folder, extension):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        # Get the list of daily files sorted by name
        daily_spl_files = sorted(file for file in os.listdir(
            folder_path) if file.startswith("DailySPL_") and file.endswith(extension))

        # Initialize the spectrogram matrix
        fb_spl = np.ones((1440, len(daily_spl_files)))
        count = 0

        for file_name in daily_spl_files:

            # Extract the date from the file name
            # Format of file name -> DailyPSL_<YEAR><MONTH><DAY>.extension
            # Assume the file name format is consistent
            #date_str = file_name[9:19]
            # Open the file
            file_path = os.path.join(folder_path, file_name)
            with h5py.File(file_path, "r") as file:
                # Get the Pxx matrix from the file
                spl = file["Spl"][:]

            # Reverse the order of the spectrogram values
            spl_order = spl[::-1]
            # Fill remaining values with last value of spl_order
            fb_spl[-len(spl_order):, count] = spl_order[-1]
            fb_spl[:len(spl_order), count] = spl_order

            count += 1

        interpolated_fbspl = utils.interpolate_matrix(fb_spl)

        output_file_name = f"FbSPL.{extension}"
        output_file_path = os.path.join(output_folder, output_file_name)

        with h5py.File(output_file_path, "w") as file:
            file.create_dataset("fb_spl", data=interpolated_fbspl)

    def generate_long_time_fb_spl_gram(folder_path, output_folder, extension , title):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

         # Get the list of daily files sorted by name
        fb_files = sorted(file for file in os.listdir(
        folder_path) if file.startswith("FbSPL") and file.endswith(extension))

        for file_name in fb_files:

            file_path = os.path.join(folder_path, file_name)
            with h5py.File(file_path, "r") as file:
                # Get the Pxx matrix from the file
                fb_spl = file["fb_spl"][:]

            hours_day = np.linspace(0, 24, fb_spl.shape[0])
            time = np.linspace(0,29,fb_spl.shape[1])
            xticks = np.arange(1,len(fb_files))
            plt.figure(figsize=(10, 6))


            # Plot the matrix using pcolormesh
            plt.pcolormesh(time, hours_day, np.log10(fb_spl), cmap='jet')

            # Add a color bar
            plt.colorbar()
            #plt.clim(1.87,1.92)

            plt.title(f'{title}')
            plt.yticks(np.arange(1, 25))
            plt.xticks(xticks)
            # Add labels to the axes
            plt.xlabel('Days')
            plt.ylabel('Hours of day (h)')
            
            output_file_name = "FbSPL_Gram.jpg"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            plt.savefig(output_file_path)
            plt.show()
            plt.close()


    def generate_daily_spectrogram_images(folder_path, output_folder, extension):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the list of files in the folder
        file_list = os.listdir(folder_path)

        # Get the frequencies corresponding to Pxx
        frequencies = np.fft.rfftfreq(NFFT, d=1 / SAMPLE_RATE)

        for file_name in file_list:
            # Check if the file is a spectrogram file
            if file_name.startswith("DailyPxx_") and file_name.endswith(extension):
                # Extract the date from the file name
                # Format of file name -> DailyPxx_<YEAR><MONTH><DAY>.extension
                # Assume the file name format is consistent
                date_str = file_name[9:17]

                # Open the HDF5 file
                file_path = os.path.join(folder_path, file_name)
                with h5py.File(file_path, "r") as file:
                    # Get the Pxx matrix from the file
                    pxx = file["Pxx"][:]

                time = np.linspace(0, 24, pxx.shape[1])

                plt.figure(figsize=(22, 6))
                # Plot the matrix using pcolormesh
                plt.pcolormesh(time, frequencies / 1000,
                               np.log10(pxx), cmap='jet')

                # Add a color bar
                plt.colorbar()

                plt.title('Day {}'.format(utils.format_date_str(date_str)))
                plt.xticks(np.arange(1, 25))
                # Add labels to the axes
                plt.xlabel('time (h)')
                plt.ylabel('frequency (kHz)')

                output_file_name = f"DailySpectrogram_{date_str}.jpg"
                output_file_path = os.path.join(
                    output_folder, output_file_name)

                plt.savefig(output_file_path)
                plt.close()

    def generate_weekly_pxx(folder_path, output_folder, extension):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the list of daily files sorted by name
        daily_files = sorted(file for file in os.listdir(
            folder_path) if file.startswith("DailyPxx_") and file.endswith(extension))

        # Check if there are enough files to form a complete week
        if len(daily_files) < 7:
            print("Not enough files to make a full week")
            return

        first_day = None
        last_day = None
        weekly_pxx = None  # Initialize the weekly matrix

        for i, file_name in enumerate(daily_files):
            # Assume the file name format is consistent
            date_str = file_name[9:19]

            if i % 7 == 0:
                first_day = date_str

            try:
                # Get the full file path
                file_path = os.path.join(folder_path, file_name)

                with h5py.File(file_path, "r") as file:
                    # Get the Pxx matrix from the daily file
                    pxx = file["Pxx"][:]

                if weekly_pxx is None:
                    weekly_pxx = pxx
                else:
                    weekly_pxx = np.concatenate((weekly_pxx, pxx), axis=1)

                if i % 7 == 6 or i == len(daily_files) - 1:
                    last_day = date_str
                    # Save the weekly matrix to a new file
                    weekly_file_name = f"WeeklyPxx_{first_day}_to_{last_day}.{extension}"
                    weekly_file_path = os.path.join(
                        output_folder, weekly_file_name)

                    with h5py.File(weekly_file_path, "w") as file:
                        file.create_dataset("Pxx", data=weekly_pxx)

                    print(f"Saved weekly file: {weekly_file_name}")
                    weekly_pxx = None

            except ValueError:
                print(f"Ignored invalid file: {file_name}")

        print("Concatenation completed.")

    def generate_weekly_spectrogram_images(folder_path, output_folder, extension):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the list of files in the provided folder
        file_list = os.listdir(folder_path)

        # Get the corresponding frequencies for Pxx
        frequencies = np.fft.rfftfreq(NFFT, d=1/SAMPLE_RATE)

        for file_name in file_list:
            # Check if the file is a spectrogram file
            if file_name.startswith("WeeklyPxx_") and file_name.endswith(extension):
                # Extract the start and end dates from the file name
                start_date_str = file_name[10:20]
                end_date_str = file_name[24:34]

                # Open the HDF5 file
                file_path = os.path.join(folder_path, file_name)
                with h5py.File(file_path, "r") as file:
                    # Get the Pxx matrix from the file
                    pxx = file["Pxx"][:]

                time = np.linspace(0, 7, pxx.shape[1])

                plt.figure(figsize=(22, 6))
                # Plot the matrix using pcolormesh
                plt.pcolormesh(time, frequencies/1000,
                               np.log10(pxx), cmap='jet')

                # Add a colorbar
                plt.colorbar()
                plt.clim(-8, -6)

                plt.title('Week {} to {}'.format(start_date_str, end_date_str))
                plt.xticks(np.arange(1, 7))
                # Add labels to the axes
                plt.xlabel('time (day)')
                plt.ylabel('frequency (kHz)')

                output_file_name = f"WeeklySpectrogram_{start_date_str}_to_{end_date_str}.jpg"
                output_file_path = os.path.join(
                    output_folder, output_file_name)

                plt.savefig(output_file_path)
                plt.close()

    
