def heart(mx: float = 0.04, my: float = 0.08145, uk: int = 30):
    # Default: my = 0.072
    # My Android Smart Phone: my = 0.07145
    # My Laptop Console: my = 0.8145
    # Using algebraic equation: (x^2+y^2 - 1)^3 - x^2 * y^3 = 0
	print('\n'.join([''.join([('*'[(x-y) % len('*')] if ((x*mx)**2+(y*my)**2-1)**3-(x*mx)**2*(y*my)**3 <= 0 else ' ') for x in range(-uk, uk)]) for y in range(uk, -uk, -1)]))


if __name__ == "__main__":
	heart(0.04, 0.08145, 35)