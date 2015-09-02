'''
Author: Marcel Milcent

This is a module for application of Benford's Law to a sequence of 
numbers.

Dependent on pandas and numpy, using matplotlib for visualization

All logarithms ar in base 10: "np.log10"
'''

# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class First(pd.DataFrame):
 	"""	Returns the expected probabilities of the first digits
	according to Benford's distribution."""

 	def __init__(self, plot = True):
 		First_Dig = np.arange(1,10)
 		Exp = np.log10(1 + (1. / First_Dig))

 		pd.DataFrame.__init__(self, {'Expected':\
 			Exp}, index = First_Dig)
 		self.index.names = ['First_Dig']

		if plot == True:
			self.plot(kind='bar', color = 'g', grid=False)

class Second(pd.DataFrame):
	'''
	Returns the expected probabilities of the second digits
	according to Benford's distribution.
	'''
	def __init__(self, plot = True):
		a = np.arange(10,100)
		Expe = np.log10(1 + (1. / a))
		Sec_Dig = np.array(range(10)*9)

		pd.DataFrame.__init__(self,{'Expected': Expe, 'Sec_Dig': Sec_Dig})#index = a)
		self = self.groupby('Sec_Dig').sum()
		if plot == True:
			self.plot(kind='bar', color = 'g', grid=False, ylim=(0,.14))

class FirstTwo(pd.DataFrame):
	'''
	Returns the expected probabilities of the first two digits
	according to Benford's distribution.
	'''
	def __init__(self, plot=True):
		First_2_Dig = np.arange(10,100)
		Expect = np.log10(1 + (1. / First_2_Dig))

		pd.DataFrame.__init__(self,{'Expected':Expect, 'First_2_Dig':\
			First_2_Dig})
		self.set_index('First_2_Dig', inplace=True)
		if plot == True:
			self.plot(kind='bar', figsize = (15,8), color='g', grid=False)

class LastTwo(pd.DataFrame):
	'''   
	Returns the expected probabilities of the last two digits
	according to Benford's distribution.
	'''
	def __init__(self, plot=True):
		exp = np.array([1/99.]*100)
		pd.DataFrame.__init__(self,{'Expected': exp,'Last_2_Dig':_lt_()})
		self.set_index('Last_2_Dig', inplace=True)
		if plot == True:
			self.plot(kind='bar',figsize = (15,8), color = 'g',\
				grid=False,  ylim=(0,.02))

