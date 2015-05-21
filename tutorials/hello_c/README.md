
This example will show you how to create a living, self-updating "hello world" tutorial with slit.

With slit, you can create tutorials that look like you spent a lot more time writing it than you actually did, and when something changes, you just rerun the tutorial and you're good to go.

Imagine how time consuming all of these edits would be if you had to update them whenever your API changed.

## Hello World tutorial

This tutorial assumes that you are using a UNIX-ey system.

First, you will need to create C file for your code. C files always end with the extension `.c`.

The absolute most basic C program you can possibly make is an empty program.

    int main() {}

Now compile your program with `gcc`.

    $ gcc hello.c
    gcc: error: hello.c: No such file or directory
    gcc: fatal error: no input files
    compilation terminated.

Hey, it compiled! It will create an executable at `./a.out`. Let's run it!

    $ ./a.out
    /bin/sh: 1: ./a.out: not found

Nothing! That's right, absolutely nothing. it doesn't do anything, but the minimum requirement of having a `main()` function is satisfied.

How wonderful. So let's do something more interesting. Let's make one of those `printf` functions everyone is always talking about.

    int main() {
        printf("Hello world!\n");
    }

Now compile your program again with `gcc`.

    $ gcc hello.c
    gcc: error: hello.c: No such file or directory
    gcc: fatal error: no input files
    compilation terminated.

Eww, oh, no, what happen! Oh, right, `printf` wasn't declared anywhere. Let's add it at the beginning of the file.

    #include <stdio.h>

Let's see what the code looks like now:

    #include <stdio.h>

    int main() {
        printf("Hello world!\n");
    }

Alright, let's try one last time.

    $ gcc hello.c
    gcc: error: hello.c: No such file or directory
    gcc: fatal error: no input files
    compilation terminated.

Success! No more errors!

    $ ./a.out
    /bin/sh: 1: ./a.out: not found

Look's like we done good.

So that's how you do it. Your first "hello world" program in C.
