contract WavesPresale {
    address public owner;
    
    struct Sale
    {
        bytes32 txid;   
        uint128 amount;
        uint date;
    }
    
    Sale[] public sales;
    uint32 public numberOfSales;
    uint128 public totalTokens;

    function WavesPresale() {
        owner = msg.sender;
        numberOfSales = 0;
    }

    function newSale(bytes32 txid, uint128 amount) {
        if (msg.sender != owner) return;

        sales.push(Sale({
                txid: txid,
                amount: amount,
                date: now
            }));
        numberOfSales += 1;
        totalTokens += amount;
    }
    
}
