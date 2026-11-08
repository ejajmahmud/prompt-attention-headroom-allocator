"""Unit tests for prompt-attention-headroom-allocator."""
import unittest
from prompt_attention_headroom_allocator.allocator import PromptAttentionHeadroomAllocator


class TestPromptAttentionHeadroomAllocator(unittest.TestCase):
    def test_unconstrained_allocation(self):
        alloc = PromptAttentionHeadroomAllocator(total_context_limit=10000, min_headroom=2000)
        q = alloc.allocate(system_needed=1000, scratchpad_needed=2000, docs_needed=2000)
        self.assertEqual(q.system_tokens, 1000)
        self.assertEqual(q.scratchpad_tokens, 2000)
        self.assertEqual(q.docs_tokens, 2000)
        self.assertEqual(q.headroom_tokens, 5000)
        self.assertEqual(q.total, 10000)

    def test_overage_scaling_preserves_headroom(self):
        alloc = PromptAttentionHeadroomAllocator(total_context_limit=10000, min_headroom=2000)
        q = alloc.allocate(system_needed=2000, scratchpad_needed=8000, docs_needed=8000)
        self.assertGreaterEqual(q.headroom_tokens, 2000)
        self.assertLessEqual(q.total, 10000)
