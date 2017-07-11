#!/usr/bin/env python

def mean(data):
	n = len(data)
	media = 0.0

	for x in data:
		media += x

	media *= 1.0
	media /= n
	
	return media

def median(data):
	n = len(data)
	# dados ja estao ordenados

	if n % 2 == 0:
		q = n // 2
		median = (data[q-1] + data[q]) / 2.0
	else:
		q = (n+1) // 2
		median = data[q-1]

	return median


def variance(data):
	n = len(data)
	variance = 0.0
	mi = mean(data)

	for x in data:
		variance += (x ** 2)

	variance *= 1.0
	variance /= n
	variance -= (mi ** 2)

	return variance

def stdev(data):
	return (variance(data) ** 0.5)

