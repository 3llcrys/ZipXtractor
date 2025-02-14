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
    if args.file.endswith("."):
        dirFiles = os.listdir(args.file)
        for file in dirFiles:
            if file.endswith('.zip'):
                zipFileList.append((args.file).replace("\\.", "")+"\\"+os.path.join(file))
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
        if args.output is None:
            print("Please ensure that the argument '--output' is set for extraction")
            return
        for zipFile in zipFileList:
            # Replace output path with regex
            if "$match" in args.output:
                match = re.search(args.regex, zipFile)
                if match:
                    output = args.output.replace("$match", match.group(1))
                    print(f'Regex {args.regex} identified "{match.group(1)}"')
                else:
                    print(f"No match found in filename '{zipFile}' using regex '{args.regex}'")
                    continue
            else:
                output = args.output
            print(f"Files will be extracted to '{output}'")

            with zipfile.ZipFile(zipFile, 'r') as archiveFile:
                # If no Path is set, extract the entire archive
                if args.path is None:
                    archiveFile.extractall(output)
                    continue

                # Determine if the path is a directory
                path_is_directory = args.path.endswith('/')

                # Extract files based on the specified path
                found = False
                for file in archiveFile.namelist():
                    if file.startswith(args.path):
                        found = True
                        # Determine the relative path based on whether the directory itself should be included
                        if path_is_directory:
                            #ignore directory
                            relative_path = file[len(args.path):]
                            destination = os.path.join(output, relative_path)
                        else:
                            #include directory
                            relative_path = file[len(os.path.dirname(args.path)):]
                            destination = os.path.join(output, relative_path)

                        # Keep original structure
                        if args.structure.lower() == "true":
                            archiveFile.extract(file, output)
                        else:
                            # extract files without structure
                            if not file.endswith('/'):
                                if path_is_directory:
                                    # Dont include directory
                                    destination = os.path.join(output, os.path.basename(file))
                                else:
                                    #include the directory
                                    destination = os.path.join(output, os.path.relpath(file, os.path.dirname(args.path)))
                                
                                # Write / Extract files
                                os.makedirs(os.path.dirname(destination), exist_ok=True)
                                with archiveFile.open(file) as source_file:
                                    with open(destination, 'wb') as dest_file:
                                        dest_file.write(source_file.read())

                if not found:
                    print(f"Cannot find specified path in ZipFile: {args.path}. Available paths:")
                    for name in archiveFile.namelist():
                        print(name)
 
def main():
    args = parse_arguments()
    if args.path != None:
        args.path = (args.path).replace("\\", "/")
    zip_file_list = get_zip_file_list(args)
    print(zip_file_list)
 
    if args.action.lower() == "list":
        list_contents(args, zip_file_list)
    elif args.action.lower() == "extract":
        extract_files(args, zip_file_list)
 
if __name__ == "__main__":
    main()