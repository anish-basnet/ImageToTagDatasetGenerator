import os;

directory_name=input('Enter the directory which contains files : ');

#directory_name='images';
try:
    for i,filename in enumerate(os.listdir(directory_name)):
        extension=filename[filename.find('.',):];
        os.rename(os.path.join(directory_name,filename),os.path.join(directory_name,'data'+str(i+1)+extension));
        print(i+1,' Sucessfully Transform');
except FileNotFoundError:
    print("No Directory found!")