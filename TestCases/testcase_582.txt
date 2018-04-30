int tak(int x, int y, int z) {
    if(y < x) {
        return 1 + tak( tak(x - 1, y , z),
            tak(y - 1, z , x),
            tak(z - 1, x , y)
        );
    } else {
       return z;
    }
}

int main() {
    return tak(18,12,6);
}




/*!! metadata:
=== comment ===
function2.mx
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
13

!!*/

