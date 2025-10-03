---
aliases:
  - "ethereum virtual machine (evm)"
  - "ethereum-virtual-machine-(evm)"
  - "Ethereum-Virtual-Machine-(Evm)"
  - "ethereum -virtual -machine (-e-v-m)"
  - "EVM"
---


## Definition

The **Ethereum Virtual Machine (EVM)** is the computational engine at the heart of the Ethereum protocol. It is a global, decentralized computer that executes smart contracts and manages the state of the Ethereum blockchain.

## Core Architecture

### Quasi-Turing-Complete State Machine
- **Turing-complete**: Ability to run any program, given enough resources
- **"Quasi" qualifier**: All execution processes are finite, limited by gas mechanism
- **Security**: Prevents infinite loops and denial-of-service attacks
- **Sandboxed environment**: Code execution completely isolated from host machine

### Data Components
- **Volatile memory**: Temporary data during execution
- **Permanent storage**: Part of Ethereum state, persists across transactions
- **Stack**: For computations and function calls

### Execution Process
1. **High-level languages** (Solidity, Vyper) → **Bytecode** (EVM instructions)
2. **Opcodes**: Set of instructions processed by EVM
3. **State transition function**: Y(S,T)=S′ where S=current state, T=transactions, S′=new state
4. **Global state update**: All account balances and smart contract data

## Key Properties

### Deterministic Execution
- Same input always produces same output
- Enables consensus across decentralized network
- Critical for trustless coordination

### Gas Mechanism
- **Computational cost**: Every operation has fixed gas cost
- **Security**: Prevents network abuse and infinite loops
- **Economic model**: Users pay for computational resources

### Network Effects
- **Industry standard**: De facto standard for smart contract execution
- **EVM-compatible chains**: Polygon, BNB Smart Chain, Avalanche
- **Interoperability**: dApps portable across multiple chains
- **Composability**: Standardized interface enables building blocks

## Affordances and Potentials

### Beneficial Potentials
- **Decentralized Applications**: Powers entire ecosystem of dApps
- **Complex Financial Instruments**: Enables sophisticated DeFi protocols, DAOs
- **Interoperability**: Easy porting across EVM-compatible blockchains
- **Project Management**: Blockchain state management principles applicable to objective progress measurement

### Detrimental Potentials
- **Exploitable Code**: Any flaws in smart contract logic can be exploited
- **Computational Limits**: Gas constraints can make complex computations prohibitively expensive
- **"Out of gas" errors**: Users lose transaction fees without transaction success

## Role in Web3 Stack

The EVM serves as the **foundational execution layer** for:
- [[smart contracts]] - Programmable logic
- [[Decentralized Autonomous Organizations (DAOs)]] - Governance mechanisms
- **DeFi_Protocols** - Financial applications
- **Token_Standards** - ERC-20, ERC-721, ERC-1155

## Technical Specifications

### Gas Costs
- **Simple operations**: 3-5 gas units
- **Storage operations**: 20,000 gas units
- **Complex computations**: Variable, based on computational complexity

### Opcodes
- **Arithmetic**: ADD, SUB, MUL, DIV
- **Logical**: AND, OR, NOT, XOR
- **Storage**: SSTORE, SLOAD
- **Control flow**: JUMP, JUMPI, CALL, RETURN

## References

- [[Web3 Primitives]] - Comprehensive taxonomy
- [[Web3 Affordances & Potentials]] - Detailed affordances analysis
- [[Web3 and the Generative Dynamics of the Metacrisis v01]] - Role in systemic solutions
- [[Call Transcript]] - Discussion of EVM capabilities

## Related Concepts

- [[smart contracts]] - Primary use case
- [[Gas_Mechanism]] - Economic model
- [[Proof of Stake (PoS)]] - Consensus mechanism
- [[Composability]] - Key design principle
- [[decentralized applications (dApps)]] - Applications built on EVM
