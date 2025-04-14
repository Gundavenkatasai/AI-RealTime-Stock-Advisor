import pandas as pd
import re

class StockChatbot:
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.stock_symbols = stock_data['Symbol'].str.upper().tolist()
        
    def respond(self, message):
        message = message.upper().strip()
        
        
        stock_symbol = self._extract_stock_symbol(message)
        
        if stock_symbol:
            return self._get_stock_info(stock_symbol, message)
        elif "LIST" in message or "ALL" in message or "STOCKS" in message:
            return self._list_all_stocks()
        elif "HELP" in message:
            return self._get_help()
        else:
            return {
                'response': "I'm not sure I understand. You can ask about specific stocks by symbol or name, or type 'help' for assistance.",
                'type': 'text'
            }
    
    def _extract_stock_symbol(self, message):
        
        for symbol in self.stock_symbols:
            if f' {symbol} ' in f' {message} ':
                return symbol
        
        
        symbol_mapping = {
            'RELIANCE': ['RELIANCE', 'RIL'],
            'TATASTEEL': ['TATA STEEL', 'TATA IRON'],
            'HDFCBANK': ['HDFC BANK'],
            'ICICIBANK': ['ICICI BANK'],
            'BAJFINANCE': ['BAJAJ FINANCE'],
            'BHARTIARTL': ['AIRTEL', 'BHARTI AIRTEL'],
            'INFY': ['INFOSYS'],
            'TCS': ['TATA CONSULTANCY'],
            'ITC': ['ITC LIMITED'],
            'LT': ['LARSEN', 'L&T'],
            'M&M': ['MAHINDRA', 'MAHINDRA & MAHINDRA']
        }
        
        for symbol, names in symbol_mapping.items():
            for name in names:
                if name.upper() in message:
                    return symbol
        
        return None
    
    def _get_stock_info(self, symbol, question):
        stock = self.stock_data[self.stock_data['Symbol'].str.upper() == symbol].iloc[0]
        
        if 'PRICE' in question or 'LTP' in question:
            response = f"{symbol} is currently trading at ₹{stock['LTP']}"
            if 'CHNG' in question or 'CHANGE' in question:
                change = stock['Chng']
                percent_change = stock['% Chng']
                direction = "up" if change >= 0 else "down"
                response += f", {direction} by ₹{abs(change)} ({abs(percent_change)}%)"
            return {'response': response, 'type': 'text'}
        
        elif 'HIGH' in question and '52' not in question:
            return {'response': f"{symbol}'s current day high is ₹{stock['High']}", 'type': 'text'}
        
        elif 'LOW' in question and '52' not in question:
            return {'response': f"{symbol}'s current day low is ₹{stock['Low']}", 'type': 'text'}
        
        elif '52' in question and 'HIGH' in question:
            return {'response': f"{symbol}'s 52-week high is ₹{stock['52w H']}", 'type': 'text'}
        
        elif '52' in question and 'LOW' in question:
            return {'response': f"{symbol}'s 52-week low is ₹{stock['52w L']}", 'type': 'text'}
        
        elif 'VOLUME' in question:
            return {'response': f"{symbol}'s trading volume is {stock['Volume (lacs)']} lacs shares", 'type': 'text'}
        
        elif 'PERFORMANCE' in question or 'CHANGE' in question:
            change_30d = stock['30 d % chng']
            change_365d = stock['365 d % chng']
            return {
                'response': f"{symbol}'s performance:\n30-day change: {change_30d}%\n365-day change: {change_365d}%",
                'type': 'text'
            }
        
        else:
            
            response = (
                f"{symbol} Stock Information:\n"
                f"Current Price (LTP): ₹{stock['LTP']}\n"
                f"Today's Change: ₹{stock['Chng']} ({stock['% Chng']}%)\n"
                f"Day Range: ₹{stock['Low']} - ₹{stock['High']}\n"
                f"52-Week Range: ₹{stock['52w L']} - ₹{stock['52w H']}\n"
                f"Volume: {stock['Volume (lacs)']} lacs shares\n"
                f"30-Day Performance: {stock['30 d % chng']}%\n"
                f"1-Year Performance: {stock['365 d % chng']}%"
            )
            return {'response': response, 'type': 'text'}
    
    def _list_all_stocks(self):
        stocks_list = ", ".join(self.stock_symbols)
        return {
            'response': f"Here are all the stocks I have data for:\n{stocks_list}",
            'type': 'text'
        }
    
    def _get_help(self):
        help_text = (
            "I can provide information about stocks in the National Stock Exchange of India. Here's what you can ask:\n"
            "- 'What is the price of RELIANCE?'\n"
            "- 'How is INFY performing?'\n"
            "- 'What is the 52-week high for TATASTEEL?'\n"
            "- 'Show me all stocks'\n"
            "- 'What is the volume for HDFCBANK?'\n"
            "\nYou can ask about any stock by its symbol or company name."
        )
        return {'response': help_text, 'type': 'text'}