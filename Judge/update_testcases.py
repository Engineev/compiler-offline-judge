import requests
import time
import os
from html.parser import HTMLParser

oj_root_url = 'http://blacko.cn:6002'
testcases_url = '/Compiler/testcases'
testcases_path = '../TestCases'

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
        elif tag == 'span' and attrs[0] == ('class', 'glyphicon glyphicon-ok'):
            # enabled testcase
            testcase = get_text(oj_root_url + self.testcase_url)
            out_file = os.path.join(testcases_path, self.testcase_url.split('/')[-1])
            with open(out_file, 'w', encoding='utf8') as f:
                f.write(testcase)

    def handle_endtag(self, tag):
        if not self.in_tbody:
            return
        if tag == 'tbody':
            self.in_tbody = False

def process_html(html):
    parser = TestCaseHTMLParser()
    parser.parser_init()
    parser.feed(html)

def update_testcases():
    if not os.path.exists(testcases_path):
        os.makedirs(testcases_path) 

    html = get_text(oj_root_url + testcases_url)
    process_html(html)

update_testcases()