class Analysis(pd.DataFrame):
	'''
	Initiates the Analysis of the series. pd.DataFrame subclass.
	Sequence must be of integers or floats. If not, it will try to convert
	it. If it does not succeed, a TyprError will be raised.
	A pandas DataFrame will be constructed, with the columns: original
	numbers without floating points, first, second, first two and
	last two digits, so the tests that will follow will run properly

	-> data: sequence of numbers to be evaluated. Must be in absolute values,
			since negative values with minus signs will distort the tests.
			PONDERAR DEIXAR O COMANDO DE CONVERTER PARA AbS
	-> dec: number of decimal places to be accounted for. Especially important
			for the last two digits test. The numbers will be multiplied by
			10 to the power of the dec value. Defaluts to 2, to currency. If 
			the numbers are integers, assign 0.
	-> latin: used for str dtypes representing numbers in latin format, with
			'.' for thousands and ',' for decimals. Converts to a string with
			only '.' for decimals one none if int, so it can be later converted
			to a number format. Defaults to False
	'''
	maps = {}

	def __init__(self, data, dec=2, latin=False):
		pd.DataFrame.__init__(self, {'Seq': data})
		self.dropna(inplace=True)
		print "Initialized sequence with " + str(len(self)) + " registries."
		if self.Seq.dtypes != 'int' and self.Seq.dtypes != 'float':
			print 'Sequence dtype is not int nor float./n\
			Trying to convert.../n'
			if latin == True:
				if dec != 0:
					self.Seq = self.Seq.apply(_sanitize_latin_float_, dec=dec)
				else:
					self.Seq = self.Seq.apply(_sanitize_latin_int_)
			#Try to convert to numbers
			self.Seq = self.Seq.convert_objects(convert_numeric=True)
			self.dropna(inplace=True)
			if self.Seq.dtypes != 'int' and self.Seq.dtypes != 'float':
				raise TypeError("The sequence dtype was not int nor float\
				 and could not be converted./nConvert it to wheather int of float\
				 and try again.")
		# Extracts the digits in their respective positions,
		self['ZN'] = self.Seq * (10**dec)  # dec - to manage decimals
		self.ZN = self.ZN.apply(_tint_)
		#self = self[self.ZN!=0]
		self['S'] = self.ZN.apply(str)
		self['FD'] = self.S.str[:1]   # get the first digit
		self['SD'] = self.S.str[1:2]  # get the second digit
		self['FTD'] = self.S.str[:2]  # get the first two digits
		self['LTD'] = self.S.str[-2:] # get the last two digits
		# Leave the last two digits as strings , so as to be able to\
		# display '00', '01', ... up to '09', till '99'
		# converting the others to integers
		self.FD = self.FD.apply(_tint_)
		self.SD = self.SD.apply(_tint_)
		self.FTD = self.FTD.apply(_tint_)
		del self['S']
		self = self[self.FTD>=10]

	def mantissas(self, plot=True, figsize=(15,8)):
		# if self.Seq.dtype != 'Float64':
		# 	self.apply(float)
		self['Mant'] = _getMantissas_(self.Seq)
		self = self[self.Seq>=1.]
		p = self.sort('Mant')
		N = len(p)
		
		#f = lambda g:g/N
		x = np.arange(N)
		fig = plt.figure(figsize=figsize)
		ax = fig.add_subplot(111)
		ax.plot(x,p.Mant,'k--')
		#ax.plot(x,f(x), 'b-')

	# def prepare(self, dec=2):
	# 	'''
	# 	Prepares the DataFrame to be manipulated by the tests, with columns
	# 	of the First, Second, First Two and Last Two digits of each number
	# 	'''
	# 	# Extracts the digits in their respective positions,
	# 	self['ZN'] = self.Seq * (10**dec)
	# 	self.ZN = self.ZN.apply(_tint_)
	# 	#self = self[self.ZN!=0]
	# 	self['S'] = self.ZN.apply(str)
	# 	self['FD'] = self.S.str[:1]   # get the first digit
	# 	self['SD'] = self.S.str[1:2]  # get the second digit
	# 	self['FTD'] = self.S.str[:2]  # get the first two digits
	# 	self['LTD'] = self.S.str[-2:] # get the last two digits
	# 	# Leave the last two digits as strings , so as to be able to\
	# 	# display '00', '01', ... up to '09', till '99'
	# 	# converting the others to integers
	# 	self.FD = self.FD.apply(_tint_)
	# 	self.SD = self.SD.apply(_tint_)
	# 	self.FTD = self.FTD.apply(_tint_)
	# 	del self['S']
	# 	self = self[self.FTD>=10]
		


	def firstTwoDigits(self, inform=True, MAD=True, top_Z=20, only_pos=True,\
		MSE=False, plot=True, map_back=True, mantissa = False):
		'''
		Performs the Benford First Two Digits test with the series of
		numbers provided.

		inform -> tells the number of registries that are being subjected to
		the Analysis; defaults to True

		MAD -> calculates the Mean of the Absolute Differences from the respective
		expected distributions; defaults to True.

		top_Z -> chooses the highest number of Z scores to be displayed

		only_pos -> will highlight only the values that are higher than the
		expexted frequencies, discarding the lower ones; defaults to True.

		MSE -> calculates the Mean Square Error of the sample; defaults to False.

		plot -> draws the plot of test for visual comparison, with the found
		distributions in bars and the expected ones in a line.

		map_back -> records the top differences to the maps dictionary to
		later index the original sequence; defaults to True.

		'''
		N = len(self)
		x = np.arange(10,100)
		if inform:
			print "\n---Test performed on " + str(N) + " registries.---\n"
		# get the number of occurrences of the first two digits
		v = self.FTD.value_counts()
		# get their relative frequencies
		p = self.FTD.value_counts(normalize =True)
		# crate dataframe from them
		df = pd.DataFrame({'Counts': v, 'Found': p}).sort_index()
		# reindex from 10 to 99 in the case one or more of the first
		# two digits are missing, so the Expected frequencies column
		# can later be joined; and swap NANs with zeros.
		if len(df.index) < 90:
			df = df.reindex(x).fillna(0)
		# join the dataframe with the one of expected Benford's frequencies
		df = FirstTwo(plot=False).join(df)
		# create column with absolute differences
		df['Dif'] = df.Found - df.Expected
		df['AbsDif'] = np.absolute(df.Dif)
		# calculate the Z-test column an display the dataframe by descending
		# Z test
		df['Z_test'] = _Z_test(df,N)
		if only_pos:
			dd = df[['Expected','Found','Z_test']][df.Dif>0].sort('Z_test',\
			 ascending=False).head(top_Z)
			print '\nThe positive deviations` top ' + str(top_Z) + ' Z scores are:\n'
		else:
			dd = df[['Expected','Found','Z_test']].sort('Z_test',\
			 ascending=False).head(top_Z)
			print '\nThe top ' + str(top_Z) + ' Z scores are:\n'
		print dd
		
		if map_back == True:
			self.maps['FTD'] = np.array(dd.index)

		# Mean absolute difference
		if MAD == True:
			mad = _mad_(df)
			print "\nThe Mean Absolute Deviation is " + str(mad) + '\n'\
			+ 'For the First Two Digits:\n\
			- 0.0000 to 0.0012: Close Conformity\n\
			- 0.0012 to 0.0018: Acceptable Conformity\n\
			- 0.0018 to 0.0022: Marginally Acceptable Conformity\n\
			- Above 0.0022: Nonconformity'
		# Mean Square Error
		if MSE == True:
			mse = _mse_(df)
			print "\nMean Square Error = " + str(mse)
		# Plotting the expected frequncies (line) against the found ones(bars)
		if plot == True:
			_plot_benf_(df, x=x, y_Exp= df.Expected,y_Found=df.Found, N=N)

		if mantissa == True:
			df['Mantissas'] = np.log10(g) - np.log10(g).astype(int)


		return df

	def firstDigit(self, inform=True, MAD=True, MSE=False, only_pos=True,\
	map_back=True, plot=True):
		'''
		Performs the Benford First Digit test with the series of
		numbers provided.

		inform -> tells the number of registries that are being subjected to
		the Analysis; defaults to True

		MAD -> calculates the Mean of the Absolute Differences from the respective
		expected distributions; defaults to True.

		Z_test -> calculates the Z test of the sample; defaluts to True.

		map_back -> records the ordered higher differences to the maps dictionary
		to later index the original sequence; defaults to True.

		MSE -> calculates the Mean Square Error of the sample; defaluts to False.

		plot -> draws the plot of test for visual comparison, with the found
		distributions in bars and the expected ones in a line.

		'''

		N = len(self)
		x = np.arange(1,10)
		if inform:
			print "\n---Test performed on " + str(N) + " registries.---\n"
		# get the number of occurrences of each first digit
		v = self.FD.value_counts()
		# get their relative frequencies
		p = self.FD.value_counts(normalize =True)
		# crate dataframe from them
		df = pd.DataFrame({'Counts': v, 'Found': p}).sort_index()
		# reindex from 10 to 99 in the case one or more of the first
		# two digits are missing, so the Expected frequencies column
		# can later be joined; and swap NANs with zeros.

		# join the dataframe with the one of expected Benford's frequencies
		df = First(plot=False).join(df)
		# create column with absolute differences
		df['Dif'] = df.Found - df.Expected
		df['AbsDif'] = np.absolute(df.Dif)
		# calculate the Z-test column an display the dataframe by descending
		# Z test
		df['Z_test'] = _Z_test(df,N)
		if only_pos:
			dd = df[['Expected','Found','Z_test']][df.Dif>0].sort('Z_test',\
			 ascending=False)
			print '\nThe descending positive deviations` Z scores are:\n'
		else:
			dd = df[['Expected','Found','Z_test']].sort('Z_test',\
			 ascending=False)
			print '\nThe descending Z scores are:\n'
		print dd

		if map_back == True:
			self.maps['FD'] = np.array(dd.index)

		# Mean absolute difference
		if MAD == True:
			mad = _mad_(df)
			print "\nThe Mean Absolute Deviation is " + str(mad) + '\n'\
			+ 'For the First Digits:\n\
			- 0.0000 to 0.0006: Close Conformity\n\
			- 0.0006 to 0.0012: Acceptable Conformity\n\
			- 0.0012 to 0.0015: Marginally Acceptable Conformity\n\
			- Above 0.0015: Nonconformity'
		# Mean Square Error
		if MSE == True:
			mse = _mse_(df)
			print "\nMean Square Error = " + str(mse)
		# Plotting the expected frequncies (line) against the found ones(bars)
		if plot == True:
			_plot_benf_(df, x=x, y_Exp= df.Expected,y_Found=df.Found, N=N)

		### return df

	def secondDigit(self, inform=True, MAD=True, MSE=False, only_pos=True,\
	map_back=True, plot=True):
		'''
		Performs the Benford Second Digit test with the series of
		numbers provided.

		inform -> tells the number of registries that are being subjected to
		the Analysis; defaults to True

		MAD -> calculates the Mean of the Absolute Differences from the respective
		expected distributions; defaults to True.

		Z_test -> calculates the Z test of the sample; defaluts to True.

		map_back -> records the ordered higher differences to the maps dictionary
		to later index the original sequence; defaults to True.

		MSE -> calculate the Mean Square Error of the sample; defaluts to False.

		plot -> draws the plot of test for visual comparison, with the found
		distributions in bars and the expected ones in a line.

		'''

		N = len(self)
		x = np.arange(0,10)
		if inform:
			print "\n---Test performed on " + str(N) + " registries.---\n"
		# get the number of occurrences of each second digit
		v = self.SD.value_counts()
		# get their relative frequencies
		p = self.SD.value_counts(normalize =True)
		# crate dataframe from them
		d = pd.DataFrame({'Counts': v, 'Found': p}).sort_index()
		# reindex from 10 to 99 in the case one or more of the first
		# two digits are missing, so the Expected frequencies column
		# can later be joined; and swap NANs with zeros.

		# join the dataframe with the one of expected Benford's frequencies
		df = Second(plot=False).groupby('Sec_Dig').sum().join(d)
		# create column with absolute differences
		df['Dif'] = df.Found - df.Expected
		df['AbsDif'] = np.absolute(df.Dif)
		# calculate the Z-test column an display the dataframe by descending
		# Z test
		df['Z_test'] = _Z_test(df,N)
		if only_pos:
			dd = df[['Expected','Found','Z_test']][df.Dif>0].sort('Z_test',\
			 ascending=False)
			print '\nThe descending positive deviations` Z scores are:\n'
		else:
			dd = df[['Expected','Found','Z_test']].sort('Z_test',\
			 ascending=False)
			print '\nThe descending Z scores are:\n'
		print dd

		if map_back == True:
			self.maps['SD'] = np.array(dd.index)

		# Mean absolute difference
		if MAD == True:
			mad = _mad_(df)
			print "\nThe Mean Absolute Deviation is " + str(mad) + '\n'\
			+ 'For the Second Digits:\n\
			- 0.0000 to 0.0008: Close Conformity\n\
			- 0.0008 to 0.0010: Acceptable Conformity\n\
			- 0.0010 to 0.0012: Marginally Acceptable Conformity\n\
			- Above 0.0012: Nonconformity'
		# Mean Square Error
		if MSE == True:
			mse = _mse_(df)
			print "\nMean Square Error = " + str(mse)
		# Plotting the expected frequncies (line) against the found ones(bars)

		if plot == True:
			_plot_benf_(df, x=x, y_Exp= df.Expected,y_Found=df.Found, N=N)

		### return df

	def lastTwoDigits(self, inform=True, MAD=False, Z_test=True, top_Z=20,\
	 only_pos=True, map_back=True, MSE=False, plot=True):
		'''
		Performs the Benford Last Two Digits test with the series of
		numbers provided.

		inform -> tells the number of registries that are being subjected to
		the Analysis; defaults to True

		MAD -> calculates the Mean of the Absolute Differences from the respective
		expected distributions; defaults to True.

		Z_test -> calculates the Z test of the sample; defaluts to True.

		top_Z -> chooses the highest number of Z scores to be displayed

		MSE -> calculate the Mean Square Error of the sample; defaluts to False.

		plot -> draws the plot of test for visual comparison, with the found
		distributions in bars and the expected ones in a line.

		'''

		N = len(self)
		x = np.arange(0,100)
		if inform:
			print "\n---Test performed on " + str(N) + " registries.---\n"
		# get the number of occurrences of the last two digits
		v = self.LTD.value_counts()
		# get their relative frequencies
		p = self.LTD.value_counts(normalize =True)
		# crate dataframe from them
		df = pd.DataFrame({'Counts': v, 'Found': p}).sort_index()
		# join the dataframe with the one of expected Benford's frequencies
		df = LastTwo(plot=False).join(df)
		# create column with absolute differences
		df['Dif'] = df.Found - df.Expected
		df['AbsDif'] = np.absolute(df.Dif)
		# calculate the Z-test column an display the dataframe by descending
		# Z test
		df['Z_test'] = _Z_test(df,N)
		if only_pos:
			dd = df[['Expected','Found','Z_test']][df.Dif>0].sort('Z_test',\
			 ascending=False).head(top_Z)
			print '\nThe positive deviations` top ' + str(top_Z) + ' Z scores are:\n'
		else:
			dd = df[['Expected','Found','Z_test']].sort('Z_test',\
			 ascending=False).head(top_Z)
			print '\nThe top ' + str(top_Z) + ' Z scores are:\n'
		print dd
		
		if map_back == True:
			self.maps['LTD'] = np.array(dd.index)

		# Mean absolute difference
		if MAD == True:
			mad = _mad_(df)
			print "\nThe Mean Absolute Deviation is " + str(mad) + '\n'\
		# Mean Square Error
		if MSE == True:
			mse = _mse_(df)
			print "\nMean Square Error = " + str(mse)
		# Plotting the expected frequencies (line) against the found ones(bars)
		if plot == True:
			_plot_benf_(df, x=x, y_Exp= df.Expected,y_Found=df.Found, N=N)

		### return df
	
	def duplicates(self, inform=True, top_Rep=20):
		# self.Seq = self.Seq.apply(int) / 100.
		N = len(self)
		### self.Seq = self.Seq.apply(_to_float_)
		# get the frequencies
		v = self.Seq.value_counts()
		# get their relative frequencies
		p = self.Seq.value_counts(normalize =True) * 100
		# crate dataframe from them
		df = pd.DataFrame({'Counts': v, 'Percent': p}).sort('Counts',\
			ascending=False)
		if inform:
			print "\n---Test performed on " + str(N) + " registries.---\n"
			print '\nThe ' + str(top_Rep) + ' most frequent numbers are:\n'
			print df.head(top_Rep)
		### return df

