
class TA{
	string state;
	int anger;
}
int init_anger = 100;
int work_anger = 10;
void work(string st, TA ta)
{
	if (ta.anger <= 100) println(st + ", " + ta.state + " enjoys this work. XD");
	else println(st + ", " + ta.state + " wants to give up!!!!!");
	ta.anger = ta.anger + work_anger;
}
int main()
{
	TA mr;
	TA mars;
	mr = new TA;
	mr.state = "the leading TA";
	mr.anger = 0;
	mars = new TA;
	mars.state = "the striking TA";
	mars.anger = init_anger;
	work("MR", mr);
	work("Mars", mars);
	work("Mars", mars);
	return 0;
}


/*!! metadata:
=== comment ===
class_test-mahaojun.mx
=== input ===

=== assert ===
output
=== timeout ===
0.1
=== output ===
MR, the leading TA enjoys this work. XD
Mars, the striking TA enjoys this work. XD
Mars, the striking TA wants to give up!!!!!
=== phase ===
codegen pretest
=== is_public ===
True

!!*/

