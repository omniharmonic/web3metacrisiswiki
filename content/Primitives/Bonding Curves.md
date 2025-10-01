# Bonding Curves

Bonding curves are mathematical functions that define the relationship between token price and supply in automated market makers and token distribution mechanisms. They enable the creation of markets for tokens without requiring traditional order books or centralized exchanges.

## Mathematical Foundation

A bonding curve establishes a deterministic relationship where token price increases as supply increases, following a predetermined mathematical function. Common implementations use linear, exponential, logarithmic, or sigmoid curves, each creating different economic dynamics for token buyers and sellers.

## Core Mechanisms

The bonding curve smart contract acts as an automated market maker, minting new tokens when users purchase and burning tokens when users sell. Price discovery occurs algorithmically based on current supply, while liquidity is provided by the curve itself rather than external market makers.

## Economic Properties

Different curve shapes create distinct economic behaviors. Linear curves provide consistent price increases, exponential curves create accelerating appreciation that can discourage late adoption, while sigmoid curves balance early accessibility with later stability. Reserve ratios determine price volatility and the portion of funds held in reserve.

## Applications

Bonding curves find application in various contexts: continuous token organizations for funding projects, curation markets where tokens represent quality signals, governance tokens with evolving value based on participation, and social tokens that reflect community engagement and reputation.

## Benefits and Limitations

Bonding curves eliminate the need for initial liquidity provision and enable immediate price discovery for new tokens. However, they can create front-running opportunities, may not reflect underlying value beyond supply dynamics, and can produce extreme price volatility in thin markets.

## Implementation Considerations

Successful bonding curve implementations require careful selection of curve parameters, robust smart contract security, consideration of economic incentives and potential attack vectors, and clear communication of the mathematical relationship to users.

## Related Concepts

- [[automated market makers (AMMs)]]
- [[Tokenomics]]
- [[Price Discovery]]
- [[Liquidity Pools]]
- [[content/Primitives/smart contracts]]