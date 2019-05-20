from matplotlib import pyplot as plt
from numpy.fft  import rfft, rfftfreq
from numpy      import abs as np_abs

def show_spectrum(non_filtred_data, filtred_data, f_d):
	spectrum_non_filt = rfft(non_filtred_data)
	spectrum_filt     = rfft(filtred_data)

	fig, ax = plt.subplots(2)
	ax[0].set(xlabel = 'Frequency', ylabel = 'Amplitude', title = 'Without filtering')
	ax[1].set(xlabel = 'Frequency', ylabel = 'Amplitude', title = 'With filtering')

	ax[0].plot(rfftfreq(len(non_filtred_data), 1./f_d), np_abs(spectrum_non_filt))
	ax[1].plot(rfftfreq(len(filtred_data),  1./f_d), np_abs(spectrum_filt))

	ax[0].grid()
	ax[1].grid()

	plt.show()


