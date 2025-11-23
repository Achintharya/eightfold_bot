"""
Simplified Web Context Extraction Module for Company Research Agent
"""

import asyncio
import os
import json
import requests
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

# Load .env from config directory
load_dotenv('config/.env')

# Try to import optional crawl4ai
try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
    from crawl4ai.extraction_strategy import LLMExtractionStrategy
    from pydantic import BaseModel, Field
    
    class PageSummary(BaseModel):
        summary: str = Field(..., description="Detailed page summary related to query")
    
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False


async def save_to_file(data, filename, base_path="./data"):
    """
    Simple file save operation
    
    Args:
        data: Data to save (will be JSON serialized if not string)
        filename: Name of the file
        base_path: Base directory path
    """
    # Ensure directory exists
    Path(base_path).mkdir(exist_ok=True)
    file_path = Path(base_path) / filename
    
    # Serialize data if needed
    if not isinstance(data, str):
        content = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        content = data
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


async def search_web(query: str, max_results: int = 5):
    """
    Search the web using DuckDuckGo (free) or Serper API (if available)
    
    Args:
        query: Search query
        max_results: Maximum number of results
        
    Returns:
        List of URLs
    """
    # Try DuckDuckGo first (free)
    try:
        with DDGS() as search:
            results = search.text(query, max_results=max_results)
            urls = [result["href"] for result in results if "href" in result]
            if urls:
                return urls
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
    
    # Try Serper API if available
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key:
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": serper_key
            }
            payload = {"q": query, "num": max_results}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://google.serper.dev/search", 
                    json=payload, 
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        urls = []
                        for result in data.get("organic", []):
                            link = result.get("link")
                            if link and "youtube.com" not in link and "youtu.be" not in link:
                                urls.append(link)
                        if urls:
                            return urls[:max_results]
        except Exception as e:
            print(f"Serper API search failed: {e}")
    
    return []


async def extract_from_url(url: str, query: str):
    """
    Extract content from a single URL
    
    Args:
        url: URL to extract from
        query: Original search query for context
        
    Returns:
        Dictionary with extracted content
    """
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit text length
            text = text[:3000]  # First 3000 characters
            
            return {
                "url": url,
                "summary": f"Content from {url} about {query}: {text[:500]}...",
                "full_text": text,
                "error": False
            }
        else:
            return {
                "url": url,
                "summary": f"Failed to fetch {url}: Status {response.status_code}",
                "error": True
            }
            
    except Exception as e:
        return {
            "url": url,
            "summary": f"Error extracting from {url}: {str(e)}",
            "error": True
        }


async def extract(query: str = None, silent_mode: bool = False):
    """
    Main extraction function - search and extract web content
    
    Args:
        query: Search query
        silent_mode: If True, suppress output
        
    Returns:
        List of extracted data
    """
    if not query:
        return []
    
    if not silent_mode:
        print(f"🔍 Searching for: {query}")
    
    # Search for URLs
    urls = await search_web(query)
    
    if not urls:
        if not silent_mode:
            print("No URLs found")
        return []
    
    if not silent_mode:
        print(f"Found {len(urls)} URLs")
    
    # Save sources
    sources_content = f"\n## {query}\n"
    for url in urls:
        sources_content += f"- {url}\n"
    await save_to_file(sources_content, "sources.md")
    
    # Extract content from URLs
    output_data = []
    
    # Try advanced extraction if crawl4ai is available
    if CRAWL4AI_AVAILABLE:
        try:
            browser_config = BrowserConfig(headless=True, verbose=False)
            extraction_strategy = LLMExtractionStrategy(
                llm_config=LLMConfig(
                    provider="mistral/mistral-small-latest", 
                    api_token=os.getenv("MISTRAL_API_KEY")
                ),
                schema=PageSummary.model_json_schema()
            )

            async with AsyncWebCrawler(config=browser_config) as crawler:
                results = await crawler.arun_many(
                    urls=urls, 
                    config=CrawlerRunConfig(
                        cache_mode=CacheMode.BYPASS,
                        extraction_strategy=extraction_strategy
                    )
                )

            for url, result in zip(urls, results):
                if result.success:
                    page_summary = json.loads(result.extracted_content)
                    output_data.append({
                        "url": url,
                        "summary": page_summary.get("summary", ""),
                        "error": False
                    })
                else:
                    output_data.append({
                        "url": url,
                        "summary": f"Crawl failed for {url}",
                        "error": True
                    })
                    
        except Exception as e:
            if not silent_mode:
                print(f"Advanced extraction failed: {e}, using simple extraction")
            # Fall back to simple extraction
            for url in urls:
                data = await extract_from_url(url, query)
                output_data.append(data)
    else:
        # Use simple extraction
        for url in urls:
            if not silent_mode:
                print(f"Extracting from: {url}")
            data = await extract_from_url(url, query)
            output_data.append(data)
    
    # Save extracted data
    await save_to_file(output_data, "context.json")
    
    if not silent_mode:
        print(f"✓ Extracted content from {len(output_data)} sources")
    
    return output_data


# For backward compatibility
async def simple_extract(urls, query):
    """Backward compatibility function"""
    output_data = []
    for url in urls:
        data = await extract_from_url(url, query)
        output_data.append(data)
    await save_to_file(output_data, "context.json")
    return output_data


# For backward compatibility
file_manager = type('FileManager', (), {
    'atomic_write': lambda self, f, c: save_to_file(c, f),
    'atomic_append': lambda self, f, c: save_to_file(c, f)
})()


if __name__ == "__main__":
    # Example usage
    asyncio.run(extract("test query"))
