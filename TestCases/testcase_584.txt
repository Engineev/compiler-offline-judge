int main() {
    int n = 5;
    int sum = 0;
    int i;
    int j;
    for (i = 1; i <= n; ++i)
        for (j = 1; j <= n; ++j)
            sum = sum + i;
    return sum;
}



/*!! metadata:
=== comment ===
loop3.mx
=== assert ===
exitcode
=== timeout ===
0.1
=== input ===

=== phase ===
codegen pretest
=== is_public ===
True
=== exitcode ===
75

!!*/

