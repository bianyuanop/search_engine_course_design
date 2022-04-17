import re
import nltk
import jieba
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from stopwordsiso import stopwords
from util import get_words_from_html


class Stemmingor: 

    def __init__(self, mode='en') -> None:
        self.words_patt = re.compile('\w+')
        self.mode = mode
        self.stopwords = stopwords(['en', 'zh'])

    def preprocessing(self, raw_html) -> list:
        words = get_words_from_html(raw_html)
        return words
    
    def remove_stop_words(self, words: list) -> list:
        return [word for word in words if word not in self.stopwords and word != ' ']

    def stem_one(self, word) -> str:
        return nltk.PorterStemmer().stem(word)
    
    def stem(self, words: list) -> list:
        result = set()
        words = self.remove_stop_words(words)
        for word in words:
            result.add(self.stem_one(word))
        
        return list(result)
    
    def stem_cn(self, sentence) -> list:
        words = jieba.cut_for_search(sentence)
        words = self.remove_stop_words(words)
        res = set(words)
        return list(res)
    
    def stem_raw_html(self, raw_html) -> list:
        words = self.preprocessing(raw_html)
        if self.mode == 'cn':
            return self.stem_cn(' '.join(words))
        else:
            return self.stem(words)

if __name__ == '__main__':
    enHtml = '''
<html>
<body>
    <div>
        <a href="hello">hello</a>
        <a href="hello">another</a>
        world
        <div>
        a search engine is called information retrieval system
        but sometimes it's not since the development of the technology 
        </div>
    </div>
    <p>hello</p>
    <p>world</p>
    <script>
    (() => {
        console.log("hello, world");
    })();
    </script>
</body>
</html>
'''

    stem = Stemmingor(mode='en')
    paragraph = 'NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.'
    res = stem.stem(paragraph.split(' '))
    print(res)
    
    pass

    cnHtml = '''
<html>
<body>
    <p>
    数学、中英文皆可以混排
    </p>
    <p>
    这个函数接收4个变量作为参数，从函数的定义上看4个变量的含义都是一目了然，即使不写注释，我们基本也能猜到是什么意思，分别是：用户名，密码，身份和验证码，名字和个数看上去觉得都相对比较合理，但是我们说，干净的函数还要包括使用，也就是下面执行登录时调用函数，由于login接收了4个参数，那么对于顺序的输入就变得十分重要，如果输错，那么函数的运行就会出现异常，因此显然这边就相对没有那么合理，那我们优化一下呢
    </p>
    <script>
    (() => {
        console.log("hello, world");
    })();
    </script>
</body>
</html>
    '''

    stem = Stemmingor(mode='cn')
    print(stem.stem_raw_html(cnHtml))