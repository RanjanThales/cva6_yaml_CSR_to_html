#!/usr/bin/env python
# coding: utf-8

import yaml
from yaml.loader import SafeLoader
import json
import argparse

parser = argparse.ArgumentParser(description='YAML file to HTML table or CSV converter',
                epilog='YAML-Table')
parser.add_argument('--inputFile', dest='inputfile', required=True, help="input yaml file to process")
parser.add_argument('--outFolder', dest='outFolder', required=False, help="output folder")
args = parser.parse_args()
INPUT_YAML = args.inputfile
outFolder = ""
outFolder = args.outFolder

#with open('cv64a6_csr_template.yaml') as f:
#    data = yaml.load(f, Loader=SafeLoader)

with open(INPUT_YAML, 'r') as yaml_in, open("example.json", "w") as json_out:
    yaml_object = yaml.safe_load(yaml_in)
    json.dump(yaml_object, json_out)


#from json2html import *
#json2html.convert(json = yaml_object)


import copy
data = copy.deepcopy(yaml_object)

li_final = []

for i in data:
    d = copy.deepcopy(i)
    for key, value in list(d.items()):        
        if (isinstance(value, (dict,list))):
            del d[key]
        elif key == 'address':
            d[key] = hex(value)
        elif (isinstance(value, str)):
            d[key] = value.strip('\n')
        
    li_final.append(d)


import pandas as pd
df_main = pd.DataFrame(data=li_final)
df_main = df_main.fillna(' ')

#df.to_html(classes='table table-striped')
pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

#html_string = '''
#<html>
#  <head><title>Tabular Format</title></head>
#  <link rel="stylesheet" type="text/css" href="df_style.css"/>
#  <body>
#    {table}
#    <br>
#    {table}
#  </body>
#</html>.
#'''
#
## OUTPUT AN HTML FILE
#with open('tabular_format.html', 'w') as f:
#    f.write(html_string.format(table=df_main.to_html(classes='mystyle')))


# In[7]:


html_string1 = '''
<html>
  <head><title>Tabular Format</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    '''
    
html_string_last='''
  </body>
</html>.
'''


with open('df_style.css', 'r') as cssFile:
     style = cssFile.read()
print(
)
html_string1 += df_main.to_html(classes='tbl_main_style', index=False)
df_main.to_csv("output.csv")

#from pretty_html_table import build_table
#html_string1 = build_table(df_main, 'blue_light')

def logError(logText):
    with open('error.dat', 'a') as f:
        f.write(logText)
        f.write("\n\n\n")
        
with open('error.dat', 'w') as f:
        f.write("Error Log----")
        f.write("\n")
        
for i in data:
    body_ext = "\n<br>\n\n<br>\nCSR : "+i['csr']+"\n<br>\n"+"CSR Address : "+hex(i['address'])+"\n<br>\n"+"Reset Value :         "+"\n<br>\n"
    try:
        rv32 = i['rv32']

        lst_bit = []
        lst_mode = []
        lst_desc = []
        for j in rv32:
            if isinstance(j, dict):
                try:
                    bit = str(j['msb'])+":"+str(j['lsb'])
                    mode = j['type']
                    desc = j['description'].strip('\n')
                    lst_bit.append(bit)
                    lst_mode.append(mode)
                    lst_desc.append(desc)
                except KeyError:
                    logError("One or many msb/lsb/type/description not found for - "+i['csr']+" "+hex(i['address']))
        df1 = pd.DataFrame(list(zip(lst_bit, lst_mode, lst_desc)),
                columns =['Bit#', 'Mode', 'Description'])

        html_string1 = html_string1 + body_ext + df1.to_html(classes='mystyle', index=False)

        with open('output.csv', 'a') as f:
            f.write('\n\n')
            f.write("CSR : ,"+i["csr"]+"\n")
            f.write("CSR Address : ,"+hex(i["address"])+"\n")
            f.write("Reset Value : ,"+" "+"\n")
        df1.to_csv('output.csv', mode='a', index = False)
    except KeyError:
        logError("rv64 not found for - "+i['csr']+" "+hex(i['address']))

html_final = html_string1 + html_string_last
with open('tabular_format.html', 'w') as f:
    f.write(html_final)
print("Process Complete")




