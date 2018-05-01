import requests
import time
import os
import shutil
import sys, getopt
from html.parser import HTMLParser

oj_root_url = 'http://blacko.cn:6002'
testcases_url = '/Compiler/testcases'
testcases_path = '..'
testcases_subdir = 'TestCases'
get_disabled_testcases = False

def get_text(url):
    try_count = 0
    while try_count < 3:
        try:       
            text = requests.get(url).text
            return text
        except:
            try_count += 1
            time.sleep(3)
    print('[Error] cannot get url \"%s\"' % (url))
    return ''

class TestCaseHTMLParser(HTMLParser):
    def parser_init(self):
        self.in_tbody = False
        self.a_idx = 0
        self.testcase_url = ''

    def get_testcase(self):
        testcase = get_text(oj_root_url + self.testcase_url)
        out_file = os.path.join(testcases_path, testcases_subdir, self.testcase_url.split('/')[-1])
        with open(out_file, 'w', encoding='utf8') as f:
            f.write(testcase)

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.in_tbody = True
        if not self.in_tbody:
            return
        if tag == 'tr':
            self.a_idx = 0
        elif tag == 'a' and self.a_idx == 0:
            self.testcase_url = attrs[0][1]
            self.a_idx += 1
        elif tag == 'span':
            if attrs[0] == ('class', 'glyphicon glyphicon-ok'):
                # enabled testcase
                self.get_testcase()
            elif attrs[0] == ('class', 'glyphicon glyphicon-remove') and get_disabled_testcases:
                # disabled testcase
                self.get_testcase()

    def handle_endtag(self, tag):
        if not self.in_tbody:
            return
        if tag == 'tbody':
            self.in_tbody = False

def process_html(html):
    parser = TestCaseHTMLParser()
    parser.parser_init()
    parser.feed(html)

def print_help():
    print(
'''Options:
  -h, --help                Display this information
  --testcases-dir <dir>     Set <dir> as the directory to store test cases
  --get-disabled            Get all testcases, including disabled ones'''
    )

def update_testcases():
    if os.path.exists(testcases_path):
        shutil.rmtree(testcases_path)
    os.makedirs(testcases_path) 

    html = get_text(oj_root_url + testcases_url)
    process_html(html)

def main(argv):
    global testcases_path
    global get_disabled_testcases
    try:
        opts, _ = getopt.getopt(argv, 'h', ['help', 'testcases-dir=', 'get-disabled'])
    except:
        print_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt == '--testcases-dir':
            testcases_path = arg
        elif opt == '--get-disabled':
            get_disabled_testcases = True
    update_testcases()
    

if __name__ == '__main__':
    main(sys.argv[1:])