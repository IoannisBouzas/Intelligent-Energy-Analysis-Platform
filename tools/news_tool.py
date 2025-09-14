import os
from datetime import datetime
from tavily import TavilyClient


class GreekNewsTool:
    """Greek news research tool for the main agent"""

    def __init__(self, mistral_client):
        self.mistral_client = mistral_client
        tavily_api = os.getenv('TAVILY_API_KEY')
        self.tavily_client = TavilyClient(tavily_api)

    def get_tool_schema(self):
        """Return tool schema for agent integration"""
        return {
            "type": "function",
            "function": {
                "name": "greek_news_tool",
                "description": "Search and analyze Greek news articles on any topic from the query. Provides summaries, relevance scores, and insights from Greek news sources.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The news query to search for"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    async def execute(self, query):
        """Execute Greek news search and analysis"""
        try:
            # Search phase
            context = self._search_news(query)

            if not context or len(context["sources"]) == 0:
                return {
                    "success": False,
                    "error": "No relevant Greek news articles found",
                    "articles": [],
                    "summary": "No articles available for analysis"
                }

            # Extract content
            extracted_context = self._extract_context(context)

            # Generate analysis
            analysis = await self._analyze_news(extracted_context, query)

            return {
                "success": True,
                "articles": extracted_context["sources"],
                "analysis": analysis,
                "search_query": query,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "articles": [],
                "summary": f"Error occurred during news analysis: {str(e)}"
            }

    def _search_news(self, query):
        """Search Greek news"""

        # Primary search with Greek domains
        search_response = self.tavily_client.search(
            query,
            max_results=7,
            topic="news",
            time_range="week",
            search_depth="advanced",
            include_domains=[
                "newsbomb.gr","kathimerini.gr",
                "tanea.gr", "tovima.gr",
                "iefimerida.gr", "protothema.gr",
                "sport24.gr", "in.gr",
                "gazzetta.gr", "documentonews.gr",
                "energypress.gr"
            ]
        )

        return {
            "sources": [
                {
                    "url": result["url"],
                    "title": result["title"],
                    "snippet": result.get("content", "")[:400]
                }
                for result in search_response["results"]
            ]
        }

    def _extract_context(self, context):
        """Extract full content from articles"""
        urls = [source["url"] for source in context["sources"]]

        try:
            extract_response = self.tavily_client.extract(urls)

            # Match extracted content
            for extracted_result in extract_response["results"]:
                for source in context["sources"]:
                    if source["url"] == extracted_result["url"]:
                        source["content"] = extracted_result["raw_content"]

            # Handle failed extractions
            for failed_result in extract_response["failed_results"]:
                for source in context["sources"]:
                    if source["url"] == failed_result["url"]:
                        source["content"] = source.get("snippet", "Content extraction failed")

        except Exception:
            # Fallback to snippets
            for source in context["sources"]:
                if "content" not in source:
                    source["content"] = source.get("snippet", "No content available")

        return context

    async def _analyze_news(self, context, query):
        """Generate comprehensive news analysis"""

        # Prepare context for analysis
        context_text = ""
        for i, source in enumerate(context["sources"][:5]):  # limit to the 5 top articles
            content = source.get('content', source.get('snippet', 'No content'))[:1000]
            context_text += f"Article {i + 1}:\nTitle: {source['title']}\nURL: {source['url']}\nContent: {content}\n\n"

        prompt = f"""You are a Greek news analyst. Analyze these articles for query: {query}

        Available Articles:
        {context_text}

        Provide analysis in EXACTLY this format for each relevant article:

        [Article Title]
        Source: [Domain]  
        
        Executive Summary: [3-4 sentences with key findings]
        Key Developments:
        URL: [URL]
        • [Most significant finding with specific details]
        • [Secondary important point]
        • [Third point if relevant]
    
        Focus on factual reporting and preserve important Greek terms with English explanations.
        Always include the full working URL for each article."""

        response = await self.mistral_client.chat.complete_async(
            model="mistral-medium-2508",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        return response.choices[0].message.content