"""
An example of using argparse.

COSC435

Micah Sherr <msherr@cs.georgetown.edu>
Georgetown University


Hint: try running this program via:

  python example_argparse.py --help

"""

import argparse


def main():
    parser = argparse.ArgumentParser()

    # add a required argument, which can either be specified
    # via -n or --name.  Store the result in a variable called "name"
    parser.add_argument('-n', '--name', dest='name', help='your first name', required=True)

    # add an optional argument, which must be an integer
    parser.add_argument('-a', '--age', dest='age', help='your age', type=int)

    # add a command-line argument that has no parameter -- i.e., it's true iff it's specified
    # note that "store_true" is a special string that tells argparse what to store if this
    # command-line argument is provided
    parser.add_argument('-t', '--mytest', dest='foobar', help='doesn\'t really do much', action="store_true")
    args = parser.parse_args()
    
    print( "Hello there!" )
    print( "Your name is %s" % args.name )   # see "dest" in the first add_argument call
    if args.age is not None:
        print( "You specified your age.  Ten years from now you'll be %d.\n" % (args.age + 10) )

    if args.foobar is True:
        print( "You specified the -t or --mytest option" )
    else:
        print( "You did not specify the -t or --mytest option" )
        

if __name__ == '__main__':
    main()
    
