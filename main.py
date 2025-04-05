import streamlit as st
import requests

def fetch_country_data(country_name):
    # Updated API endpoint to v3.1 and using the name endpoint
    url = f'https://restcountries.com/v3.1/name/{country_name}'
    
    try:
        # Add timeout parameter to prevent hanging
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                country_data = data[0]
                name = country_data['name']['common']
                
                # Handle cases where data might be missing
                capital = country_data.get('capital', ['N/A'])[0] if 'capital' in country_data and country_data['capital'] else 'N/A'
                population = country_data.get('population', 'N/A')
                area = country_data.get('area', 'N/A')
                
                # Handle currencies more safely
                currency = 'N/A'
                if 'currencies' in country_data and country_data['currencies']:
                    currency_code = list(country_data['currencies'].keys())[0]
                    currency = country_data['currencies'][currency_code].get('name', currency_code)
                
                region = country_data.get('region', 'N/A')
                flag = country_data.get('flags', {}).get('png', '')
                
                return name, capital, population, area, currency, region, flag
            else:
                return None
        else:
            st.error(f"API Error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please check your internet connection and try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check your internet connection and try again.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("Country Information App")

    country_name = st.text_input("Enter a country name:")
    if country_name:
        with st.spinner("Fetching country information..."):
            country_info = fetch_country_data(country_name)
        
        if country_info:
            name, capital, population, area, currency, region, flag = country_info
            
            # Display flag image
            if flag:
                st.image(flag, width=300)
            
            st.subheader("Country Information:")
            st.write(f"Country: {name}")
            st.write(f"Capital: {capital}")
            st.write(f"Population: {population:,}" if isinstance(population, int) else f"Population: {population}")
            st.write(f"Area: {area:,} sq km" if isinstance(area, (int, float)) else f"Area: {area}")
            st.write(f"Currency: {currency}")
            st.write(f"Region: {region}")
        else:
            st.warning(f"Could not find information for '{country_name}'. Please check the spelling and try again.")

if __name__ == "__main__":
    main()