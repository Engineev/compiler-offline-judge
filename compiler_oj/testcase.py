import os


class TestCase:
    def __init__(self, raw, filename="unknown", t=1.0):
        self.__raw = raw
        self.filename = filename
        self.src = self.__read_source()
        self.comment = self.__find_block("comment")
        self.input = self.__find_block("input")
        self.output = self.__format_output(self.__find_block("output"))
        self.assertion = self.__find_block("assert")
        self.timeout = self.__find_block("timeout")
        if self.timeout != "":
            self.timeout = float(self.timeout) 
        else:
            self.timeout = 10.0
        self.timeout /= t # Continue for t seconds 续一秒!!
        self.exitcode = self.__find_block("exitcode")
        self.exitcode = int(self.exitcode) if self.exitcode != "" else None
        self.phase = self.__find_block("phase")

    @staticmethod
    def __format_output(raw):
        return '\n'.join(list(map(lambda x: x.strip(), raw.split('\n'))))

    def __read_source(self):
        end = self.__raw.find("/*!! metadata:")
        return self.__raw[0:end]

    def __find_block(self, name):
        title = '=== ' + name + ' ==='
        beg = self.__raw.find(title)
        if beg == -1:
            return ''
        beg += len(title)
        end = self.__raw.find("===", beg)
        if end == -1:
            end = self.__raw.find("!!*", beg)
        if end == -1:
            return ""
        return self.__raw[beg:end].strip()


def read_testcases(dirs, t):
    testcases = []

    for dir in dirs:
        names = os.listdir(dir)
        print(dir + " : " +  str(len(names)))
        for name in names:
            __, extension = os.path.splitext(name)

            if extension != ".txt" and extension != ".mx":
                # print(extension)
                continue

            with open(os.path.join(dir, name)) as f:
                raw = f.read()
                testcases.append(TestCase(raw, name, t))

    print("testcases at all: " + str(len(testcases)))
    # print([i.phase for i in testcases])
    return testcases
