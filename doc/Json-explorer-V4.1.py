# Json explorer.py
# This script reads the Json files exported by Soundcraft Ui12/16/24 digital mixers and prettyprints the result
# Author: Patrick Keogh with some decoding hints from Motte on Github.
#
# V1. MVP, just produced a listing
# V2. Converted to tabular view
# V3. Column headings
# V4. Convert to HTML rendering = produces a .html file which is displayed in your default browser.
# V4.1 Folded the "Other" entries into the HTML approach
#
import json
import os
import webbrowser
from datetime import datetime

def ht(t):
## open the category-specific HTML file and write the headers
    fn = os.environ.get("tmp") + t + "_" + repr(datetime.timestamp(datetime.now())).replace(".","") + ".html"
    f = open(fn, 'w')
    f.write('<!DOCTYPE html>')
    f.write('<HTML>')
    f.write('   <HEAD>')
    f.write('      <TITLE>' + t + ' mixer values</TITLE>')
    f.write('   </HEAD>')
    f.write('   <BODY>')
    f.write('    <h1>' + request[r]+ ' mixer values</h1>')
    return f,fn
    
def hc(f,fn):
## write the footers, close and display
        f.write('   </BODY>')
        f.write('</HTML>')
        f.close()
        webbrowser.open('file:///'+fn)
    
json_file = "C:\\Users\\patri\\Downloads\\Ui16 Mojo Street (1).json" # Set to your file location
f = open(json_file,'r')
json_string = f.read()
f.close
Ui_dict = json.loads(json_string)
trans = {"i":"Input ", "a":"Aux ", "f":"FX ", "s":"Subgroup ", "l":"Line in", "m":"Master ", "p":"Play(USB) "}
request = trans
request['o'] = 'Other'
format_string = "{:>15}"
format_string_f = "{:>15.4}"
fn = ""

while True:
    for i in request: print(i, "(", request[i], ")")
    r = input('?')[:1].lower()
    t = {}
    l = {}
    columns = 0
    if r == '': break
    for a_key in sorted(Ui_dict):
        levels = a_key.count(".")
        if levels <= 1 and r == 'o':
            l[a_key] = Ui_dict[a_key]
        elif levels >= 2:
            top,rest = a_key.split(".",1)
            if top == r:
                chan, key = rest.split(".",1)
                try:
                    nchan = int(chan)
                    if key in t:
                        t[key].insert(nchan,Ui_dict[a_key])
                        if nchan > columns: columns = nchan
                    else:
                        t[key] = []
                        t[key].insert(nchan,Ui_dict[a_key])
                except:
                    print("\n Unhandled entry ",a_key, '-> ',Ui_dict[a_key])

    if l != {}: # we accumulated some non-tabular key value pairs
        if os.path.exists(fn): os.remove(fn)
        html_file, fn = ht(request[r])
## write the rows
        for key in l:
            html_file.write('<p>' + key + ' -> ' + repr(l[key]) + '</p>')
        hc(html_file, fn)

    if t != {}: # we accumulated some tabular data
        if os.path.exists(fn): os.remove(fn)
        html_file, fn = ht(request[r])
        html_file.write('    <table border=1>')
## write the table header
        html_file.write('      <tr>')
        html_file.write('        <th>Channel</th>')                
        for i in range(1, columns+2):
            html_file.write('        <th>' + repr(i) + '</th>')
        html_file.write('      </tr>')
## write the table rows                        
        for key in t:
            html_file.write('      <tr>')
            html_file.write('      <td>' + key + '</td>')
            for j in range(0,len(t[key])):
                x = t[key][j]
                if isinstance(x,float):
                    s = format_string_f.format(x)
                else:
                    s = str(x)
                html_file.write('      <td>' + s + '</td>')
        hc(html_file, fn)
