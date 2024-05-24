# Some Linux Basics

## Reasoning
The docker image for this project is derived from Ubuntu (Linux distribution), and it is headless, meaning it does not have a GUI, and you will be interacting with it in the command line.

## Reading the Bash prompt
Bash is the command line interpreter you are using inside of this image.
If you run the image, you will notice a prompt before your cursor.
It is in this format:
```
[user]@[hostname]:[current-directory]
```

### User
You will be logged in as the user "root" by default.
As the name implies, the root user is the root of all permissions, and you have full permission to do anything inside the container.
This means you won't have any permissions errors, but it does mean you need to be somewhat careful with what you do, as your system will not hesitate to delete the entire file system if you tell it to.
However, keep in mind that you are working on a Docker container, meaning everything you do will be erased after you exit the container and rerun the image.
This should prevent damage to your host.

### Hostname (container ID)
Typically "hostname" refers to a network hostname (something you could see on your WiFi router's settings), but in this case it has been set to your container id.
This is useful when you need to run docker commands on the container while it is running. (For instance, copying files to and from the container and your computer's filesystems.)

### Directory
Directories on a file system are a tree. The root node (directory) on Linux (and other UNIX-based OSes like MacOS) is the directory "/". (On Windows the root directory is "C:\\" or similar.)
From here, you have a combination of directories and files. Directories (aka folders) contain references to other directories and files.
Files are always leaves on the tree. (For the most part, technically if you get into links this gets a little more complex.)

In your bash prompt, you will see the path from your current directory all the way back to the root directory (known as an absolute path).
Ex: /home/turtle/Documents/ means that / has a reference to home, which has a reference to turtle, which has a reference to Documents, which is your current directory.

## Commands
### How to use commands
Commands are often written in the following form:
```
[command] [flag] [flag argument] [etc.]
```

### Flags
The "command" is the name of the command you intend to run. (The name in the headers of this section.)
Flags specify an alternate behavior of the command you are running and are often written in one of two forms:
```
-f
--form
```
Commonly used flags will usually have a one-letter one-dash form, and all flags will typically have a two-dash longer form.
If a command supports both, they can be used interchangeably.

### Help
Most commands, and often scripts (executable files), will support a help page.
This can typically be accessed with `-h` or `--help`.
This help page will specify some brief information about the usage of a command, as well as some common flags.

### man (manual)
Sometimes the help page doesn't provide all the information you need, or perhaps simply want to know more about a command (or library sometimes).
In that case, the manual command, `man`, is your best friend. He's not fully installed on the lake temperature image, but you can also look up "man" pages with your web browser.

Usage: `man [command name]`

Once you've opened the man page, you can scroll up and down with your arrow keys or j and k, and use q to quit.

### cd (change directory)
It does exactly what it sounds like.

Usage: `cd [directory]`

"directory" can be an absolute path or a local path.

An absolute path is written starting at the root directory "/". For example:
```
/usr/lib/
```

A local path starts at your current directory. Say we have this directory structure:
```
/
└── home
    └── turt
        ├── cool-stuff
        └── fancy-files
```

And say that we are in the directory "/home/turt/". One way to write a local path is to just type a path from your current directory.
We can access the path "/home/turt/cool-stuff/" from our current directory with the path "cool-stuff/". Additionally, "." acts as a 
placeholder for your current directory, so an equivalent local path would be "./cool-stuff/".

However, what if we want to go to a parent directory? We can do that too, using "..". ".." represents the parent directory
of our current directory, so, if we are in "/home/turt/cool-stuff/" and we want to access the directory "/home/turt/fancy-files",
we can use the path "../fancy-files".

### ls (list)

Lists the contents (files and directories) inside of a directory

Usage: `ls`
Alternate usage: `ls [directory]`

The first usage will list the contents of your current directory, but you can optionally specify a different directory,
as shown in the second usage.

List more information with this flag: `-l` (stands for long).
This will list all of the contents vertically and includes information such as ACL permissions, user and group owner, file size (in 4KiB blocks typically), 
and the date of the last time the file was modified.

### pwd (print working directory)

Prints your working directory (the directory you are currently operating within).

Usage `pwd`

### cat (concatenate)

Prints the contents of a file.

Usage `cat [file path]`

### cp (copy)

Copies files or directories from the first path to the second.
Can also be used to rename the copy.

Usage `cp [path1] [path2]`

Using two file paths will result in making a copy that is also renamed to the file listed in the second path.

Example:

```
.
└── turt
    ├── cool-stuff
    └── fancy-files
        └── cool-file.txt
```

Copying without rename:
```
cp ./turt/fancy-files/cool-file.txt ./turt/cool-stuff/
```

Results in:
```
.
└── turt
    ├── cool-stuff
    │   └── cool-file.txt
    └── fancy-files
        └── cool-file.txt
```

Copying with rename:

```
cp ./turt/fancy-files/cool-file.txt ./turt/cool-stuff/fancy-file.txt
```

Results in:
```
.
└── turt
    ├── cool-stuff
    │   └── fancy-file.txt
    └── fancy-files
        └── cool-file.txt
```

### mv (move)

Works the same way as `cp`, but deletes the original. Can be used similarly to rename a file or directory.

### file

Analyses the contents of a file and prints what it type of file it is. (Not the extension.)

Usage: `file [file path]`

Example output, with text.txt being a normal text file:
```
text.txt: ASCII text
```

Example output, with text.txt being an executable compiled from a C script:
```
text.txt: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=6eb1cb964bdbe7af60bfae5a59a2b1de18b5889b, for GNU/Linux 4.4.0, not stripped
```

Example output, with text.txt being a python script:
```
text.txt: Python script, ASCII text executable
```

## Referencing multiple files in one path 
You can reference multiple files or directories using one of two methods.

### Wildcard
Wildcard: `*`. This acts as a match for any characters in any amount.

Using this directory structure:
```
.
├── flying
│   ├── evenmoretext.txt
│   └── turtles
├── moretext.txt
├── pythonfile.py
└── text.txt
```

The path `./*` will match `flying/`, `moretext.txt`, `pythonfile.py`, and `text.txt`.
Note that it does not recurse into directories.

The path `./*.txt` will match `moretext.txt` and `text.txt`.
The path `./more*.txt` will just match `moretext.txt`.

### Curly braces and commas
Format `{first,second}`.

Think of these as being arrays looped through by a for loop. Additionally, adding
