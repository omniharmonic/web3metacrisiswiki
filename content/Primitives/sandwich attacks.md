---
aliases:
  - "sandwich-attacks"
  - "Sandwich-Attacks"
---


## Definition

**Sandwich Attacks** are a specific type of [[MEV]] extraction and [[front running]] technique where an attacker places two transactions—one before and one after a target transaction—to manipulate the price and extract value from the victim. The attack gets its name from "sandwiching" the victim's transaction between the attacker's buy and sell orders.

## Technical Architecture

### Attack Mechanism
- **Pre-transaction**: Buy order placed before victim's transaction
- **Target transaction**: Victim's transaction executes at manipulated price
- **Post-transaction**: Sell order placed immediately after victim's transaction
- **Value extraction**: Profit from artificial price movement

### Execution Requirements
- **Mempool monitoring**: Identifying profitable target transactions
- **Gas price optimization**: Ensuring correct transaction ordering
- **Atomic execution**: All three transactions must execute in sequence
- **Slippage calculation**: Maximizing extractable value

### Target Selection
- **Large trades**: Transactions that will significantly move prices
- **High slippage tolerance**: Users with loose price protection
- **Popular tokens**: Assets with sufficient liquidity for manipulation
- **DEX transactions**: Automated market maker interactions

## Attack Vectors

### Automated Market Maker (AMM) Exploitation
- **Constant product formula**: Exploiting mathematical price curves
- **Liquidity pool manipulation**: Temporarily affecting token ratios
- **Slippage amplification**: Increasing user's price impact

### Cross-DEX Arbitrage Sandwiching
- **Multi-venue attacks**: Coordinating across multiple exchanges
- **Price discrepancy exploitation**: Creating and exploiting price differences
- **Liquidity fragmentation**: Using market structure against users

### Token Launch Sniping
- **New token listings**: Exploiting initial liquidity provision
- **Presale exploitation**: Manipulating early trading activity
- **Pump and dump coordination**: Coordinated price manipulation

## Economic Impact

### User Losses
- **Increased slippage**: Users receive worse prices than expected
- **Hidden costs**: Extraction not visible in transaction fees
- **Reduced trading efficiency**: Discouraging legitimate trading activity

### Market Effects
- **Price manipulation**: Artificial price movements
- **Liquidity fragmentation**: Reduced market depth and efficiency
- **Trust erosion**: Users losing confidence in fair execution

### Scale of Extraction
- **Millions extracted daily**: Significant value extracted from users
- **Automated systems**: Bots executing thousands of attacks
- **Sophisticated operations**: Professional MEV extraction businesses

## Protection Mechanisms

### Technical Defenses
- **Private mempools**: Hiding transactions from public view
- **Commit-reveal schemes**: Cryptographic transaction protection
- **Batch auctions**: Grouping transactions to prevent ordering manipulation
- **MEV-protected RPCs**: Services offering sandwich attack protection

### User-Level Protection
- **Slippage limits**: Setting tight maximum price movement bounds
- **Private transaction pools**: Using services like Flashbots Protect
- **Timing strategies**: Avoiding predictable trading patterns
- **Alternative execution venues**: Using protected trading environments

### Protocol-Level Solutions
- **Fair ordering protocols**: Preventing transaction reordering
- **MEV redistribution**: Sharing extraction benefits with users
- **Encrypted mempools**: Hiding transaction details until execution
- **Threshold decryption**: Time-delayed transaction revelation

## Detection and Analysis

### On-Chain Analysis
- **Transaction pattern recognition**: Identifying sandwich attack signatures
- **Address clustering**: Tracking attacker wallet relationships
- **Profit calculation**: Measuring extracted value
- **Victim identification**: Finding affected users

### Monitoring Tools
- **MEV dashboards**: Real-time attack tracking
- **Alert systems**: Notifying users of potential attacks
- **Research platforms**: Academic analysis of extraction patterns
- **Community tools**: Open-source detection systems

## Legal and Ethical Considerations

### Market Manipulation
- **Traditional finance parallels**: Similar to prohibited practices in regulated markets
- **Unfair advantage**: Exploiting privileged position for profit
- **Victim harm**: Clear financial damage to other users

### Regulatory Response
- **Enforcement challenges**: Difficulty regulating decentralized systems
- **International coordination**: Cross-border nature of blockchain activity
- **Technical complexity**: Regulatory understanding of attack mechanisms

### Community Standards
- **Ethical debates**: Community discussions on acceptable practices
- **Protocol governance**: Decentralized decision-making on attack prevention
- **Social consensus**: Informal norms around fair trading

## Mitigation Strategies

### Individual Protection
- **Education**: Understanding attack mechanisms and protection methods
- **Tool usage**: Employing MEV protection services
- **Trading practices**: Avoiding predictable and vulnerable patterns

### Protocol Development
- **Fair ordering research**: Developing attack-resistant transaction ordering
- **MEV minimization**: Reducing extractable value through design
- **User protection**: Building protection into protocol layer

### Ecosystem Solutions
- **Protected trading venues**: Exchanges offering sandwich attack protection
- **MEV redistribution**: Sharing extraction benefits with affected users
- **Community coordination**: Collective action against harmful extraction

## Related Concepts

- [[MEV]] - Broader category of value extraction
- [[front running]] - General transaction ordering exploitation
- [[automated market makers (AMMs)]] - Primary target of sandwich attacks
- [[Slippage]] - User cost amplified by attacks
- [[Arbitrage]] - Legitimate trading vs. exploitative extraction
- [[Gas]] - Fee mechanism used in attack execution
- [[Market_Manipulation]] - Broader category of unfair practices
- [[decentralized exchanges]] - Venues where attacks occur
- [[Flash Loans]] - Tool enabling sophisticated attacks
- [[Liquidity]] - Market property exploited in attacks

## References

- Research/Web3_Systemic_Solutions_Essay_Outline.md - Line 1370
- Research/Web3_Affordances_Potentials.md - AMM and DEX mechanics
- Flashbots research on MEV and sandwich attacks
- Academic papers on blockchain transaction ordering
- MEV protection service documentation
