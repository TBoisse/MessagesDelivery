class Message{
    constructor(content, hour) {
        this.content = content;
        this.hour = hour;
    }
}

class MessageBlock{
    constructor(user){
        this.user = user;
        this.messages = [];
    }

    appendSpread(content, hour){
        this.messages.push(new Message(content, hour))
    }
}

class Chat{
    constructor(){
        this.messageBlocks = [];
    }

    appendSpread(user, content, hour){
        let createNewBlock = false;
        if(this.messageBlocks.length == 0 || this.messageBlocks.at(-1).user != user){
            const block = new MessageBlock(user)
            this.messageBlocks.push(block);
            createNewBlock = true;
        }
        this.messageBlocks.at(-1).appendSpread(content, hour)
        return createNewBlock;
    }

    isFirstMessageLastBlock(){
        return this.messageBlocks.at(-1).messages.length == 1;
    }
}