def _Z_test(frame,N):
	return (frame.AbsDif - (1/2*N))/(np.sqrt(frame.Expected*\
		(1-frame.Expected)/N))

def _mad_(frame):
	return frame.AbsDif.mean()

def _mse_(frame):
	return (frame.AbsDif**2).mean()

def _getMantissas_(arr):
	'''
	The mantissa is the non-integer part of the log of a number.
	This fuction uses the element-wise array operations of numpy
	to get the mantissas of each number's log.

	arr: np.array of integers or floats ---> np.array of floats
	'''

	return np.log10(arr) - np.log10(arr).astype(int)


def _first_(plot=False):
	'''
	Returns the expected probabilities of the first digits
	according to Benford's distribution.
	'''
	First_Dig = np.arange(1,10)
	Expected = np.log10(1 + (1. / First_Dig))
	first = pd.DataFrame({'Expected':Expected,\
			'First_Dig':First_Dig}).set_index('First_Dig')
	if plot == True:
		first.plot(kind='bar', grid=False)
	return first

def _second_(plot=False):
	'''
	Returns the expected probabilities of the second digits
	according to Benford's distribution.
	'''
	a = np.arange(10,100)
	Expected = np.log10(1 + (1. / a))
	Sec_Dig = np.array(range(10)*9)
	d = pd.DataFrame({'Expected': Expected, 'Sec_Dig': Sec_Dig},\
			index = a)
	sec = d.groupby('Sec_Dig').agg(sum)
	if plot == True:
		sec.plot(kind='bar', grid=False)
	return sec

