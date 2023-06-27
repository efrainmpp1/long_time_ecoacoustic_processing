import LongTimeProcessingEcoacousticTools

daily_pxx_folder = './results/Daily'

LongTimeProcessingEcoacousticTools.Tools.generate_daily_spectrogram_images(
    daily_pxx_folder, './results/DailySpectograms', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_weekly_pxx(
    daily_pxx_folder, './results/WeeklyPxx/', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_weekly_spectrogram_images(
    './results/Daily', './results/WeeklySpectograms', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_daily_msp(
    daily_pxx_folder, './results/DailyMSP/100_to_1500Hz', 'mat', freq_min=100, freq_max=1500)

LongTimeProcessingEcoacousticTools.Tools.generate_daily_spl(
    './results/DailyMSP/100_to_1500Hz', './results/DailySPL/100_to_1500Hz', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_long_time_fb_spl(
    './results/DailySPL/100_to_1500Hz', './results/FB_SPL/100_to_1500Hz', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_long_time_fb_spl_gram(
    './results/FB_SPL/100_to_1500Hz', './results/FB_SPL/100_to_1500Hz', 'mat', 'LOW (100Hz-1500Hz) FB_SPL')

LongTimeProcessingEcoacousticTools.Tools.generate_daily_msp(
    daily_pxx_folder, './results/DailyMSP/1500_to_5000Hz', 'mat', freq_min=1500, freq_max=5000)

LongTimeProcessingEcoacousticTools.Tools.generate_daily_spl(
    './results/DailyMSP/1500_to_5000Hz', './results/DailySPL/1500_to_5000Hz', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_long_time_fb_spl(
    './results/DailySPL/1500_to_5000Hz', './results/FB_SPL/1500_to_5000Hz', 'mat')

LongTimeProcessingEcoacousticTools.Tools.generate_long_time_fb_spl_gram(
    './results/FB_SPL/1500_to_5000Hz', './results/FB_SPL/1500_to_5000Hz', 'mat', 'HIGH (1500Hz-5000Hz) FB_SPL')
