import sys, getopt
import scripts.windowsautomate as wsa


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print('main.py -f <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('tmain.py -f <file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            inputfile = arg
    print('Input file is:', inputfile)
    wsa.run(inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
