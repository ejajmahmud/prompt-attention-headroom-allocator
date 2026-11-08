"""CLI for prompt-attention-headroom-allocator."""
import sys
import argparse
from .allocator import PromptAttentionHeadroomAllocator


def main():
    parser = argparse.ArgumentParser(description="Prompt Attention Headroom Allocator CLI")
    parser.add_argument("--demo", action="store_true", help="Run attention headroom allocation demo")
    args = parser.parse_args()

    if args.demo:
        allocator = PromptAttentionHeadroomAllocator(total_context_limit=32000, min_headroom=4000)
        quota = allocator.allocate(system_needed=4000, scratchpad_needed=15000, docs_needed=20000)
        print("[+] Computed Dynamic Context Quotas:")
        print(f"    System Tokens: {quota.system_tokens}")
        print(f"    Scratchpad Tokens: {quota.scratchpad_tokens}")
        print(f"    Docs Tokens: {quota.docs_tokens}")
        print(f"    Guaranteed Headroom: {quota.headroom_tokens}")
        print(f"    Total Window: {quota.total} <= 32000")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
