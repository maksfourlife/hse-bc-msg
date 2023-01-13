#hse-bc-msg
P2P client for messaging on EVM blockchains with RSA support

Console Repl application for messaging.

To start, enter the secret key of your Matic wallet -secret

- To open a chat, type `> open 0x0..0 (address)`
   - If this is the first message and the encryption key has not been set, you will be prompted to send the recipient a message request
   - If the request was sent to you, you will be prompted to accept it
   - While in a chat, you can send a message by typing `> msg "Message text"`
   - To exit, type `> close`

- You can reset the encryption key by typing `> reset 0x0.00 (address)`

*** At the moment the application is in beta version and has some bugs
   - only the last message is available for viewing
   - for the changes to take effect, the chat must be reopened
  
- To exit the application, use ^C or `> quit`

At startup, you can specify the optional arguments -rpc and -gasprice
