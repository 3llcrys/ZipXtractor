import argparse
import zipfile
import os
import re
 
def parse_arguments():
    parser = argparse.ArgumentParser(prog="ZipXtractor",description="extract specific files or folders from a zip archive")
    parser.add_argument("-a","--action", choices=["list","extract"],required=True, help="action to take")
    parser.add_argument("-f","--file",required=True, help="Zipfile to extract")
    parser.add_argument("-p","--path", help="file or directory path to extract from archive")
    parser.add_argument("-s","--structure",choices=["True","False"], default="True", help="Keep original structure for export (True) or export only file (False)")
    parser.add_argument("-o","--output", help="output path; if $match is used enclosing the path in '' is required")
    parser.add_argument("-ex","--regex", help="regex that can be used on the input filename to modify the output path using groups ()")
    return parser.parse_args()
 
#check if multiple zipfiles should be extracted  
def get_zip_file_list(args):
    zipFileList = []
    if args.file == ".":
        dirFiles = os.listdir(args.file)
        for file in dirFiles:
            if file.endswith('.zip'):
                zipFileList.append(".\\"+os.path.join(file))
    else:
        zipFileList.append(os.path.join(args.file))
    return zipFileList
 
 
# List File contents
def list_contents(args, zipFileList):
    if (args.action).lower() == "list":
        for zipFile in zipFileList:
            print(f'ZipFile: {zipFile}')
            with zipfile.ZipFile(zipFile, 'r') as archiveFile:
                for file in archiveFile.namelist():
                    if (file).endswith('/'):
                        print(f'Folder: {file}')
                    else:
                        print(f'File: {file}')
 
# Extract Files
def extract_files(args, zipFileList):
    if (args.action).lower() == "extract":
        if args.output == None:
            print("Please ensure that the argument '--output' is set for extraction")
        for zipFile in zipFileList:
            # Replace outputpath with regex
            if "$match" in args.output:
                match = re.search(args.regex, zipFile)
                output = (args.output).replace("$match", match.group(1))
                print(f'Regex {args.regex} identified "{match.group(1)}"')
            else:
                output = args.output
            print(f"Files will be extracted to '{output}'")
            with zipfile.ZipFile(zipFile, 'r') as archiveFile:
                # If no Path is set extract entire archvie
                if (args.path is None):
                    with archiveFile as source_file:
                        source_file.extractall(output)
                        exit()
                # if specific path is given as argument extract only item within this path
                if args.path in archiveFile.namelist():
                    with archiveFile.open(args.path) as source_file:
                        # if it is a directory
                        if (args.path).endswith('/'):
                            outputDir = os.path.join((output +'\\'), os.path.basename(os.path.normpath(args.path)))
                            if (args.structure).lower() == "false":
                                os.makedirs(outputDir)
                            # Loop for files of directory if directory
                                for file in archiveFile.namelist():
                                    if file.startswith(args.path):
                                        if not ((file).endswith('/')):
                                            with archiveFile.open(file) as source_file:
                                                outputFile= os.path.join((outputDir +'\\'), os.path.basename(os.path.normpath(file)))
                                                with open(outputFile, 'wb') as dest_file:
                                                    dest_file.write(source_file.read())
                            # Keep file structure
                            if (args.structure).lower() == "true":
                                for file in archiveFile.namelist():
                                    if file.startswith(args.path):
                                        archiveFile.extract(file, output)
                        # if it is only a file
                        else:
                            if (args.structure).lower() == "false":
                                for file in archiveFile.namelist():
                                    if file.startswith(args.path):
                                        outputDir = os.path.join(output)
                                        # create output dir if not existend
                                        if not os.path.exists(outputDir):
                                            os.makedirs(outputDir)
                                        outputFile = os.path.join(output, os.path.basename(args.path))
                                        with archiveFile.open(file) as source_file:
                                            with open(outputFile, 'wb') as dest_file:
                                                dest_file.write(source_file.read())
                            # Keep file structure
                            if (args.structure).lower() == "true":
                                for file in archiveFile.namelist():
                                    if file.startswith(args.path):
                                        archiveFile.extract(file, output)
                else:
                    print(f"Can not find specified path in ZipFile: {args.path}, for directory end with '\' to extract contents.")
 
 
def main():
    args = parse_arguments()
    if args.path != None:
        args.path = (args.path).replace("\\", "/")
    zip_file_list = get_zip_file_list(args)
 
    if args.action.lower() == "list":
        list_contents(args, zip_file_list)
    elif args.action.lower() == "extract":
        extract_files(args, zip_file_list)
 
if __name__ == "__main__":
    main()