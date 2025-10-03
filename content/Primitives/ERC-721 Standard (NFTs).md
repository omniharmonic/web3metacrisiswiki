---
aliases:
  - "erc-721 standard (nfts)"
  - "erc-721-standard-(nfts)"
  - "Erc-721-Standard-(Nfts)"
  - "e-r-c-721 -standard (-n-f-ts)"
---


## Definition

**ERC-721** is a technical standard for non-fungible tokens (NFTs) on the Ethereum blockchain. Unlike [[ERC-20 Standard|ERC-20]] tokens which are fungible (interchangeable), ERC-721 tokens are unique and non-interchangeable, each representing a distinct digital asset.

## Core Properties

### Non-Fungibility
- **Unique identifiers**: Each token has a distinct token ID
- **Individual metadata**: Each token can have unique properties and attributes
- **Ownership tracking**: Clear ownership records for each unique token
- **Transfer mechanisms**: Individual token transfer capabilities

### Standardized Interface
- **balanceOf()**: Returns number of tokens owned by an address
- **ownerOf()**: Returns owner of a specific token ID
- **transferFrom()**: Transfers ownership of a specific token
- **approve()**: Approves another address to transfer a specific token
- **getApproved()**: Returns approved address for a token
- **setApprovalForAll()**: Approves or revokes operator for all tokens

## Beneficial Potentials

### Digital Ownership and Property Rights
- **Unique digital assets**: Art, collectibles, virtual real estate
- **Intellectual property**: Digital certificates, patents, copyrights
- **Identity and credentials**: Digital identity documents, certificates
- **Gaming and virtual worlds**: Unique items, characters, land parcels
- **Real-world asset tokenization**: Property deeds, artwork, luxury goods

### Creative Economy and Creator Rights
- **Artist empowerment**: Direct monetization without intermediaries
- **Royalty mechanisms**: Automated royalty payments to creators
- **Provenance tracking**: Immutable history of ownership and authenticity
- **Fractional ownership**: Dividing high-value assets into shares
- **Community ownership**: Collective ownership of digital assets

### New Economic Models
- **Play-to-earn gaming**: Earning unique digital assets through gameplay
- **Virtual economies**: In-game item trading and ownership
- **Digital collectibles**: Sports memorabilia, trading cards, art
- **Membership tokens**: Access to exclusive communities or services
- **Utility tokens**: Access to specific functions or services

## Detrimental Potentials

### Speculation and Market Manipulation
- **Price volatility**: Extreme price swings and market bubbles
- **Pump and dump schemes**: Coordinated price manipulation
- **Wash trading**: Artificial volume and price inflation
- **Market manipulation**: Insider trading and price fixing
- **FOMO-driven purchases**: Irrational investment decisions

### Environmental and Technical Issues
- **High energy consumption**: Proof-of-work mining for transactions
- **Storage challenges**: Metadata storage and permanence issues
- **Technical complexity**: User experience barriers
- **Scalability limitations**: High gas costs for transactions
- **Centralization risks**: Platform dependencies and control

### Legal and Regulatory Challenges
- **Intellectual property disputes**: Ownership and copyright issues
- **Money laundering**: Use of NFTs for illicit financial activities
- **Tax implications**: Unclear tax treatment of NFT transactions
- **Consumer protection**: Lack of regulatory oversight
- **Cross-border issues**: International legal complexities

## Technical Implementation

### Smart Contract Structure
```solidity
interface ERC721 {
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
```

### Metadata Standards
- **Token URI**: Points to metadata describing the token
- **JSON metadata**: Standardized format for token properties
- **IPFS integration**: Decentralized metadata storage
- **On-chain metadata**: Storing properties directly on blockchain
- **Dynamic metadata**: Metadata that can change over time

## Use Cases and Applications

### Digital Art and Collectibles
- **Digital artwork**: Unique digital creations by artists
- **Trading cards**: Digital versions of collectible cards
- **Memorabilia**: Sports, music, and entertainment collectibles
- **Photography**: Unique digital photographs
- **Generative art**: Algorithmically created unique pieces

### Gaming and Virtual Worlds
- **In-game items**: Weapons, armor, tools, and accessories
- **Virtual real estate**: Land parcels in virtual worlds
- **Characters and avatars**: Unique digital personas
- **Achievements**: Digital trophies and accomplishments
- **Membership passes**: Access to exclusive game content

### Identity and Credentials
- **Digital identity**: Self-sovereign identity documents
- **Educational certificates**: Academic and professional credentials
- **Membership cards**: Access to exclusive communities
- **Event tickets**: Unique access to events and experiences
- **Loyalty programs**: Unique rewards and benefits

## Integration with Other Primitives

### [[smart contracts]]
- **Automated logic**: Self-executing rules for NFT behavior
- **Royalty mechanisms**: Automatic creator payments
- **Access control**: Gated content and services
- **Marketplace logic**: Automated trading and auctions

### [[Decentralized Autonomous Organizations (DAOs)]]
- **Governance tokens**: Voting rights in DAO decisions
- **Membership NFTs**: Access to DAO participation
- **Reward mechanisms**: Unique rewards for contributions
- **Identity verification**: Proof of membership and participation

### [[Composability]]
- **Cross-platform assets**: NFTs usable across multiple applications
- **Layered functionality**: Combining multiple NFT features
- **Interoperability**: NFTs working with different protocols
- **Modular design**: Building complex systems from simple components

## References

- **Source Documents**: [[Web3 Primitives]], [[Paper Outline]]
- **Technical Specification**: [ERC-721 Standard](https://eips.ethereum.org/EIPS/eip-721)
- **Related Standards**: [[ERC-20 Standard]], [[ERC_1155_Standard]]

## Related Concepts

- [[tokenization]] - The process of creating digital representations of assets
- [[Digital_Ownership]] - New forms of property rights in digital spaces
- [[Creator_Economy]] - Economic models empowering content creators
- [[Virtual_Economies]] - Economic systems within digital environments
- [[Intellectual_Property]] - Legal frameworks for digital asset ownership
