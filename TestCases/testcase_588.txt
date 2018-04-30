int main() {
    int n = 10;
    int sum = 0;
    int i;
    for (i = 1; i <= n; ++i) sum = sum + i;
    int j;
    for (j = 1; j <= n; ++j) sum = sum + 10 + j;
    return sum;
}



/*!! metadata:
=== comment ===
loop2.mx
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
210

!!*/

