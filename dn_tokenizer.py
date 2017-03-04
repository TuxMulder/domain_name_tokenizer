import domain_tokenizer as dt
import tldextract
###
from mrcc import CCJob


class DnTokenizer(CCJob):
  def process_record(self, record):
    if record['Content-Type'] != 'text/plain':
      return
    
    url = record.header['warc-target-uri']
    domain = self.__get_domain_name(url)
    payload = record.payload.read()
    tokenization = dt.tokenize_domain_name(domain, payload)
    if tokenization:
        yield (domain, tokenization)

  def __get_domain_name(self, url):        
    ext = tldextract.extract(url)
    return "{}.{}".format(ext.domain, ext.suffix)





if __name__ == '__main__':
  DnTokenizer.run()
