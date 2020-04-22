from import_hook import add_mdoc_hook
from somebody import People
import somebody

def main():
    Me = People("zhangliang","3000")
    Me.Hello()
    print(somebody.__doc__)

if __name__ == "__main__":
    main()