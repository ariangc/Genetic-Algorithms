from __future__ import print_function
from numpy import random, array, dot
import sys
from math import *

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class NeuralNet:
	def __init__(self, weights):
		self.weights = weights

	def getOutput(self, inputs, prev):
		in_hid = self.weights[:36]
		in_hid = in_hid.reshape(9,4)
		hid = dot(array(inputs).T, in_hid)
		hid_out = self.weights[36:]
		hid_out = hid_out.reshape(4,4)
		output = dot(hid, hid_out)
		x = 0
		y = 0
		for i in range(len(output)):
			if output[i] > x and abs(i - prev) != 2:
				x = output[i]
				y = i

		return y