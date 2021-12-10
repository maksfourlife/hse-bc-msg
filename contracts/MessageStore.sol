// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract MessageOracle {
	enum MessageType {
		Request,
		Accept,
		Text
	}

	struct Message {
		MessageType _type;
		bytes content;
		address receiver;
		address sender;
    uint time;
	}

	mapping(uint => Message) public messages;
	uint public messageCount;

	function sendMessage(MessageType _type, bytes calldata content, address receiver) external {
		messages[messageCount++] = Message(
			_type,
			content,
			receiver,
			msg.sender,
      block.timestamp
		);
	}
}