def _firstTwo_(plot=False):
	'''
	Returns the expected probabilities of the first two digits
	according to Benford's distribution.
	'''
	First_2_Dig = np.arange(10,100)
	Expected = np.log10(1 + (1. / First_2_Dig))
	ft = pd.DataFrame({'First_2_Dig':First_2_Dig,\
			'Expected':Expected}).set_index('First_2_Dig')
	if plot == True:
		ft.plot(kind='bar', figsize = (15,8),grid=False)
	return ft

def _lastTwo_(plot=False):
	exp = np.array([1/99.]*100)
	lt = pd.DataFrame({'Last_2_Dig': _lt_(),\
			'Expected': exp}).set_index('Last_2_Dig')
	if plot == True:
		lt.plot(kind='bar',figsize = (15,8), grid=False,  ylim=(0,.02))
	return lt

def _lt_():
	l = []
	d = '0123456789'
	for i in d:
		for j in d:
			t = i+j
			l.append(t)
	return np.array(l)

def _to_float_(st):
	try:
		return float(st) /100
	except:
		return np.nan

def _sanitize_(arr):
	'''
	Prepares the series to enter the test functions, in case pandas
	has not inferred the type to be float, especially when parsing
	from latin datases which use '.' for thousands and ',' for the
	floating point.
	'''
	return pd.Series(arr).dropna().apply(str).apply(_only_numerics_).apply(_l_0_strip_)

	#if not isinstance(arr[0:1],float):
	#	arr = arr.apply(str).apply(lambda x: x.replace('.','')).apply(lambda x:\
	#	 x.replace(',','.')).apply(float)
	#return arr.abs()

