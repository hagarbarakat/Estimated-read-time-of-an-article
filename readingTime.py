from urllib.error import URLError
from urllib.request import urlopen
import bs4

class Read:
    def __init__(self,url):
        self.url = url
        self.WPM = 200  #words per minute
        self.wlength = 5 #word length

    def extract(self, url):
        """
        extract text, buttons, ... etc from url
        :return: text
        """
        try:
            html = urlopen(self.url).read()
            s4 = bs4.BeautifulSoup(html, 'html.parser')
            texts = s4.findAll(text=True)
            return texts
        except URLError as e:
            if hasattr(e, 'reason'):
                print('[Failed] to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            exit(-1)

    def is_visible(self, element):
        """
        filter out unnecessary data
        :param element:
        :return: boolean
        """
        #filter out CSS styles, Java  Script, HTML headers, comments, new lines
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif isinstance(element, bs4.element.Comment):
            return False
        elif element.string == "\n":
            return False
        return True

    def count_words_in_text(self, text_list):
        total_words = 0
        for current_text in text_list:
            total_words += len(current_text) / self.wlength
        return total_words

    def filter_visible_text(self, page_texts):
        return filter(self.is_visible, page_texts)

    def estimate_reading_time(self):
        texts = self.extract(self.url)
        filtered_text = self.filter_visible_text(texts)
        print(filtered_text)
        total_words = self.count_words_in_text(filtered_text)
        return total_words / self.WPM


url = input("URL of Article:\n")
time = Read(str(url))
estimated = time.estimate_reading_time()
print("Estimated time of this aricle is :", estimated)
