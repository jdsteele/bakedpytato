def decimal_round(value, digits=2):
	e = 10 ** digits
	value = value * e
	value = value.to_integral_value(ROUND_HALF_UP) / e
	return value

def linear_extrapolation(self, x, xa, ya, xb, yb):
	q = xb - xa
	if (q == 0):
		return None
	
	r = x - xa
	s = yb - ya
	t = r * s
	u = t / q
	y = ya + u
	return y