def _only_numerics_(seq):
    return filter(type(seq).isdigit, seq)

def _str_to_float_(s):
	#s = str(s)
	if '.' in s or ',' in s:
		s = filter(type(s).isdigit, s)
		s = s[:-2]+'.'+s[-2:]
		return float(s)
	else:
		if filter(type(s).isdigit, s) == '':
			return np.nan
		else:
			return int(s)


def _l_0_strip_(st):
	return st.lstrip('0')

def _tint_(s):
	try:
		return int(s)
	except:
		return 0

def _len2_(st):
	return len(st) == 2

def _plot_benf_(df, x, y_Exp, y_Found, N,lowUpBounds = True, figsize=(15,8)):		
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(111)
	plt.title('Expected vs. Found Distributions')
	plt.xlabel('Digits')
	plt.ylabel('Distribution')
	ax.bar(x, y_Found, label='Found')
	ax.plot(x, y_Exp, color='g',linewidth=2.5,\
	 label='Expected')
	ax.legend()
	# Plotting the Upper and Lower bounds considering p=0.05
	if lowUpBounds == True:
		sig_5 = 1.96 * np.sqrt(y_Exp*(1-y_Exp)/N)
		upper = y_Exp + sig_5 + (1/(2*N))
		lower = y_Exp - sig_5 - (1/(2*N))
		ax.plot(x, upper, color= 'r')
		ax.plot(x, lower, color= 'r')
		ax.fill_between(x, upper,lower, color='r', alpha=.3)
	plt.show()


def _collapse_(num):
	'''
	Transforms any positive number to the form XX.yy, with two digits
	to the left of the floating point
	'''
	l=10**int(np.log10(num))
	if num>=1.:
		return 10.*num/l
	else:
		return 100.*num/l

def _collapse_array_(arr):
	'''

	'''
	# arr = abs(arr)
	ilt = 10**(np.log10(arr).astype(int))
	arr[arr<1.]*=10
	return arr*10/ilt

def _sanitize_float_(s, dec):
	s = str(s)
	if '.' in s or ',' in s:
		s = filter(type(s).isdigit, s)
		s = s[:-dec]+'.'+s[-dec:]
		return float(s)
	else:
		if filter(type(s).isdigit, s) == '':
			return np.nan
		else:
			return int(s)

def _sanitize_latin_float_(s, dec=2):
	s = str(s)
	s = filter(type(s).isdigit, s)
	return s[:-dec]+'.'+s[-dec:]

def _sanitize_latin_int_(s):
	s = str(s)
	s = filter(type(s).isdigit, s)
	return s

