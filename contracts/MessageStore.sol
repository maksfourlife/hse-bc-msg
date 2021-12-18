// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;


contract MessageStore {
    enum MessageType {
        Request,
        Accept,
        Text
    }

    struct Message {
        MessageType _type;
        bytes content;
        address sender;
        uint timestamp;
    }

    event NewMessage(
        address indexed receiver,
        Message message
    );

    mapping(address => Message[]) public messages;

    function messageCount(address receiver) public view returns (uint256) {
        return messages[receiver].length;
    }

    function sendMessage(
        MessageType _type,
        bytes calldata content,
        address receiver
    ) external {
        Message memory message = Message(
            _type,
            content,
            msg.sender,
            block.timestamp
        );

        messages[receiver].push(message);
        emit NewMessage(receiver, message);
    }
}