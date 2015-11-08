from qdb import set_trace, RemoteCommandManager

def f():
    in_f = True
    return 'getting out of f'

def main():
    set_trace(
        uuid='qdb',
        host='localhost',
        port=8001,
        cmd_manager=RemoteCommandManager(),
    )
    mutable_object = {}
    print 'Hello world!'
    f()
    print mutable_object

if __name__ == '__main__':
    main()