int main() {
    int n = 20;
    int sum = 0;
    int i = 1;
    while (i <= n) {
        sum = sum + i;
        i = i+1;
    }
    return sum;
}



/*!! metadata:
=== comment ===
loop1.mx
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

