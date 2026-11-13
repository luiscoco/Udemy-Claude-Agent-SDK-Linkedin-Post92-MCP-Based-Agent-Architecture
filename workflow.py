"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    def get_policy(arguments):
        key = arguments['name']
        if key not in data['policies']:
            raise ValueError('Unknown policy')
        return {'name': key, 'text': data['policies'][key], 'source': 'bundled policy fixture'}
    observation = get_policy({'name': data['policy']})
    options = in_process_tool('get_policy', 'Retrieve one named policy from the approved catalogue.', {'name': str}, get_policy) if agent.live else None
    answer = await agent.ask('policy_lookup', 'Use get_policy and answer only from its returned text.', {'name': data['policy']}, observation['text'], sdk=options)
    return {'tool_name': 'mcp__lesson__get_policy', 'reference_observation': observation, 'answer': answer, 'server_type': 'in-process SDK MCP'}
