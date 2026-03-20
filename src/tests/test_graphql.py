
from src.services.graphql_client import GraphQLClient
import aiohttp

import asyncio
import json




async def main():
    async with aiohttp.ClientSession() as session:
        
        client = GraphQLClient(session)
        json_result = await client.get_pokemon_data(3)
        json.dumps(json_result, indent=2)
        print(json.dumps(json_result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
