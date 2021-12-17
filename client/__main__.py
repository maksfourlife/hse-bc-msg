import client.args
from client.cmd import MsgCmd
from client.oracle import Oracle


Oracle.start()
MsgCmd().cmdloop()
