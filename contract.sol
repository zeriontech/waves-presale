contract WavesPresale {
    address public owner;
    
    struct Sale
    {
        bytes32 txid;   
        uint amount;
        uint date;
    }
    
    Sale[] public sales;
    uint index;
    
    function WavesPresale() {
        owner = msg.sender;
        index = 0;
    }

    function setProposal(bytes32 txid, uint amount) {
        if (msg.sender != owner) return;
        
        sales.push(Sale({
                txid: txid,
                amount: amount,
                date: now
            }));
        index += 1;
    }
    
}


