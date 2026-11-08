"""Core Prompt Attention Headroom Allocator implementation."""
from typing import Dict, Any, Optional


class SegmentQuota:
    def __init__(self, system_tokens: int, scratchpad_tokens: int, docs_tokens: int, headroom_tokens: int):
        self.system_tokens = system_tokens
        self.scratchpad_tokens = scratchpad_tokens
        self.docs_tokens = docs_tokens
        self.headroom_tokens = headroom_tokens

    @property
    def total(self) -> int:
        return self.system_tokens + self.scratchpad_tokens + self.docs_tokens + self.headroom_tokens


class PromptAttentionHeadroomAllocator:
    def __init__(self, total_context_limit: int = 128000, min_headroom: int = 4096):
        self.total_limit = total_context_limit
        self.min_headroom = min_headroom

    def allocate(self, system_needed: int, scratchpad_needed: int, docs_needed: int) -> SegmentQuota:
        available_input = self.total_limit - self.min_headroom
        total_requested = system_needed + scratchpad_needed + docs_needed

        if total_requested <= available_input:
            # Plenty of room: give full requested plus remaining to headroom
            actual_headroom = self.total_limit - total_requested
            return SegmentQuota(system_needed, scratchpad_needed, docs_needed, actual_headroom)

        # Compression required: system is fixed, scratchpad and docs are proportionally scaled
        fixed_system = min(system_needed, available_input // 4)
        rem_for_payload = available_input - fixed_system
        payload_requested = scratchpad_needed + docs_needed

        if payload_requested > 0:
            scale = rem_for_payload / float(payload_requested)
            actual_scratch = int(scratchpad_needed * scale)
            actual_docs = int(docs_needed * scale)
        else:
            actual_scratch = 0
            actual_docs = 0

        return SegmentQuota(fixed_system, actual_scratch, actual_docs, self.min_headroom)
