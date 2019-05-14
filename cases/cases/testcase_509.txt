int func(int a, int b, int c)
{
	return (a + b + c) & ((1 << 30) - 1);
}

int main()
{
	int n = getInt();
	int[][] f = new int[n][n];
	int[][] g = new int[n][n];
	int[][] g_useless = new int[n][n];
	int i; int j; int k;
	for(i = 0; i < n; ++i)
		for(j = 0; j < n; ++j)
			f[i][j] = i + j;
	for(i = 0; i < n; ++i)
		for(j = 0; j < n; ++j)
		{
			for(k = 0; k < n; ++k)
			{
				if(j >= i)
				{
					g[i][j] = func(g[i][j], f[i][k], f[k][j]);
					g_useless[i][j] = func(g[i][j], f[i][k], f[k][j]);
					g_useless[i][j] = func(g[i][j], f[i][k], f[k][j]);
					g_useless[i][j] = func(g[i][j], f[i][k], f[k][j]);
				}
			}
		}
	int sum = 0;
	for(i = 0; i < n; ++i)
		for(j = 0; j < n; ++j)
			sum = (sum + g[i][j]) & ((1 << 30) - 1);
	print(toString(sum));
	return 0;
}




/*!! metadata:
=== comment ===
optim1-5140309234-xietiancheng.txt
Hint: (j >= i) is invariant, so the code should be changed to
if (j >= i)
{
	for (...)
	...
}
You may also want to do a inline optimization if you cannot pass it
We also expect you to do dead code elimination.
If the time bound is too tight or too loose, contact TA for help.
=== input ===
700
=== assert ===
output
=== timeout ===
15.0
=== output ===
655083248
=== phase ===
optim pretest
=== is_public ===
True

!!*/

