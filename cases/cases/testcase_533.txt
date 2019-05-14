int qpow(int a,int p,int mod) {
    int t = 1;
    int y = a;
    while(p>0){
        if((p&1) == 1)t=t*y % mod;
        y=y*y % mod;
        p=p / 2;
    }
    return t;
}





int main() {
    println(toString(qpow(2,10,10000)));
    return 0;
}


/*!! metadata:
=== comment ===
codegen1-5140309569-xushichao.txt
=== input ===

=== assert ===
output
=== timeout ===
1.0
=== output ===
1024
=== phase ===
codegen pretest
=== is_public ===
True

!!*/

