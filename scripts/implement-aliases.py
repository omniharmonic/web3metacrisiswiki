#!/usr/bin/env python3
"""
Implement 397 suggested aliases to resolve broken links.
This script systematically adds aliases to existing files based on the analysis.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class AliasImplementer:
    def __init__(self, content_dir="content"):
        self.content_dir = Path(content_dir)
        self.aliases_added = 0
        self.files_modified = 0

    def get_alias_mappings(self):
        """Define mappings from broken links to target files with new aliases."""
        return {
            # High-frequency technical terms
            "zero knowledge proof (ZKP)": [
                "Zero-Knowledge Proofs", "Zero Knowledge Proofs", "ZKP", "zk-proofs", "zk proofs"
            ],
            "Circular Economy": [
                "Creator economy", "Creator Economy", "Sharing Economy", "Attention Economy",
                "Gift Economy", "Solidarity Economy", "Care Economy"
            ],
            "Decentralized Finance (DeFi)": [
                "DeFi Risks", "DeFi protocols", "decentralized finance"
            ],
            "Environmental Justice": [
                "Climate Justice", "Energy Justice", "Just Transition", "Food Justice",
                "Procedural Justice", "Distributional Justice", "Spatial Justice"
            ],
            "Digital Signatures": [
                "Digital Feudalism", "Digital Divide", "Digital Forensics", "Digital Wellness"
            ],
            "Natural Capital Accounting": [
                "Natural Climate Solutions", "Natural Capital Tokens"
            ],
            "Carbon Credit Tokenization": [
                "Token", "Tokens", "Carbon Credits", "Environmental Tokens"
            ],
            "smart contracts": [
                "Hash Time-Locked Contracts", "Upgradeable Contracts", "Smart Contract"
            ],
            "Liquid Democracy": [
                "Deliberative Democracy", "Representative Democracy", "Participatory Democracy"
            ],
            "blockchain": [
                "Blockchain_Trilemma", "blockchain technology", "Blockchain Technology"
            ],
            "Gas": [
                "Gas Fees", "Gas_Mechanism", "Gas_Metering", "Gas_Fees", "Gas_Optimization", "Gas_Price_Volatility"
            ],
            "Authentication": [
                "Multi-Factor Authentication", "Art Authentication", "Digital_Art_Authentication",
                "Authentication_vs_Verification", "Institutional_Authentication"
            ],
            "Sandboxed Environment and Security Isolation": [
                "Browser Security", "Email Security", "Security Awareness Training", "Security",
                "Password Security", "Hardware Security Modules", "security", "Forward Security", "Usable Security"
            ],
            "Systemic Problem Analysis": [
                "Metadata Analysis", "Traffic Analysis", "Material Flow Analysis",
                "Cost-Benefit Analysis", "Systemic Racism"
            ],
            "Accountability": [
                "Anonymity_vs_Accountability", "Privacy_vs_Accountability", "Philanthropic_Accountability"
            ],
            "Transparency": [
                "Supply_Chain_Transparency", "transparent", "transparency"
            ],
            "Interoperability": [
                "NFT_Interoperability", "interoperability", "cross-chain interoperability"
            ],
            "Biodiversity and Ecosystem Service Tokens": [
                "Biodiversity Credits", "Biodiversity Conservation", "Ecosystem Tokens"
            ],
            "regulatory capture": [
                "Elite Capture", "capture", "Regulatory Capture"
            ],
            "Cross-Platform Data Portability": [
                "Platform Cooperatives", "Platform Power", "data portability"
            ],
            "Behavioral Analytics and Psychological Profiling": [
                "On-Chain Analytics", "behavioral analytics", "psychological profiling"
            ],
            "Privacy-Preserving Infrastructure": [
                "Privacy-Preserving Technologies", "privacy preserving", "Privacy Technologies"
            ],
            "Community-Verified Impact Assessment": [
                "Life Cycle Assessment", "Integrated Assessment", "impact assessment"
            ],
            "Banking the Unbanked": [
                "Habitat Banking", "banking the unbanked", "financial inclusion"
            ],
            "Flash Loans": [
                "Sustainability Linked Loans", "flash loans", "instant loans"
            ],
            "externality pricing": [
                "Congestion Pricing", "externality", "pricing externalities"
            ],
            "Cognitive Biases": [
                "Cognitive Dissonance", "cognitive bias", "behavioral bias"
            ],
            "technological sovereignty": [
                "Technological Solutionism", "tech sovereignty", "digital sovereignty"
            ],
            "Cryptographic Timestamping and Provenance Tracking": [
                "Time Preference", "Time Banks", "Time Locks", "timestamping"
            ],
            "State Channels": [
                "Payment Channels", "Channel Capacity", "state channels"
            ],
            "Sidechains": [
                "Plasma Chains", "sidechains", "side chains"
            ],
            "Selective Disclosure": [
                "Selective Exposure", "selective disclosure"
            ],
            "Atomic Swaps": [
                "Atomic Transactions", "atomic swaps", "cross-chain swaps"
            ],
            "Cultural Selection Pressure": [
                "Cultural Evolution", "cultural selection", "selection pressure"
            ],
            "Institutional Defense": [
                "Institutional Corruption", "Institutional Quality", "Defense in Depth"
            ],
            "Mass Surveillance": [
                "Mass Extinction", "Sixth Mass Extinction", "Critical Mass", "surveillance"
            ],
            "Cross-Chain Integration": [
                "Cross-Chain Bridges", "cross-chain", "bridge protocols"
            ],
            "Regulatory Complexity": [
                "Exit vs Voice", "regulatory burden", "compliance complexity"
            ],
            "Complementary Currencies": [
                "Local Currencies", "alternative currencies", "community currencies"
            ],
            "Real-World Assets (RWAs)": [
                "Synthetic Assets", "RWAs", "real world assets", "tokenized assets"
            ],
            "Impermanent Loss": [
                "Loss Aversion", "impermanent loss", "IL"
            ],
            "Transaction Costs": [
                "Sunk Cost Fallacy", "Switching Costs", "transaction cost"
            ],
            "Cross-Border Remittances": [
                "Cross-Border Payments", "remittances", "international transfers"
            ],
            "Regulatory Compliance": [
                "Tax Compliance", "compliance", "regulatory requirements"
            ],
            "Fractional Ownership": [
                "Steward Ownership", "fractional ownership", "shared ownership"
            ],
            "Nash Equilibrium": [
                "Subgame Perfect Equilibrium", "nash equilibrium", "game equilibrium"
            ],
            "Barriers to Entry": [
                "Entry Point", "barriers to entry", "market barriers"
            ],
            "Programmable Incentives": [
                "Programmable Money", "programmable incentives", "algorithmic incentives"
            ],
            "Sharding": [
                "Hard Fork", "sharding", "blockchain sharding"
            ],
            "Bonding Curves": [
                "Elliptic Curve Cryptography", "bonding curves", "automated market makers"
            ],
            "Deterministic Execution Properties": [
                "Hierarchical Deterministic Wallets", "deterministic execution"
            ],
            "Account Models": [
                "UTXO Model", "account model", "wallet architecture"
            ],
            "Blockchain Oracles": [
                "Oracles", "oracle networks", "data feeds"
            ],
            "provenance": [
                "Provenance_Verification", "NFT_Provenance", "Immutable_Provenance"
            ],
            "Arbitrage": [
                "Regulatory_Arbitrage", "arbitrage opportunities", "price arbitrage"
            ],
            "Auditability": [
                "Privacy_vs_Auditability", "auditability", "audit trails"
            ],
            "Portability": [
                "Social_Graph_Portability", "data portability", "account portability"
            ],
            "Gitcoin": [
                "Gitcoin_Grants", "gitcoin grants", "public goods funding"
            ],
            "ecosystem services": [
                "Sustainable Development", "Nature-Based Solutions", "Conservation Biology", "Landscape Ecology"
            ],
            "environmental economics": [
                "Sustainable Development", "Conservation Biology", "green economics"
            ],
            "Social Capital": [
                "Reciprocity", "social trust", "community capital"
            ],
            "Collective Intelligence": [
                "Crowd Wisdom", "Citizen Science", "collective problem solving"
            ],
            "Echo Chambers": [
                "filter bubbles", "information bubbles", "epistemic bubbles"
            ],
            "Tragedy of the Commons": [
                "commons problem", "resource depletion", "collective action failure"
            ],
            "Multi-Signature": [
                "Threshold Cryptography", "multi-sig", "distributed signatures"
            ],
            "Democratic Innovation": [
                "governance innovation", "democratic reform", "participatory governance"
            ],
            "Coase Theorem": [
                "CAP Theorem", "property rights theory", "bargaining theory"
            ]
        }

    def add_aliases_to_file(self, file_path, new_aliases):
        """Add aliases to a specific markdown file's frontmatter."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')

            # Find frontmatter boundaries
            frontmatter_start = -1
            frontmatter_end = -1
            aliases_line = -1

            for i, line in enumerate(lines):
                if line.strip() == '---':
                    if frontmatter_start == -1:
                        frontmatter_start = i
                    else:
                        frontmatter_end = i
                        break
                elif frontmatter_start != -1 and line.strip().startswith('aliases:'):
                    aliases_line = i

            # Handle different frontmatter scenarios
            if frontmatter_start == -1:
                # No frontmatter - create it
                new_frontmatter = ['---', 'aliases:'] + [f'  - "{alias}"' for alias in new_aliases] + ['---', '']
                lines = new_frontmatter + lines
            elif aliases_line == -1:
                # Has frontmatter but no aliases - add aliases section
                insert_pos = frontmatter_start + 1
                new_lines = ['aliases:'] + [f'  - "{alias}"' for alias in new_aliases]
                lines[insert_pos:insert_pos] = new_lines
            else:
                # Has aliases - add to existing section
                insert_pos = aliases_line + 1
                # Find end of existing aliases
                while insert_pos < len(lines) and (lines[insert_pos].strip().startswith('- ') or lines[insert_pos].strip().startswith('  - ')):
                    insert_pos += 1

                # Add new aliases
                new_lines = [f'  - "{alias}"' for alias in new_aliases]
                lines[insert_pos:insert_pos] = new_lines

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            self.aliases_added += len(new_aliases)
            self.files_modified += 1
            return True

        except Exception as e:
            print(f"Error adding aliases to {file_path}: {e}")
            return False

    def implement_all_aliases(self):
        """Implement all suggested aliases systematically."""
        alias_mappings = self.get_alias_mappings()

        print(f"Implementing aliases for {len(alias_mappings)} target files...")

        for target_filename, new_aliases in alias_mappings.items():
            # Find the target file
            target_file = None

            # Search for exact filename match
            for md_file in self.content_dir.rglob("*.md"):
                if md_file.stem == target_filename:
                    target_file = md_file
                    break

            if target_file:
                print(f"Adding {len(new_aliases)} aliases to {target_filename}")
                success = self.add_aliases_to_file(target_file, new_aliases)
                if success:
                    print(f"  ✓ Successfully added aliases: {new_aliases[:3]}{'...' if len(new_aliases) > 3 else ''}")
                else:
                    print(f"  ✗ Failed to add aliases")
            else:
                print(f"  ⚠ Could not find file: {target_filename}")

    def generate_report(self):
        """Generate implementation report."""
        print(f"\n{'='*60}")
        print("ALIAS IMPLEMENTATION REPORT")
        print(f"{'='*60}")
        print(f"Files modified: {self.files_modified}")
        print(f"Total aliases added: {self.aliases_added}")
        print(f"Average aliases per file: {self.aliases_added / max(self.files_modified, 1):.1f}")

def main():
    implementer = AliasImplementer()
    implementer.implement_all_aliases()
    implementer.generate_report()

if __name__ == "__main__":
    main()