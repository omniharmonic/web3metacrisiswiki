
## Definition

The **ERC-20 (Ethereum Request for Comment 20)** standard is the technical blueprint for creating fungible tokens on Ethereum. It defines a common interface that allows any ERC-20 token to be seamlessly integrated into wallets, exchanges, and dApps across the ecosystem.

## Core Properties

### Fungibility
- **Interchangeable units**: Each token is identical to and interchangeable with every other unit
- **Uniform value**: All tokens have the same value and properties
- **No uniqueness**: No individual token has unique characteristics
- **Examples**: Currencies, voting rights, utility tokens, shares

### Standardization
- **Common interface**: All ERC-20 tokens implement the same functions
- **Interoperability**: Any wallet or dApp can support any ERC-20 token
- **Composability**: Tokens can be used in various applications
- **Ecosystem integration**: Seamless integration across Web3 ecosystem

## Required Functions

### Core Functions
- **totalSupply()**: Returns the total number of tokens in circulation
- **balanceOf(address owner)**: Returns the token balance of a specific address
- **transfer(address to, uint256 value)**: Transfers tokens to a recipient address
- **approve(address spender, uint256 value)**: Allows a spender to withdraw tokens
- **allowance(address owner, address spender)**: Checks remaining tokens a spender can withdraw
- **transferFrom(address from, address to, uint256 value)**: Executes approved transfer

### Required Events
- **Transfer**: Emitted when tokens are transferred
- **Approval**: Emitted when approval is granted

## Technical Implementation

### Smart Contract Structure
```solidity
contract ERC20 {
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    uint256 private _totalSupply;
    
    function totalSupply() public view returns (uint256);
    function balanceOf(address account) public view returns (uint256);
    function transfer(address to, uint256 amount) public returns (bool);
    function allowance(address owner, address spender) public view returns (uint256);
    function approve(address spender, uint256 amount) public returns (bool);
    function transferFrom(address from, address to, uint256 amount) public returns (bool);
}
```

### Gas Optimization
- **Efficient storage**: Optimized data structures for gas efficiency
- **Batch operations**: Support for multiple transfers in single transaction
- **Event optimization**: Minimal gas usage for event emissions
- **Function optimization**: Efficient implementation of required functions

## Beneficial Potentials

### Decentralized Finance (DeFi)
- **Stablecoins**: USDC, USDT, DAI for stable value storage
- **Lending protocols**: Aave, Compound for borrowing and lending
- **Decentralized exchanges**: Uniswap, SushiSwap for trading
- **Yield farming**: Automated yield optimization strategies

### Governance Systems
- **Voting rights**: UNI, AAVE tokens for protocol governance
- **Proposal submission**: Token holders can submit governance proposals
- **Decision making**: Collective decision-making through token voting
- **Treasury management**: Token-based treasury allocation

### Fundraising and Investment
- **Initial Coin Offerings (ICOs)**: Raise capital through token sales
- **Venture capital**: Token-based investment and funding
- **Crowdfunding**: Community-driven funding for projects
- **Token distribution**: Fair and transparent token allocation

### Utility and Access
- **Service access**: Tokens required to access services
- **Premium features**: Enhanced functionality for token holders
- **Membership**: Token-based membership and access control
- **Rewards**: Token rewards for participation and contribution

## Detrimental Potentials

### Scams and Fraud
- **Pump and dump schemes**: Artificial price inflation followed by crashes
- **Rug pulls**: Developers abandon projects after raising funds
- **Fake projects**: Non-existent or fraudulent token projects
- **Phishing attacks**: Fake tokens and malicious contracts

### Security Vulnerabilities
- **Smart contract bugs**: Vulnerabilities in token contract code
- **Approval exploits**: Malicious contracts draining user tokens
- **Reentrancy attacks**: Exploiting contract state during execution
- **Integer overflow**: Mathematical errors in token calculations

### Regulatory Challenges
- **Securities violations**: Many tokens may be unregistered securities
- **Compliance complexity**: Difficult to comply with multiple jurisdictions
- **Tax implications**: Unclear tax treatment of token transactions
- **Legal uncertainty**: Unclear legal status and enforcement

### Market Manipulation
- **Wash trading**: Artificial trading volume to manipulate prices
- **Insider trading**: Unfair advantage from privileged information
- **Market manipulation**: Coordinated efforts to move prices
- **Liquidity issues**: Low liquidity leading to price volatility

## Use Cases and Applications

### Financial Applications
- **Digital currencies**: Bitcoin alternatives and stablecoins
- **Payment systems**: Fast and low-cost payment processing
- **Remittances**: Cross-border money transfers
- **Micropayments**: Small value transactions

### Governance Applications
- **DAO governance**: Voting rights in decentralized organizations
- **Protocol governance**: Control over blockchain protocols
- **Community governance**: Local and regional decision-making
- **Corporate governance**: Token-based corporate voting

### Utility Applications
- **Access tokens**: Required to access services and platforms
- **Reward tokens**: Incentives for participation and contribution
- **Loyalty programs**: Customer retention and engagement
- **Gaming tokens**: In-game currency and rewards

### Investment Applications
- **Asset tokenization**: Representing ownership of real assets
- **Fractional ownership**: Dividing high-value assets into smaller units
- **Investment funds**: Token-based investment vehicles
- **Real estate**: Property ownership and rental income

## Technical Considerations

### Gas Optimization
- **Efficient transfers**: Minimize gas costs for token transfers
- **Batch operations**: Multiple transfers in single transaction
- **Storage optimization**: Efficient data structures for gas savings
- **Function optimization**: Streamlined implementation of required functions

### Security Best Practices
- **Code auditing**: Professional security reviews
- **Testing**: Comprehensive test coverage
- **Formal verification**: Mathematical proof of correctness
- **Bug bounties**: Community-driven security testing

### Upgradeability
- **Proxy patterns**: Upgradeable token contracts
- **Modular design**: Separate logic and storage contracts
- **Migration mechanisms**: Smooth transitions to new versions
- **Backward compatibility**: Support for older contract versions

## Ecosystem Impact

### Standardization Benefits
- **Interoperability**: Seamless integration across applications
- **Composability**: Tokens can be used in various combinations
- **Innovation**: Faster development of new applications
- **User experience**: Consistent interface across all tokens

### Economic Effects
- **Liquidity**: Increased liquidity through standardization
- **Market efficiency**: Better price discovery and trading
- **Capital allocation**: More efficient allocation of resources
- **Innovation**: Rapid development of new financial products

### Social Impact
- **Financial inclusion**: Access to financial services for unbanked
- **Global access**: Available to anyone with internet connection
- **Transparency**: Public audit trail of all transactions
- **Democratization**: Reduced barriers to financial participation

## References

- [[Web3 Primitives]] - Comprehensive taxonomy
- [[Web3 Affordances & Potentials]] - Detailed affordances analysis
- [[Web3 and the Generative Dynamics of the Metacrisis v01]] - Role in systemic solutions
- [[Crypto For Good Claims]] - Social impact applications
- [[Call Transcript]] - Discussion of token standards

## Related Concepts

- [[content/Primitives/smart contracts]] - Technical foundation
- [[tokenization]] - Core mechanism
- [[Decentralized Finance (DeFi)]] - Primary application
- [[Governance Tokens]] - Use case
- [[Composability]] - Key design principle
