int main() {
    int a = 5;
    int b = 0;
    int c;
    if (b != 0 && a/b != 1) {
        c = 10;
    } else {
        c = 20;
    }

    if (!(c == 10 && a/b == 0 && a == 5))
        c = 30;

    return c;
}



/*!! metadata:
=== comment ===
simple2.mx
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
30

!!*/

