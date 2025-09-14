import re
import requests
from datetime import date
from bs4 import BeautifulSoup

def get_live_energy_data():
    """Scrape and structure the energy provider data"""
    link = "https://kilovatora.gr/"
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get provider names
    img_tags = soup.select('div.d-flex.justify-content-between img[alt]')
    provider_names = []
    for img in img_tags:
        name = img.get('alt')
        cleaned_name = name.split("- τιμή κιλοβατώρας")[0].strip()
        provider_names.append(cleaned_name)

    contracts_per_provider = [5, 4, 2, 2, 3, 4, 2, 1, 1, 4, 1, 1]

    tables = soup.find_all('table')

    provider_contracts = {}
    all_contracts = []

    # Extract all contracts
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                contract_name = cells[0].get_text(strip=True)
                contract_name = re.sub(r'Ενημέρωση:.*?\d{4}', '', contract_name).strip()

                if contract_name:
                    before_2000 = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                    after_2000 = cells[3].get_text(strip=True) if len(cells) > 3 else ""

                    contract_data = {
                        'name': contract_name,
                        'price_under_2000': before_2000,
                        'price_over_2000': after_2000
                    }
                    all_contracts.append(contract_data)




    # Assign contracts to providers
    contract_index = 0
    for i, provider in enumerate(provider_names):
        if i < len(contracts_per_provider):
            num_contracts = contracts_per_provider[i]
            provider_contracts[provider] = all_contracts[contract_index:contract_index + num_contracts]
            contract_index += num_contracts

    return provider_contracts


class LivePriceTool:

    def __init__(self, mistral_client):
        self.client = mistral_client
        self.name = "live_price_tool"
        self.description = "Live scrape a greek site for energy prices from different providers and give insights about the prices"

    def get_tool_schema(self):

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "User's question about the energy prices and providers."
                        }
                    },
                    "required": ["user_query"]
                }
            }
        }

    async def generate_insights(self, user_query, energy_data):
        """Generate insights based on user query and energy data"""
        system_prompt = f"""
        You are a Greek energy market analyst. Provide actionable price comparisons and recommendations.

        ANALYSIS STRUCTURE:

        ## Price Summary
        **Cheapest Overall:** [Provider] at [price] €/kWh
        **Best for Low Usage (<2000 kWh):** [Provider] at [price]
        **Best for High Usage (>2000 kWh):** [Provider] at [price]

        ## Provider Comparison Table
        | Provider | Contract | <2000 kWh | >2000 kWh 
        |----------|----------|------------|---------|
        [Complete comparison table]

        ## Savings Analysis
        For a typical household using [X] kWh monthly:
        - **Current average market rate:** [X] €/month
        - **Cheapest option:** [X] €/month (saves [X]% annually)
        - **Premium option benefits:** [List any added services/benefits]

        
        Market Insights
        Price Trends: [Analysis of current pricing vs recent historical data]
        Contract Features: [Notable differences in terms, conditions, green energy options]
        Switching Considerations: [Timeline, fees, procedures for changing providers]
        CALCULATION STANDARDS:
        
        Always show specific euro amounts, not just percentages
        Calculate annual savings for typical usage scenarios
        Include any connection fees, service charges, or switching costs
        Use consistent decimal formatting (€X.XX)
        
        RECOMMENDATION CRITERIA:
        
        Prioritize total cost savings over rate differences
        Consider contract flexibility and customer service reputation
        Note any green energy or renewable options
        Highlight time-limited promotional rates vs standard rates
        
        Provide specific, actionable advice that enables immediate decision-making.

        Current Data: {energy_data}
        Updated: {date.today().strftime('%Y-%m-%d')}
        """

        chat_response = await self.client.chat.complete_async(
            model="ministral-8b-2410",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )

        return chat_response.choices[0].message.content


    async def execute(self, user_query):

        energy_data = get_live_energy_data()

        insights = await self.generate_insights(user_query, energy_data)

        return {
            "status" : True,
            "insights" : insights
        }































































































#
# def main():
#     st.title("🔌 Live Energy Prices & Insights")
#     st.write("Ask questions about current electricity prices in Greece")
#
#     # Get live data
#     if 'energy_data' not in st.session_state:
#         with st.spinner("Loading latest energy prices..."):
#             st.session_state.energy_data = get_live_energy_data()
#
#     # User input
#     user_query = st.text_input(
#         "Ask about energy prices:",
#         placeholder="e.g., 'Which provider has the cheapest rates?' or 'Show me a comparison table'"
#     )
#
#     # Predefined quick queries
#     st.write("**Quick questions:**")
#     col1, col2, col3 = st.columns(3)
#
#     with col1:
#         if st.button("Best deals under 2000 kWh"):
#             user_query = "Which providers offer the best prices for consumption under 2000 kWh?"
#
#     with col2:
#         if st.button("Best deals over 2000 kWh"):
#             user_query = "Which providers offer the best prices for consumption over 2000 kWh?"
#
#     with col3:
#         if st.button("Show comparison table"):
#             user_query = "Create a detailed comparison table of all providers and their contracts"
#
#     # Generate response
#     if user_query:
#         with st.spinner("Analyzing current prices..."):
#             response = generate_insights(user_query, st.session_state.energy_data)
#             st.markdown(response)
#
#     # Show data refresh info
#     st.sidebar.info(f"Data last updated: {date.today().strftime('%Y-%m-%d')}")
#     if st.sidebar.button("Refresh Data"):
#         del st.session_state.energy_data
#         st.rerun()
#
#
# if __name__ == "__main__":
#     main()