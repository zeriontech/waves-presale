contract WavesPresale {
    address public owner;
    
    struct Sale
    {
        bytes32 txid;   
        uint amount;
        uint date;
    }
    
    Sale[] public sales;
    uint32 public numberOfSales;
    uint public totalTokens;

    function WavesPresale() {
        owner = msg.sender;
        numberOfSales = 0;
    }

    function changeOwner(address newOwner) {
        if (msg.sender != owner) return;

        owner = newOwner;
    }

    function newSale(bytes32 txid, uint amount, uint timestamp) {
        if (msg.sender != owner) return;

        sales.push(Sale({
                txid: txid,
                amount: amount,
                date: timestamp
            }));
        numberOfSales += 1;
        totalTokens += amount;
    }

    function () {
        // This function gets executed if a
        // transaction with invalid data is sent to
        // the contract or just ether without data.
        // We revert the send so that no-one
        // accidentally loses money when using the
        // contract.
        throw;
    }

}
