# Definition

MACI (Minimal Anti-Collusion Infrastructure) is a privacy-focused Ethereum application that provides private and collusion-resistant on-chain voting. Its architecture relies on several cryptographic primitives including:

- Elliptic Curves: MACI uses the Baby Jubjub elliptic curve for cryptographic operations.
    
- Key Pairs: Private keys are generated using cryptographically secure methods and public keys are points on the Baby Jubjub curve.
    
- Message Signing: Uses Edwards-curve Digital Signature Algorithm (EdDSA) for signing messages.
    
- Hash Functions: Employs the Poseidon hash function optimized for zero-knowledge (ZK) proofs and SHA256 for input compression.
    
- Message Encryption: Uses Poseidon in DuplexSponge mode and Elliptic Curve Diffie-Hellman (ECDH) for shared key generation to encrypt votes so that only the coordinator and message sender can decrypt them.
    
- Merkle Trees: Uses quinary Merkle trees (5 leaves per node) with Poseidon hashes for efficient computation in smart contracts.
    

MACI thus employs advanced cryptographic primitives like elliptic curve cryptography, zero-knowledge friendly hash functions, and encryption schemes specifically tailored for Ethereum smart contract use to enable secure, private, and tamper-resistant on-chain voting.[maci.pse+1](https://maci.pse.dev/docs/v1.2/primitives)

1. [https://maci.pse.dev/docs/v1.2/primitives](https://maci.pse.dev/docs/v1.2/primitives)
2. [https://maci.pse.dev/docs/v1.2/introduction](https://maci.pse.dev/docs/v1.2/introduction)
3. [https://github.com/privacy-scaling-explorations/maci](https://github.com/privacy-scaling-explorations/maci)
4. [https://github.com/privacy-scaling-explorations/maci/discussions/847](https://github.com/privacy-scaling-explorations/maci/discussions/847)
5. [https://vitalik.eth.limo/general/2024/10/29/futures6.html](https://vitalik.eth.limo/general/2024/10/29/futures6.html)
6. [https://archive.devcon.org/devcon-7/maci-why-do-we-need-private-voting-and-what-are-we-up-to/](https://archive.devcon.org/devcon-7/maci-why-do-we-need-private-voting-and-what-are-we-up-to/)
7. [https://ethglobal.com/events/circuitbreaker/prizes/privacy-scaling-explorations](https://ethglobal.com/events/circuitbreaker/prizes/privacy-scaling-explorations)
8. [https://x.com/PrivacyEthereum](https://x.com/PrivacyEthereum)
9. [https://projects.ethberlin.org/submissions/376/](https://projects.ethberlin.org/submissions/376/)
10. [https://www.youtube.com/@PrivacyEthereum/videos](https://www.youtube.com/@PrivacyEthereum/videos)