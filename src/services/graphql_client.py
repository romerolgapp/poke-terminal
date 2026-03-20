import aiohttp

import json

class GraphQLClient:
    def __init__(self, aiohttp: aiohttp.ClientSession):
        self.endpoint = "https://spriteserver.pmdcollab.org/graphql"
        self.aiohttp = aiohttp
    
    async def get_pokemon_data(self, pokemon_id: int):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "query": f'{{ monster(filter: [{pokemon_id}]) {{ id name forms {{ path name fullName portraits {{ emotions {{ emotion url }} }} }} }} }}'
        }
        async with self.aiohttp.post(self.endpoint, headers=headers, json=payload) as response:
            return await response.json()
