import sys
import os
import comtypes.client

wdFormatPDF = 17

#in_file = os.path.abspath(sys.argv[1])
#out_file = os.path.abspath(sys.argv[2])

word = comtypes.client.CreateObject('Word.Application')
doc = word.Documents.Open('D:/github/innApi/tpl_invoice_4.docx')
doc.SaveAs('D:/github/innApi/tpl_3.pdf', FileFormat=wdFormatPDF)
doc.Close()
word.Quit()