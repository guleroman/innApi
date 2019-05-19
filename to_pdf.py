from subprocess import call

def convert_file(output_file,input_file):
    call('libreoffice --headless --convert-to pdf --outdir %s %s ' %
         (output_file, input_file), shell=True)
    return ('ok')