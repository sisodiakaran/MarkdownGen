'''
Created on 18-Jul-2014

@author: Karan S. Sisodia
'''

import os
import markup
import sys
import json

try:
    import requests
except:
    print("MarkdownGen require Requests library.")
    print("pip install requests")
    sys.exit(2)

class MarkdownGen():
    """
    Class to generate Markdown to html
    """
    
    def __init__(self, source_dir, destination_dir):
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        files = self._loopThroughFiles(self.source_dir)
        self._createHtmlFiles(files)
    
    def _createHtmlFiles(self, files):
        for file in files:
            file_path = self.destination_dir
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                
            file_path = file_path + '/' + file['name'] + '.html'
                
            if os.access(os.path.dirname(file_path), os.W_OK):
                try:
                    fp = open(file_path)
                except IOError:
                    # If not exists, create the file
                    fp = open(file_path, 'w+')
                    
                html = str(self._getHtmlLayout(file['html']))
                
                fp.write(html)
                fp.close()
    
    def _loopThroughFiles(self, mypath):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(mypath):
            for file in filenames:
                if (file.endswith(".md") or file.endswith(".markdown")):
                    with open(os.path.join(dirpath, file)) as fc:
                        content = fc.read()
                        
                    print "Processing ", file
                    f.append({
                              'name': os.path.splitext(file)[0],
                              'path': os.path.join(dirpath, file),
                              #'content': content,
                              'html': self._convertMarkdownToHtml(content.replace('.md', '.html'))
                              })
        return f
    
    def _convertMarkdownToHtml(self, markdown):
        payload = {
          "text": markdown,
          "mode": "markdown",
          "context": "github/gollum"
        }
        r = requests.post("https://api.github.com/markdown", data=json.dumps(payload))
        return r.text
    
    def _getHtmlLayout(self, content):
        title = "Documentation"
        header = '<small>Generated with MarkdownGen</small>'
        footer = ''
        #http://jasonm23.github.io/markdown-css-themes/screen.css
        styles = ("http://jasonm23.github.io/markdown-css-themes/markdown7.css")
    
        page = markup.page()
        page.init(css=styles, title=title, header=header, footer=footer)
        
        page.div(content, class_='markdowngen')
        
        page.div.close()
        
        return page
        
        