from numpy import exp, array, random, dot

out = array([0,0,1,1,2,2])

for i in range(len(out)):
	print(out[i])

out = out.reshape(3,2)
print(out)